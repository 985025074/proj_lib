# 子项目嵌套解决
## 法1:
https://stackoverflow.com/questions/75159453/specifying-local-relative-dependency-in-pyproject-toml

You can turn your file path from relative to absolute by using a $PROJECT_ROOT env var and injecting it into the path itself:
您可以使用 $PROJECT_ROOT 环境变量并将其注入路径本身，将文件路径从相对路径转换为绝对路径：

dependencies = [ 
   "lol @ file:///${PROJECT_ROOT}/libs/lol"
]
pdm or uv will inject this environment variable for you (pdm docs, uv PR). Otherwise, you'll need to assign it yourself. That can be done several ways but it depends on your project and is probably out of scope for this question.
pdm 或 uv 会为您注入此环境变量（ pdm docs ， uv PR ）。否则，您需要自行分配。这可以通过多种方式完成，但取决于您的项目，并且可能超出了本问题的讨论范围。
# 法 2
工作区 太麻烦了
https://docs.astral.sh/uv/concepts/projects/workspaces/#getting-started
子包太多了 在用这个吧