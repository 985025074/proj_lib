# setup basic config:
```
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

```
# 配置文件三选一

This can be done in the same pyproject.toml file, or in a separated one: setup.cfg or setup.py [1].
```toml
[project]
name = "mypackage"
version = "0.0.1"
dependencies = [
    "requests",
    'importlib-metadata; python_version<"3.10"',
]
```
```py
from setuptools import setup

setup(
    name='mypackage',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.10"',
    ],
)

```

```
mypackage
├── pyproject.toml  # and/or setup.cfg/setup.py (depending on the configuration method)
|   # README.rst or README.md (a nice description of your package)
|   # LICENCE (properly chosen license information, e.g. MIT, BSD-3, GPL-3, MPL-2, etc...)
└── mypackage
    ├── __init__.py
    └── ... (other Python files)

```
python -m build 打包

# 不要直接运行setup.py;
It is important to remember, however, that running this file as a script (e.g. python setup.py sdist) is strongly discouraged, and that the majority of the command line interfaces are (or will be) deprecated (e.g. python setup.py install, python setup.py bdist_wininst, …).

# 包发现机制：
```
# ...
[tool.setuptools.packages]
find = {}  # Scan the project directory with the default parameters

# OR
[tool.setuptools.packages.find]
# All the following settings are optional:
where = ["src"]  # ["."] by default
include = ["mypackage*"]  # ["*"] by default
exclude = ["mypackage.tests*"]  # empty by default
namespaces = false  # true by default

```
setup有一些好的包发现机制：
https://setuptools.pypa.io/en/latest/userguide/quickstart.html#entry-points-and-automatic-script-creation



# CLI 入口:
```
[project.scripts]
cli-name = "mypkg.mymodule:some_func"
```
# dependency依靠：
```
[project]
# ...
dependencies = [
    "docutils",
    "requests <= 0.4",
]
# ...

```

# 额外数据文件，需要通过一定手段配置：
```py
[tool.setuptools]
include-package-data = true
# This is already the default behaviour if you are using
# pyproject.toml to configure your build.
# You can deactivate that with `include-package-data = false`
```
https://setuptools.pypa.io/en/latest/userguide/quickstart.html#entry-points-and-automatic-script-creation
# 快速使用安装
pip install --editable .
注意 setup.py是需要的，如果你是老版本的pip，详细查看文档


# 

