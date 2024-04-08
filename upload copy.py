# -*- coding: utf-8 -*-
###
# python如何读取excel文件中的第名为baby的表，使用for循环输出列表头为title，mrcode，size，author的所有行
# pip install openpyxl -i https://mirrors.aliyun.com/pypi/simple/ 

import json
import pandas as pd
import requests
import codecs
import datetime
import random

# Object of type datetime is not JSON serializable
def random_date():
    # 获取当前时间
    now = datetime.datetime.now()

    # 生成一个距离当前时间一年内的随机时间
    one_year_ago = now - datetime.timedelta(days=365)
    random_time = one_year_ago + datetime.timedelta(seconds=random.randint(0, 31536000))
    return random_time.strftime('%Y-%m-%d')    
def article_suggest_text(a,b,c,d):
    text="""
[quote]
||||
| --- | --- | --- |
| :gift_heart:|**1.标题**|**{}** |
| :ok_woman:|**2.作者**|**{}** |
|:bento:|**3.字数**|**{}字**|
|:open_book:|**4.时间**|**{}分钟**|
[/quote]
[quote]
:wedding:: 欢迎来到 ###### 论坛！这是一个专注于 ###### 主题的论坛，我们欢迎所有对 ###### 感兴趣的人。在这里，你可以分享你的**经验、观点和技巧** :ok_woman:，也可以获得有关 ###### 的**资源和信息**。我们希望这个论坛可以成为一个友好和支持性的社区，让每个人都能够找到他们所需要的信息和资源 :smirk_cat:，并与其他 ###### 爱好者建立**联系和友谊**。 :family_woman_woman_girl_girl: 
<kbd> [:eyes:&nbsp;**Chat**](https://@@@@@@.com/chat) </kbd> <kbd> [:bulb:&nbsp;**Feature**](https://@@@@@@.com/categories)</kbd><kbd> [:question:&nbsp;**Support**](https://@@@@@@.com/categories) </kbd> <kbd> [:bug:&nbsp;**Bug**](https://@@@@@@.com/categories) </kbd> 
[/quote]""".format(a,b,c,d)
    return str(text)



url = "https://@@@@@@.com/posts"
df = pd.read_excel('data.xlsx', sheet_name='baby')
headers = {
        'Content-Type': 'application/json',
        'Api-Key': 'db23359b5a04a35ea1debf0c3425a3adb7c6fe827e0957d0b3252eb1f76411ff',
        'Api-Username': 'admin',
        'Cookie': '__profilin=p%3Dt%2Ca%3Dac69a65d3e5b464dd7dbe779eb0a55c1%7Cea4004c156480de820009c2ce75fd9fb'
    }

text = ''  # 定义一个空字符串变量，用于存储文件内容
with codecs.open('/Users/a1234/Documents/紫夜小天地/baby/b2632.0.txt', 'r', 'gbk') as gbk_file:

    for line in gbk_file:
        utf8_text = line.encode('utf-8').decode('utf-8')
        # 避免被识别为代码块 4个空格是代码块！！！
        utf8_text=utf8_text.replace('    ', '   ')
        text += utf8_text  # 将每一行的内容追加到text变量中
    with open('b2633.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    text1 = article_suggest_text('外面传来贾斯在跟山羊讲话的声音','雅阁麻辣小龙虾','180230','1980') +text
    payload = {
        "title": "test10",
        "raw": text1,
        "category": "4",
        "created_at": random_date(),
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if response.status_code!=200:
        print(response.text)
    else:
        print(response)




# for index, row in df.iterrows():
#     try:
#         text = ''  # 定义一个空字符串变量，用于存储文件内容
#         with codecs.open('/Users/a1234/Documents/紫夜小天地/baby/b{}.0.txt'.format(row['mrcode']), 'r', 'gbk') as gbk_file:
#             for line in gbk_file:
#                 utf8_text = line.encode('utf-8').decode('utf-8')
#                 # 避免被识别为代码块 4个空格是代码块！！！
#                 utf8_text=utf8_text.replace('    ', '   ')
#                 text += utf8_text  # 将每一行的内容追加到text变量中
#         payload = {
#             "title": row['title'],
#             "raw": text,
#             "category": "4",
#             "created_at": random_date(),
#         }
#         response = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
#         if response.status_code!=200:
#             print(response.text)
#         else:
#             print(response)
#     except Exception as e:
#         print(e)