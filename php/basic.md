# 尝试使用小皮面板来进行配置。
官方的配置教程杂且多。

# php 格式
```html
<?php

code here

?>

```
# 也有glbal 关键字，但是很特殊，没有python 只能 
一定要加
# static 关键字。
同C
# 打印输出 echo 或者printf 不需要括号
echo可以打印多个

# HEREDOC:
多行字符串格式

```
<<<EOF
    <!-- 输入你要的内容 -->

EOF;
```
# 有true 和false
数据类型基本同python 一直
# class的定义方法：
```php
<?php
class Car
{
  var $color;
  function __construct($color="green") {
    $this->color = $color;
  }
  function what_color() {
    return $this->color;
  }
}
?>
```
# null



