import random
import mysql.connector

# 连接到MySQL数据库
cnx = mysql.connector.connect(user='root', password='qwe123123',
                              host='localhost',
                              database='articleDB')

cursor = cnx.cursor()

# 生成并插入数据
for i in range(10002, 20001):
    # 随机生成经纬度
    lon = 121.47 + random.random() * 0.03
    lat = 31.23 + random.random() * 0.03

    # 创建SQL语句
    query = ("INSERT INTO `user_location` (`user_id`, `location`) "
             "VALUES (%s, ST_PointFromText('POINT(%s %s)'))")

    # 执行SQL语句
    cursor.execute(query, (i, lon, lat))

# 提交事务
cnx.commit()

# 关闭连接
cursor.close()
cnx.close()