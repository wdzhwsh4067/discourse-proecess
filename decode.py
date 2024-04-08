import codecs

with codecs.open('gbk_file.txt', 'r', 'gbk') as gbk_file:
    with codecs.open('utf8_file.txt', 'w', 'utf-8') as utf8_file:
        for line in gbk_file:
            utf8_file.write(line)