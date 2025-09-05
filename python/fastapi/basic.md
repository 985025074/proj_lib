很好的项目，文档很有趣，拓展了一知识。
# 使用async的情况。
- 要用await,那controller 要用 async def
- 如果不需要 那么就直接def
# 虚拟环境的实现机制：
核心，添加虚拟环境的python到path 环境变量的最前面。
# 运行
fastapi dev file  
使用uv:  
uv run  fastapi dev file
# 分路线写法：
```py
from fastapi import APIRouter
    
router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    # 假设这里是验证逻辑
    if username == "admin" and password == "123456":
        return {"message": "Login success!"}
    return {"message": "Invalid credentials"}



```
```py
from fastapi import FastAPI
from routers import login, record

app = FastAPI()

# 注册不同模块的路由
app.include_router(login.router)
app.include_router(record.router)

# 如果你想统一加前缀，例如 API 版本：
# app.include_router(login.router, prefix="/api/v1")
# app.include_router(record.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


```

# 核心骨架：
```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```
可以加入参数
## 参数获取：
```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```
注解：会自动根据类型注释转换type.
自带一些错误处理。
## 顺序是重要的。
## 使用enum 作为一些pre defiend value:
```py
from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

## 特别的，对于路径参数的获取：
```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```
# query:
当您声明不属于路径参数的其他函数参数时，它们会自动解释为“查询”参数
多次同名查询 请使用list，注意要有一个空的query 在annoated 里的
# post 请求获取：
```py
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```
注意是json 格式发送数据！
request 实验得知
# extra 验证：
annotated + query path+ body+ header

# 自定义验证：
```py
import random
from typing import Annotated

from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
```

# fastapi支持多个query 合并到一个pandatic的basemodel
也支持分解post请求的json正文