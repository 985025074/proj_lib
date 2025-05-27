# mock 功能 通过monkeypatch实现：

# fixture  夹具：
1. 声明
```py
@pytest.fixture
def func():
    ...
# 使用只需要参数同名即可
```
注解：每个夹具单独的。不会相互打扰。
但是对于重复的请求。见下，会缓存
```py
# contents of test_append.py
import pytest


# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order():
    return []


# Act
@pytest.fixture
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
```
2. 夹具重要参数 autouse 自动使用

3. scope 参数：
 scope 的可能值为： function 、 class 、 module 、 package 或 session 。

- function: the default scope, the fixture is destroyed at the end of the test. 单个测试函数范围
4. conftest.py
    这个文件内的fixture 是共享的
     puts the fixture function into a separate conftest.py file so that tests from multiple test modules in the directory can access the fixture function
5. 清理功能 fixture的清理；使用yield.注意顺序 从后往前
```py
from emaillib import Email, MailAdminClient

import pytest


@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    user.clear_mailbox()
    mail_admin.delete_user(user)


def test_email_received(sending_user, receiving_user):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    assert email in receiving_user.inbox
```