import sqlite3

# 连接数据库，若路径下没有则直接创建
conn = sqlite3.connect("test.db")

# 获取游标
c = conn.cursor()

# 创建数据表
#
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real
#         );
#
#
# sql1 = '''
#     insert into company (id,name,age,address,salary)
#         values(2,"李四","30","重庆","15000");
#
# '''
# sql2 = '''
#     insert into company (id,name,age,address,salary)
#         values(3,"王五","26","上海","5000");
#
# '''

sql = '''
    select id,name,age,address,salary from company
'''

# 执行
info = c.execute(sql)
# c.execute(sql2)

# (1, '张三', 32, '成都', 8000.0) <class 'tuple'>
for row in info:
    print(row,type(row))

# 提交数据库操作,查询则不用提交
# conn.commit()

# 关闭数据库连接
conn.close()