# YACS: Yet Another Configuration System

YACS is a very lightweight (the core implementation is no more than 250 lines)
yet sufficiently powerful Python configuration utility, requiring no 3rd-party package. I used it in
my several machine-learning/deep-learning projects, and it worked well and reliably.


# Installation

Since YACS is so simple, we recommend just copying the single [`yacs/config.py`](yacs/config.py) file to
your project. That is it. No tedious package installation is needed.

> Note: if wish to load/dump configurations from/to a yaml file, [PyYAML](https://pypi.org/project/PyYAML/) is required.


# Usages

For a regular-scale project, developers usually use a configuration file to define some default
behaviors of their programs.

Take a machine learning project as example, the configuration file defines under which 
mode the
experiment is running, use which model to run the task, and how the data is organized:

<a name="default_config"></a>

```yaml
# default_config.yaml
mode: train
model:
  backbone: vgg19
data:
  source: dir/to/data/*.jpg
  batch_size: 32
```

## Initialization

YACS uses a [`Config`](yacs/config.py#15) object to implement all necessary interaction and
manipulation to the configurations.

Let's start by loading these configurations from the yaml and printing them:

```python
from yacs.config import Config

cfg = Config('default_config.yaml')
cfg.print()
```

In the terminal, it shows something like this:

```shell
mode:               train
model:
  backbone:         vgg19
data:
  source:           dir/to/data/*.jpg
  batch_size:       32
```

## Access attributes

`Config` is actually a child class of the built-in `dict`, so we can access its attributes by keys,
or more compactly, in a dotted-dict way (more recommended):

```python
mode = cfg['mode']  # 'train'
mode = cfg.mode     # 'train'
```

For inputs with nested structures, `Config` objects will be recursively created, so you can access
its attributes in a recursive way:

```python
bs = cfg.data.batch_size  # 32
```

## Modify attributes

For safety reason, attributes are not allowed to be modified nor deleted by default:

```python
cfg.data.batch_size = 512  # AttributeError: attempted to modify an immutable Config
```

Instead, users have to use the `unfreeze()` context manager to make any modification:

```python
with cfg.unfreeze():
    cfg.data.batch_size = 512
```

Similarly, to add a new attribute or a child object to the current `Config`
object:

```python
with cfg.unfreeze():
    cfg.training = Config({'optimizer': 'Adam'})
cfg.print()
```

```shell
mode:               train
model:
  backbone:         vgg19
data:
  source:           dir/to/data/*.jpg
  batch_size:       512
training:
  optimizer:        Adam
```

Here, by typing `cfg.training = Config({'optimizer': 'Adam'})`, we instantiate a temporary 
`Config` object from a dict and add it as the `training` attribute to `cfg`.

## Merge

For a machine learning project, hyper-parameters or other setups vary case-by-case for each 
training or inference, so in addition to the default configurations, developers often require a 
temporary config file at hand, by which to override parts of the default configurations.

Assume we are now using another yaml to store these user-specific configurations:

```yaml
# user_config.yaml
model:
  backbone: resnet50
data:
  batch_size: 128
```

Now we can use `merge()` to merge these temporary configurations into the default ones, 
overriding the duplicates while keeping others unchanged:

```python
cfg = Config('default_config.yaml')
cfg.merge('user_config.yaml')
cfg.print()
```

```shell
mode:               train
model:
  backbone:         resnet50
data:
  source:           dir/to/data/*.jpg
  batch_size:       128
```

If the user-specific configurations contain attributes that are not in `cfg`, use 
`allow_new_attr=True` to explicitly claim that you wish to add new attributes:

```python
cfg.merge('user_config.yaml', allow_new_attr=True)
```

Let's see another example. Assume there is a `optimizer` attribute in the default yaml, in which 
we assign three children attributes `optimizer_name`, `lr`, and `momentum`:

```yaml
# sgd.yaml
mode: train
optimizer:
  optimizer_name: SGD
  lr: 0.01
  momentum: 0.9
```

Now in one experiment, we wish to replace SGD with Adam optimizer, so we can create a 
temporary yaml and merge it like this:

```yaml
# adam.yaml
optimizer:
  optimizer_name: Adam
  lr: 1.0E-5
```

```python
cfg = Config('sgd.yaml')
cfg.merge('adam.yaml')
cfg.print()
```

```shell
mode:               train
optimizer:
  optimizer_name:   Adam
  lr:               1e-05
  momentum:         0.9
```

Note that by default, the non-conflict attributes will be kept unchanged after merging, so in this case, `cfg.optimizer.momentum` attribute is still kept after merging, which is not our intention because Adam does not  require a `momentum` parameter.

In such scenarios that we would like to completely replace an attribute (`cfg.optmizer` 
here) and all its children attributes, use `keep_existed_attr=False` to keep your `cfg` neater:

```python
cfg = Config('sgd.yaml')
adam_cfg = Config('adam.yaml')
cfg.optimizer.merge(adam_cfg.optimizer, keep_existed_attr=False)
cfg.print()
```

```shell
mode:               train
optimizer:
  optimizer_name:   Adam
  lr:               1e-05
```

Now `cfg.optimizer.momentum` is gone because we explicitly ask not to keep those old and 
non-conflict 
attributes.

## Work with `argparse`

One appealing feature in [Hydra](https://github.com/facebookresearch/hydra) is that it allows 
users to control their programs' running options in the terminal, with the help of `argparse` 
package.

YACS also allows initializing or merging configurations from the command line.

`Config`'s `to_parser()` method offers a way to automatically generate an `argparse.ArgumentParser` 
object, whose arguments are converted from the key-attribute pairs. For a nested attribute, keys 
from hierarchies are concatenated into an argument, with `.` as separators.

Let's use [`default_config.yaml`](#default_config) as example again. Instead of explicitly 
creating an argument parser such as

```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train')
    parser.add_argument('--model.backbone', type=str, default='vgg19')
    parser.add_argument('--data.source', type=str, default='dir/to/data/*.jpg')
    parser.add_argument('--data.batch_size', type=int, default=32)
    return parser
```

we do this in an easier way:

```python
cfg = Config('default_config.yaml')
parser = cfg.to_parser()
```

Then you can put this parser to the entry of your program, to accept arguments from the terminal,
and then merge the parsed arguments (will be stored in an `argparse.Namespace` object) back into 
the 
`cfg`:

```python
# main.py
from yacs.config import Config

def main(cfg):
    cfg.print()
    # core program ...

if __name__ == '__main__':
    cfg = Config('default_config.yaml')
    parser = cfg.to_parser()
    cfg.merge(parser.parse_args())  # merge from an argparse.Namespace object
    
    main(cfg)
```

Finally we run `main.py` in the terminal with some extra arguments:

```shell
$ python main.py --model.backbone resnet50 --data.batch_size 1024
```

and get results:

```shell
mode:               train
model:
  backbone:         resnet50
data:
  source:           dir/to/data/*.jpg
  batch_size:       1024
```


## Dump & Conversion

`Config` provides following method to dump or convert your configurations to other datatype: 

* `dump(yaml_path)` dumps the configurations into a yaml file. 

* `clone()` creates a deep copy the current `Config` object. 
  
* `to_dict()` converts to a regular nested dict.

## More Usage Examples

See [`examples`](examples) directory for more practical usages.

# Acknowledgement

YACS shares part of designs from [rbgirshick's yacs](https://github.com/rbgirshick/yacs)
and [OmegaConf](https://github.com/omry/omegaconf).

# License

Copyright 2021 Qiu Jueqin.

Licensed under [MIT](http://opensource.org/licenses/MIT).