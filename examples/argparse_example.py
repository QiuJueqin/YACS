# File: argparse_example.py
# Description:
# Created: 2021/6/23 22:36
# Author: QiuJueqin (qiujueqin@gmail.com)


import sys
import os.path as op
import argparse


examples_dir = op.dirname(op.abspath(__file__))
root_dir = op.abspath(op.join(examples_dir, '..'))
sys.path.append(root_dir)


from yacs.config import Config
from main import _print


def create_args(command_line=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['train', 'eval', 'test'], default='train')
    return parser.parse_args(command_line)


if __name__ == '__main__':
    cfg = Config('default_config.yaml')
    _print(cfg, title='Before merging argparse namespace:')

    args = create_args()  # an argparse.Namespace object
    cfg.merge(args)
    _print(cfg, title='After merging argparse namespace:')
