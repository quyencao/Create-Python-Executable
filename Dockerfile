FROM ubuntu:18.04
# FROM centos:8
# FROM debian
WORKDIR /twain
COPY dist/app /twain/
ENTRYPOINT [ "/twain/app" ]