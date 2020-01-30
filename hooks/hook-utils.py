from PyInstaller.hooks.hookutils import collect_submodules

hiddenimports_pika = collect_submodules('pika')
hiddenimports_requests = collect_submodules('requests')
hiddenimports_psutils = collect_submodules('psutil')

hiddenimports = hiddenimports_pika + hiddenimports_requests + hiddenimports_psutils