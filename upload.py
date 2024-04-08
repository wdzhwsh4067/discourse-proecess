import os
import pandas as pd
import math

def main():
    sheets = ['baby', 'valley', 'rose', 'sky', 'purple']
    directories = ['/root/Sp小说/baby', '/root/Sp小说/valley', '/root/Sp小说/rose', '/root/Sp小说/sky', '/root/Sp小说/purple']
    success_files = {'baby': 'baby_success.txt', 'valley': 'valley_success.txt', 'rose': 'rose_success.txt', 'sky': 'sky_success.txt', 'purple': 'purple_success.txt'}

    for sheet, directory in zip(sheets, directories):
        try:
            df = pd.read_excel('/root/Sp小说/Sp小说书目索引.xlsx', sheet_name=sheet)
            print(f"##loaded {sheet} sheet")
        except FileNotFoundError:
            print(f"Error: File not found for {sheet} sheet")
            continue

        success_file = success_files.get(sheet)
        if success_file:
            with open(success_file, 'a') as f:
                for index, row in df.iterrows():
                    if sheet == "baby" and row['mrcode'] in open('baby_success.txt').read():
                        continue
                    if sheet == "valley" and row['mrcode'] in open('valley_success.txt').read():
                        continue
                    if sheet == "rose" and row['mrcode'] in open('rose_success.txt').read():
                        continue
                    if sheet == "sky" and row['mrcode'] in open('sky_success.txt').read():
                        continue
                    if sheet == "purple" and row['mrcode'] in open('purple_success.txt').read():
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