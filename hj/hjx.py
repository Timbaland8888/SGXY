#!/usr/bin/evn python
# -*- encoding:utf-8 -*-
# function: connect exsi server api  for restart vm
# date:2020-04-09
# Author:Timbaland
#version:1.1
#update:2020-05-28
# import os
# os.system('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://172.16.56.50:8083/')
import subprocess
cmd = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://172.16.56.50:8083/'
CREATE_NO_WINDOW = 0x08000000
subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)