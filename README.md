# YACS: Yet Another Configuration System


## Introduction

YACS is a very lightweight (core implementation is no more than 200 lines) yet sufficiently powerful configuration utility, requiring no 3rd-party package<sup>*</sup>. I used it in my several machine-learning/deep-learning projects, and it worked well and reliably.

> <sup>*</sup> If wish to load/dump configuration from/to a yaml file, [PyYAML](https://pypi.org/project/PyYAML/) is required.


## Installation

Since YACS is so simple, I recommend just copying the single file [`config.py`](yacs/config.py) to any location in your project. 

That is it. No tedious package installation is needed.


## Usage

See [`examples/main.py`](examples/main.py) for some practical usage.


## Acknowledgement

YACS shares part of designs from [rbgirshick's yacs](https://github.com/rbgirshick/yacs) and [OmegaConf](https://github.com/omry/omegaconf).


## License

Copyright 2020 Qiu Jueqin

Licensed under [MIT](http://opensource.org/licenses/MIT).