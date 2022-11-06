# DI-toolkit


[![pipeline status](https://gitlab.bj.sensetime.com/open-XLab/cell/di-toolkit/badges/main/pipeline.svg)](https://gitlab.bj.sensetime.com/open-XLab/cell/di-toolkit/-/commits/main)
[![coverage report](https://gitlab.bj.sensetime.com/open-XLab/cell/di-toolkit/badges/main/coverage.svg)](https://gitlab.bj.sensetime.com/open-XLab/cell/di-toolkit/-/commits/main)

A simple toolkit packages:
  - logger
  - hpo: automatic hyper-parameter tuning
  - scheduler: automatic task resource scheduler


## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install DI-toolkit
```

Or install from latest source code as follows:
```shell
git clone https://gitlab.bj.sensetime.com/open-XLab/cell/di-toolkit.git
cd di-toolkit
pip install . --user
```

## Quick Start for HPO

Here is a simple example:

```python
from ditk import logging

if __name__ == '__main__':
    logging.try_init_root(logging.INFO)
    logging.info('This is info')
    logging.warning('This is warning with integer 233')
    logging.error('This is a error with string \'233\'.')

    try:
        _ = 1 / 0
    except ZeroDivisionError as err:
        logging.exception(err)

```

## Contributing

We appreciate all contributions to improve `DI-toolkit`, both logic and system designs. Please refer to CONTRIBUTING.md for more guides.


## License

`DI-toolkit` released under the Apache 2.0 license.
