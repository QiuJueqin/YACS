# File: main.py
# Description: YACS usage examples
# Created: 2021/6/16 21:41
# Author: QiuJueqin (qiujueqin@gmail.com)


from yacs.config import Config


def _print(config, title):
    print(title)
    print('-' * 40)
    config.print()
    print('\n')


# ========== Example 1 ==========
# Load default config from a yaml.
cfg = Config('./default_config.yaml')
_print(cfg, 'Default config:')


# ========== Example 2 ==========
# Load user-specific configs from another yaml and override those attributes in default cfg.
cfg.merge('./user_config.yaml')
_print(cfg, 'User-specific config:')


# ========== Example 3 ==========
# Use context manager to modify some attributes.
with cfg.unfreeze():
    cfg.model.backbone = 'resnet101'
    cfg.data.batch_size = 1024

_print(cfg, 'Config after on-spot modification:')


# ========== Example 4 ==========
# Use context manager to add new attributes.
with cfg.unfreeze():
    cfg.model.head = 'rpn'
    cfg.exp = Config({'epochs': 500})  # add a new node ('exp') and leaf attribute ('epochs')

_print(cfg, 'Config with new attributes and nodes:')


# ========== Example 5 ==========
# Override some attributes from an dict.  Note that when setting 'keep_existed_attributes' to
# False, original attributes in the source config will be removed if they are not in the new config.
# You can do this if requires to replace a node (here the whole cfg.train node) instead of adding
# attributes to it.
train_config = {'optimizer': 'Adam', 'lr': 1E-5}
cfg.train.merge(train_config,
                allow_new_attributes=True,
                keep_existed_attributes=False)

# Attribute 'momentum' now is gone since the new 'train' node doesn't contain it
_print(cfg, 'Config after replacing cfg.train node:')


# ========== Example 6 ==========
# Remove some attributes/nodes.
with cfg.unfreeze():
    cfg.remove('data')
    cfg.remove('exp')
    cfg.model.remove('head')

_print(cfg, 'Config after removing attributes and nodes:')
