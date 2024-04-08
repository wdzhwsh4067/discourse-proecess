# -*- coding: utf-8 -*-
import re
import json
import pandas as pd
import requests
import codecs
import datetime
import random
import math
from mysql import insert_data
import os
import time
def random_date():
    now = datetime.datetime.now()
    one_year_ago = now - datetime.timedelta(days=365)
    random_time = one_year_ago + datetime.timedelta(seconds=random.randint(0, 31536000))
    return random_time.strftime('%Y-%m-%d')


def article_suggest_text(title, author, chinese_count, reading_time):
    text = f"""
[quote]
||||
| --- | --- | --- |
| :gift_heart:|**1.标题**|**{title}** |
| :ok_woman:|**2.作者**|**{author}** |
|:bento:|**3.字数**|**{chinese_count}**|
|:open_book:|**4.时间**|**{reading_time}**|
[/quote]

[quote]
||
| --- | 
| :wedding:: **欢迎来到论坛！**|
| 这是一个专注于 **######主题**的论坛，我们欢迎所有对 ######感兴趣的人。|
|在这里，你可以分享你的**经验、观点和技巧** :grin: ，也可以获得有关 ######的**资源和信息**:pig:。我们希望这个论坛可以成为一个友好和支持性的社区，让每个人都能够找到他们所需要的信息和资源 :smirk_cat:，并与其他 ######爱好者建立**联系和友谊**。 |
|<kbd> [:ok_woman:&nbsp;**Chat**](https://@@@@@@.com/chat) </kbd> <kbd> [:bulb:&nbsp;**Feature**](https://@@@@@@.com/categories)</kbd><kbd> [:robot:&nbsp;**Support**](https://@@@@@@.com) </kbd>  |
[/quote]
"""
    return str(text)


def count_chinese_characters(text):
    pattern = re.compile('[\u4e00-\u9fa5]')  # 匹配中文字符集
    chinese_characters = re.findall(pattern, text)  # 查找所有匹配的中文字符
    count = len(chinese_characters)  # 统计中文字符数量
    return round(count / 10000, 3 - int(math.floor(math.log10(abs(count / 10000)))) if count / 10000 != 0 else 3)

# 导入emoji
def emoji_characters():
    emoji_codes = [':innocent:', ':rofl:', ':kissing_heart:', ':laughing:', ':robot:', ':smiley_cat:', 
                   ':speak_no_evil:', ':heart_decoration:', ':two_hearts:', ':revolving_hearts:', ':gift_heart:', 
                   ':heart:', ':supervillain:', ':man_wearing_turban:', ':woman_with_turban:', ':female_detective:', 
                   ':man_detective:', ':ninja:', ':guardswoman:', ':man_guard:', ':singer:', ':hedgehog:', 
                   ':dragon:', ':swan:', ':swan:', ':snake:', ':blowfish:', ':cricket:', ':spider:', ':leafy_green:', 
                   ':baguette_bread:', ':bell_pepper:', ':strawberry:', ':reminder_ribbon:', ':firecracker:', 
                   ':ribbon:', ':sparkler:', ':jack_o_lantern:', ':flags:', ':blue_book:', ':books:', ':pick:', 
                   ':calendar:', ':shield:', ':nut_and_bolt:', ':toolbox:', ':crossed_flags:', ':yellow_square:', 
                   ':u6307:', ':id:', ':heavy_check_mark:', ':1234:', ':curly_loop:', ':heavy_check_mark:', 
                   ':keycap_ten:', ':cityscape:', ':post_office:', ':desert_island:', ':earth_asia:', 
                   ':earth_americas:', ':factory:', ':european_castle:', ':tokyo_tower:', ':church:', ':hotel:', 
                   ':smiling_face:', ':kissing_closed_eyes:', ':kissing_smiling_eyes:', ':star_struck:', ':heart_eyes:', 
                   ':smiling_face_with_three_hearts:', ':mountain_biking_man:', ':man_mountain_biking:', ':mountain_biking_woman:', 
                   ':whale:', ':whale2:', ':dolphin:', ':microbe:', ':pig:', ':cow:', ':cactus:', ':palm_tree:', 
                   ':deciduous_tree:', ':four_leaf_clover:', ':mango:', ':apple:', ':peach:', ':crab:', ':lobster:', 
                   ':shrimp:', ':squid:', ':toolbox:', ':pushpin:', ':paperclip:', ':round_pushpin:', ':u5272:', 
                   ':u7121:', ':u7981:', ':u7533:', ':u5408:', ':u7a7a:', ':congratulations:', ':secret:', ':u55b6:', 
                   ':u6e80:', ':red_circle:', ':o:']
    
    # Select a random emoji code from the list
    random_emoji_code = random.choice(emoji_codes)
    
    # # Insert the random emoji code into the given text
    # index = random.randint(0, len(text))
    return random_emoji_code

