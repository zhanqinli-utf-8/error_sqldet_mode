# error_sqldet_mode
手工有错误注入，sqlmap跑不出注入；
针对报错注入，对于嵌套的报错注入payload，如：1 and (SELECT user()=1 FROM (SELECT(updatexml(1,concat(0x7e,(select count(table_name) from information_schema.tables where table_schema=database()),0x7e),1)))YsCQ)&bid=%23
sqlmap并没有这类payload导致无法跑出注入，可利用该脚本将数据库的所有表跑出保存在本地；
对于waf的拦截可以参考string_to_hex（），这里只是将要跑的tablename或者columnname进行16进制编码来绕过waf,可以在此模板上进行修改，减少工作量；
此脚本，只是本人实在太懒了，不想动手因此今天工作写的脚本，从脚本的内容就可以看出，本人菜得扣脚（不要喷我），此脚本也只是针对新手师傅在脱库时，sqlmap无法使用的其中一种方法，能够给予启发。
