import os
import sys
import pika
import json
import time
import shutil
import zipfile
import requests
import multiprocessing
import psutil
import signal
import uuid
from subprocess import Popen, PIPE, STDOUT
from urllib.parse import urlparse

code_tmp_dir = '/twain/tmp/code'
model_tmp_dir = '/twain/tmp/model'
code_dir = '/twain/code'
model_dir = '/twain/model'
current_process = None

if not os.path.exists(code_tmp_dir):
    os.makedirs(code_tmp_dir)

if not os.path.exists(model_tmp_dir):
    os.makedirs(model_tmp_dir)

if not os.path.exists(code_dir):
    os.makedirs(code_dir)

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

queue = 'device10'
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=queue)

class DownloadHelper:
    def __init__(self, url, tmp_directory, directory):
        self.url = url
        self.tmp_directory = tmp_directory
        self.directory = directory
    
    def can_handle_url(self):
        url_schema = self.get_url_schema()
        file_ext = self.get_file_extension()
        return url_schema in ['http', 'https'] and file_ext == '.zip'

    def get_url_schema(self):
        parsed_url = urlparse(self.url)
        return parsed_url.scheme
    
    def get_file_extension(self):
        file_name = self.get_file_name()
        _, file_ext = os.path.splitext(file_name)
        return file_ext

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def output_path(self):
        base_file_name = self.get_file_name()
        if not base_file_name:
            raise RuntimeError('Cannot set output file for download')

        filename = base_file_name
        filepath = os.path.join(self.tmp_directory, filename)
            
        return filepath

    def process(self):
        if not self.can_handle_url():
            print("Cannot download this url")
            return

        try:
            request = requests.get(self.url, timeout=30, stream=True)
            output_path = self.output_path()
            with open(output_path, 'wb') as fh:
                for chunk in request.iter_content(1024 * 1024):
                    fh.write(chunk)
            self.unzip()
            print("DONE DOWNLOAD.....")
        except Exception as e:
            print("Something went wrong:", e)

    def unzip(self):
        filename = self.get_file_name()
        self.delete_folder_content(self.directory)
        with zipfile.ZipFile(os.path.join(self.tmp_directory, filename), 'r') as zip_ref:
            zip_ref.extractall(self.directory)
        self.delete_folder_content(self.tmp_directory)

    def delete_folder_content(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

class ProcessHelper(multiprocessing.Process):
    def __init__(self, run_command, install_command=None, id=None, require_install_packages=True, cwd=code_dir):
        super(ProcessHelper, self).__init__()
        self.id = id
        self.run_command = run_command
        self.install_command = install_command
        self.env = self.get_env()
        self.cwd = cwd
        self.require_install_packages = require_install_packages
    
    def get_env(self):
        env = os.environ.copy()
        env['MODEL_DIRECTORY'] = model_dir
        env['SOURCE_DIRECTORY'] = code_dir

        return env

    def on_install_success(self):
        print("INSTALL PROCESS ID SUCCESS", self.id)
        # print("DONE INSTALL CODE", code)
        # print("DONE INSTALL CODE Error", error_msg)
    
    def on_install_failed(self, error_msg):
        print("INSTALL PROCESS ID FAIL", self.id)
        print("INSTALL PROCESS Error", error_msg)
        # print("DONE INSTALL CODE", code)

    def on_running_success(self):
        print("RUNNING PROCESS ID SUCCESS", self.id)
        # print("DONE RUNNING CODE", code)
        # print("DONE RUNNING CODE Error", error_msg)

    def on_running_failed(self, error_msg):
        print("RUNNING PROCESS ID FAIL", self.id)
        print("RUNNING PROCESS Error", error_msg)

    def run(self):
        def check_io(process):
            while True:
                output = process.stdout.readline().decode()
                if output:
                    # logger.log(logging.INFO, output)
                    print("=================== output: ", output)
                else:
                    break


        if self.require_install_packages:
            print("BEFORE INSTALL PACKAGES.....................................")
            install_proc = psutil.Popen(self.install_command, stdout=PIPE, stderr=PIPE)
            
            while install_proc.poll() is None:
                check_io(install_proc)

            install_proc.wait()

            if install_proc.returncode != 0:
                out, error_install_msg = install_proc.communicate()
                self.on_install_failed(error_install_msg)
            else:
                self.on_install_success()
                print("BEFORE RUNNING.............................................")
                running_proc = psutil.Popen(self.run_command, env=self.env, cwd=self.cwd, stdout=PIPE, stderr=PIPE)

                while running_proc.poll() is None:
                    check_io(running_proc)

                running_proc.wait()

                if running_proc.returncode != 0:
                    out, error_run_msg = install_proc.communicate()
                    self.on_running_failed(error_run_msg)
                else:
                    self.on_running_success()
        else:
            print("BEFORE RUNNING.............................................")
            running_proc = psutil.Popen(self.run_command, env=self.env, cwd=self.cwd, stderr=PIPE)
            running_proc.wait()
            print("DONE START RUNNING.........................................")
            # if running_proc.returncode != 0:
            #     out, error_run_msg = install_proc.communicate()
            #     self.on_running_failed(error_run_msg)
            # else:
            #     self.on_running_success()
    
    def kill_process_tree(self, sig=signal.SIGTERM, include_parent=False, timeout=None, on_terminate=None):
        pid = self.pid
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)

        if include_parent:
            children.append(parent)
        for p in children:
            p.send_signal(sig)

        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
        return (gone, alive)

    def is_running(self):
        p = psutil.Process(self.pid)
        return p.is_running()

def callback(ch, method, properties, body):
    global current_process
    payload = json.loads(body.decode('ascii'))
    command = payload['command']
    if command == 'model':
        # print("DOWNLOAD_MODEL {}".format(payload["data"]["id"]))
        # Download
        url = payload["data"]["url"]
        download = DownloadHelper(url, model_tmp_dir, model_dir)
        download.process()
    elif command == 'source':
        # print("DOWNLOAD_SOURCE {}".format(payload["body"]["id"]))
        # Download
        url = payload["data"]["url"]
        download_manager = DownloadHelper(url, code_tmp_dir, code_dir)
        download_manager.process()
    elif command == 'run':
        if current_process is not None and current_process.is_running():
            current_process.kill_process_tree()

        # process = popenAndCall(onExit, ['bash', '/twain/code/run.sh'], env, code_dir)
        id = str(uuid.uuid4())
        print("=====================================================")
        print("START PROCESS ID", id)
        process = ProcessHelper(['bash', '/twain/service/run.sh'], install_command=['bash', '/twain/service/install.sh'], id=id)
        process.start()
        current_process = process

        time.sleep(1)

current_process = ProcessHelper(['bash', '/twain/service/run.sh'], require_install_packages=False)
current_process.start()
time.sleep(1)

channel.basic_consume(
    queue=queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()