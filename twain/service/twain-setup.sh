#!/bin/bash
cp /twain/service/twain.service /lib/systemd/system/

chmod 644 /lib/systemd/system/twain.service

systemctl daemon-reload

systemctl enable twain.service

systemctl start twain.service
