# mock now失败：
报错：cant replace method of immutable type
mock 内置的datetime.now失败 原因是这是C 实现的
解决：mock类
https://stackoverflow.com/questions/20503373/how-to-monkeypatch-pythons-datetime-datetime-now-with-py-test
注意这个stack下面一个评论，导入问题