# File: examples.py
# Description: YACS usage examples
# Created: 2021/6/16 21:41
# Author: Qiu Jueqin (qiujueqin@gmail.com)


from yacs import Config


def _print(config, title):
    print(title)
    print('-' * 42)
    config.print()
    print('-' * 42 + '\n')


# Load default config from a yaml.
cfg = Config('./default_config.yaml')
_print(cfg, 'Example 1: Load default config:')


# Load user-specific configs from another yaml and override those attributes
# in default cfg.
cfg.merge('./user_config.yaml')
_print(cfg, 'Example 2: Load user-specific config and merge:')


# Use context manager to modify some attributes.
with cfg.unfreeze():
    cfg.model.backbone = 'resnet101'
    cfg.data.batch_size = 1024
_print(cfg, 'Example 3: After on-spot modification:')


# Use context manager to add new attributes.
with cfg.unfreeze():
    cfg.model.head = 'rpn'
    cfg.optimizer = Config({'name': 'SGD', 'lr': 0.01, 'momentum': 0.9})
_print(cfg, 'Example 4: After adding new attributes:')


# Override some attributes from an dict. Note that when setting
# `keep_existed_attr` to False, original attributes in the source config will
# be removed if they are not in the new config. This feature will be helpful
# if requires to completely replace a nested attribute
cfg.optimizer.merge({'name': 'Adam', 'lr': 1E-5}, keep_existed_attr=False)
_print(cfg, 'Example 5: After replacing cfg.optimizer:')  # 'momentum' is gone


# Remove some attributes/nodes.
with cfg.unfreeze():
    cfg.remove('optimizer')
    cfg.model.remove('head')
_print(cfg, 'Example 6: After removing attributes:')
