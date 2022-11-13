# DI-toolkit


[![PyPI](https://img.shields.io/pypi/v/DI-toolkit)](https://pypi.org/project/DI-toolkit/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/DI-toolkit)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/82e5c38227081da9d25e729e5bd3b5b8/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/82e5c38227081da9d25e729e5bd3b5b8/raw/comments.json)

[![Docs Deploy](https://github.com/opendilab/DI-toolkit/workflows/Docs%20Deploy/badge.svg)](https://github.com/opendilab/DI-toolkit/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/opendilab/DI-toolkit/workflows/Code%20Test/badge.svg)](https://github.com/opendilab/DI-toolkit/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/opendilab/DI-toolkit/workflows/Badge%20Creation/badge.svg)](https://github.com/opendilab/DI-toolkit/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/opendilab/DI-toolkit/workflows/Package%20Release/badge.svg)](https://github.com/opendilab/DI-toolkit/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/opendilab/DI-toolkit/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/opendilab/DI-toolkit)

[![GitHub stars](https://img.shields.io/github/stars/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/opendilab/DI-toolkit)
[![GitHub issues](https://img.shields.io/github/issues/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/pulls)
[![Contributors](https://img.shields.io/github/contributors/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/opendilab/DI-toolkit)](https://github.com/opendilab/DI-toolkit/blob/master/LICENSE)


A simple toolkit package for opendilab, including the following utilities:
  - `ditk.logging`, a easy-to-use logger system


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

## Quick Start

### Example of ditk.logging

Here is an example of logging.

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

`ditk.logging`has almost the same interface as native `logging` module. You can directly replace `import logging` in the code with `from ditk import logging`.

## Contributing

We appreciate all contributions to improve `DI-toolkit`, both logic and system designs. Please refer to CONTRIBUTING.md for more guides.


## License

`DI-toolkit` released under the Apache 2.0 license.
