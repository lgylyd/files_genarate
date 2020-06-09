#!/usr/bin/env python
# coding:utf-8
# author:YD
# time:2020/6/5

import os
import shutil

dir=os.path.dirname(os.path.abspath(__file__))
os.system(" pyinstaller -F -w %s//postman_gui.py "%dir)
shutil.copy("%s//postman_template.py"%dir,"%s//dist//postman_template.py"%dir)