def read_file(file_path):
    text = ''  # 定义一个空字符串变量，用于存储文件内容
    with codecs.open(file_path, 'r', 'utf-8') as gbk_file:
        for line in gbk_file:
            line = line.replace('    ', '  ')
            line = line.replace('   ', ' ')
            text += line
    return text

def post_article_to_forum(title, text):
    url = "https://@@@@@@.com/posts"
    headers = {'Content-Type': 'application/json',
               'Api-Key': 'db23359b5a04a35ea1debf0c3425a3adb7c6fe827e0957d0b3252eb1f76411ff',
               'Api-Username': 'root',
               'Cookie': '__profilin=p%3Dt%2Ca%3Dac69a65d3e5b464dd7dbe779eb0a55c1%7Cea4004c156480de820009c2ce75fd9fb'}
    paragraphs = []
    max_chars = 10000
    # Split text into paragraphs of roughly 5000 characters each
    print("##start find place to clip")
    # 这里是对文本进行分段，能否使用多种分段依据？换行符，句号，或者逗号
    while len(text) > max_chars:
        print("@@start find place to clip")
        split_index = text.rfind("\n", 0, max_chars)
        if split_index == -1:
            split_index = max_chars
            paragraphs.append(text[:split_index])
            text = ""
            print("@@split_index == -1")
        else:
            paragraphs.append(text[:split_index])
            text = text[split_index:]
            print("@@split_index != -1")
        # 判断是否超过 300 段
        if len(paragraphs) >= 300:
            paragraphs[-1] += text
            break
    print("@@text len")
    paragraphs.append(text)
    print("@@text append")
    # Post each paragraph as a separate article
    for i, paragraph in enumerate(paragraphs):
        if i==0:
            payload = {
                "title": title,
                "raw": paragraph,
                "category": "5",
                "created_at": random_date(),
            }
            # print(payload)
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            # print(response.json())
            topic_id = response.json()['topic_id']
            print('话题头创建成功')
            # created_at = response.json()['created_at']
        else:
            time.sleep(0.5)
            payload = {
                "raw": paragraph,
                "topic_id": topic_id,
                # "created_at":  (created_at + datetime.timedelta(seconds=1)).isoformat(),
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            
        if response.status_code != 200:
            time.sleep(1)
            print("error!!!",title)
        else:
            print("success")

            
def main():
    
    sheets = ['baby', 'valley', 'rose', 'sky', 'purple']
    directories = ['/root/Sp小说/baby', '/root/Sp小说/valley', '/root/Sp小说/rose', '/root/Sp小说/sky', '/root/Sp小说/purple']
    success_files = {'baby': 'baby_success.txt', 'valley': 'valley_success.txt', 'rose': 'rose_success.txt', 'sky': 'sky_success.txt', 'purple': 'purple_success.txt'}

    for sheet, directory in zip(sheets, directories):
        try:
            df = pd.read_excel('/root/bbsCode/data.xlsx', sheet_name=sheet)
            print(f"##loaded {sheet} sheet")
        except FileNotFoundError:
            print(f"Error: File not found for {sheet} sheet")
            continue

        success_file = success_files.get(sheet)
        if success_file:
            with open(success_file, 'a') as f:
                for index, row in df.iterrows():
                    if sheet == "baby" and str(row['mrcode']) in open('baby_success.txt').read():
                        print("@@already posted,pass "+str(row['mrcode'])+" in "+sheet)
                        continue
                    if sheet == "valley" and str(row['mrcode']) in open('valley_success.txt').read():
                        print("@@already posted,pass "+str(row['mrcode'])+" in "+sheet)
                        continue
                    if sheet == "rose" and str(row['mrcode']) in open('rose_success.txt').read():
                        print("@@already posted,pass "+str(row['mrcode'])+" in "+sheet)
                        continue
                    if sheet == "sky" and str(row['mrcode']) in open('sky_success.txt').read():
                        print("@@already posted,pass "+str(row['mrcode'])+" in "+sheet)
                        continue
                    if sheet == "purple" and str(row['mrcode']) in open('purple_success.txt').read():
                        print("@@already posted,pass "+str(row['mrcode'])+" in "+sheet)
                        continue
                    try:
                        text = read_file(os.path.join(directory, f"{row['mrcode']}.txt"))
                        print(f"##processed text for {sheet} sheet")
                        chinese_count = count_chinese_characters(text)
                        print("##got count")
                        reading_time = round(chinese_count * 10000 / 250 / 60,
                                            3 - int(math.floor(math.log10(abs(chinese_count * 10000 / 250 / 60))))
                                            if chinese_count * 10000 / 250 / 60 != 0 else 3)
                        print("##got time")
                        if chinese_count < 1:
                            chinese_count = int(chinese_count * 10000)
                            reading_time = round(reading_time * 60, 3)
                            bbs_title = emoji_characters() + f"{row['title']} || {chinese_count}字"
                            abstract = article_suggest_text(row['title'], row['author'], str(chinese_count) + "字",
                                                            str(reading_time) + "分钟")
                        else:
                            bbs_title = emoji_characters() + f"{row['title']} || {chinese_count:.1f}万字"
                            abstract = article_suggest_text(row['title'], row['author'], str(chinese_count) + "万字",
                                                            str(reading_time) + "小时")
                        bbs_md_text = abstract + text
                        insert_data(row['title'], row['author'], random_date(), chinese_count / 1000, reading_time / 60,
                                    text, str(bbs_title), abstract)
                        print(f"##imported database for {sheet} sheet")
                        post_article_to_forum(bbs_title, bbs_md_text)
                        with open(success_file, 'a') as sf:
                            sf.write(f"{row['mrcode']}\n")
                        print(f"##|||||post completed for {sheet} sheet")
                    except FileNotFoundError:
                        print(f"Error: File not found for mrcode: {row['mrcode']} in {sheet} sheet")
                        with open('error.txt', 'a') as ef:
                            ef.write(f"Error: {str(e)} for mrcode: {row['mrcode']} in {sheet} sheet\n")
                    except PermissionError:
                        print(f"Error: Permission denied for mrcode: {row['mrcode']} in {sheet} sheet")
                        with open('error.txt', 'a') as ef:
                            ef.write(f"Error: {str(e)} for mrcode: {row['mrcode']} in {sheet} sheet\n")
                    except Exception as e:
                        print(f"Error: {str(e)} for mrcode: {row['mrcode']} in {sheet} sheet")
                        with open('error.txt', 'a') as ef:
                            ef.write(f"Error: {str(e)} for mrcode: {row['mrcode']} in {sheet} sheet\n")
        else:
            print(f"Error: Success file not found for {sheet} sheet")



if __name__ == '__main__':
    main()