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
# Load default config from a yaml file.
default_config_path = './default_config.yaml'
cfg = Config(default_config_path)

_print(cfg, 'Default Config:')


# ========== Example 2 ==========
# Load user-specific config from another yaml file
# and override those attributes in default config.
user_config_path = './user_config.yaml'
cfg.merge(user_config_path, allow_new_attributes=True)

_print(cfg, 'User-Specific Config:')


# ========== Example 3 ==========
# Use context manager to modify some attributes.
with cfg.unfreeze():
    cfg.data.batch_size = 512
    cfg.data.subsets = ['mini_test']

_print(cfg, 'Config after on-spot modification:')


# ========== Example 4 ==========
# Use context manager to add new attributes.
with cfg.unfreeze():
    cfg.exp = Config()
    cfg.exp.total_epochs = 300

_print(cfg, 'Config with new attribute:')


# ========== Example 5 ==========
# Override some attributes from an dict.
# Note that when setting 'keep_existed_attributes' to False,
# original attributes in the source config will be removed if
# they are not in the new config. You can do this if requires
# to replace some parent field (here the whole cfg.lr_scheduler
# field)
lr_scheduler_config = {
    'lr_scheduler_name': 'gamma_decay',
    'decay_epochs': 50,
    'gamma': 0.5
}
cfg.lr_scheduler.merge(lr_scheduler_config,
                       allow_new_attributes=True,
                       keep_existed_attributes=False)

_print(cfg, 'Config after replacing cfg.lr_scheduler field:')


# ========== Example 6 ==========
# Remove some attributes.
with cfg.unfreeze():
    cfg.remove('optimizer')
    cfg.remove('lr_scheduler')

_print(cfg, 'Config after removing fields:')
