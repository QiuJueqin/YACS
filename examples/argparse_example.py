# File: argparse_example.py
# Description:
# Created: 2021/6/23 22:36
# Author: Qiu Jueqin (qiujueqin@gmail.com)
# Note: run this script from terminal to print help messages:
# python argparse_example.py --help


import init_path
from yacs.config import Config


def main(cfg):
    cfg.print()
    # core program ...


if __name__ == '__main__':
    cfg = Config('default_config.yaml')
    parser = cfg.to_parser()
    cfg.merge(parser.parse_args())  # merge from an argparse.Namespace object

    main(cfg)
