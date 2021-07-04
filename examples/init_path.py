# File: init_path.py
# Description:
# Created: 2021/6/30 23:09
# Author: Qiu Jueqin (qiujueqin@gmail.com)


import sys
import os.path as op


examples_dir = op.dirname(op.abspath(__file__))
root_dir = op.abspath(op.join(examples_dir, '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)
