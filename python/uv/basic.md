# python 安装管理：
- uv python list: View available Python versions.
- uv python install: Install Python versions.
- uv python find: Find an installed Python version.
- uv python pin: Pin the current project to use a specific Python  version.
- uv python uninstall: Uninstall a Python version.

## 安装特定版本
uv python install 3.11  
**uv 会自动下载python，调用一些命令时候，如果没有对应python，会自动下载**

# 脚本运行
uv run *.py （uv run --script ...py）
- 在项目中运行时候 会携带依赖项 （--no-project ignore）
- uv run --python 3.10 --scirpt (限制运行的版本)
## 创建脚本
uv init --script name.py --python 指定python 脚本版本（版本将嵌入python文件）
## 添加依赖项
uv add --script example.py 'requests<3' 'rich'
## 锁定依赖项：
uv lock --script file  
意思是锁定依赖项，从而以后依赖这些固定url

# 工具
uvx (==uv tool run)  
如果您在项目中运行工具，并且该工具需要安装您的项目，例如，当使用 pytest 或 mypy 时，您将需要使用 uv run 而不是 uvx 。否则，该工具将在与项目隔离的虚拟环境中运行。

uv tool install (持久化安装)  
uv tool upgrade （更新）  

# 项目
uv init projectname(mkdir)
  
uv init (in current dir)   
第一次 运行后，会产生venv + lock 文件

## 项目的依赖解决：
- uv add 'requests==2.31.0'
或者直接添加，不带版本
- uv remove 删除依赖项  
- Add all dependencies from `requirements.txt`.
uv add -r requirements.txt -c constraints.txt
- uv lock --upgrade-package requests （兼容的升级）
## 项目运行：
uv run 
uv run -- (在虚拟环境中运行的命令(直接传参好像也行))
uv run toolname 

### 上述过程也可以手动
手动同步

uv sync
source .venv/bin/activate
flask run -p 3000
python example.py

不建议手动修改项目环境，例如使用 uv pip install 。对于项目依赖项，请使用 uv add 将包添加到环境中。对于一次性需求，请使用 uvx 或 uv run --with 。