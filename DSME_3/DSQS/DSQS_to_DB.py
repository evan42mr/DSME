# db upload version
# schema pos-title-par_text-page-file_name
import re
import mysql.connector as mariadb
import json

with open('title_words.json') as f:
    title_dict = json.loads(f.read())


def stop_words(line):
    stopwords = title_dict['words']
    querywords = line.split()
    resultwords = [word for word in querywords if word not in stopwords]
    result = ' '.join(resultwords)
    return result


def check_spaces(s):
    tokens = re.findall('\s+', s)

    for i in range(0, len(tokens)):
        if len(tokens[i]) > 2:
            return True
    return False


def check_special_words(line):
    check_lst = title_dict['words']
    for item in check_lst:
        if item in line:
            return True
    return False


def print_text(text):
    text.pop()
    text_lines = ""
    for i in text:
        text_lines += ' ' + i
    #         text_lines += ' ' + i.strip()
    return text_lines


def check_roman_chapters(line):
    check_lst = ['Ⅰ.', 'Ⅱ.', 'Ⅲ.', 'Ⅳ.']
    for item in check_lst:
        if item in line:
            return True
    return False


def line_cutting(line):
    line = line.lstrip()
    words = line.split()
    tokens = re.findall('\s+', line)
    spaces = []
    new_line = ''
    for i in range(0, len(tokens)):
        spaces.append(len(tokens[i]))

    for i, word in enumerate(words):
        if len(tokens[i]) < 9:
            new_line += word + tokens[i]
        else:
            new_line += word
            break
    return new_line


# FILE_NAME = "DSQS-2016.txt"
FILE_NAME = "2019_DSQS_English.txt"
# FILE_NAME = "2019_DSQS_.txt" # Korean
 
table_name = "dsqs"
file_name_without_extension = "DSQS-2016"
text = []
pos = ""
title = ""
page_cnt = 1
part = ""
section = ""
temp_part = ""
temp_section = ""
partIII_titles = title_dict['partIII_titles']
partIII_text = ""

mydb = mariadb.connect(
    host="192.168.0.230",
    user="dev",
    passwd="424242",
    database="dsme_phase3"
)

with open(FILE_NAME) as f:
    for i, line in enumerate(f):

        if line and line[0] == '\x0c':
            page_cnt += 1

        if line.strip() and line.split()[0] == 'PART':
            temp_part = line

        if line.strip() \
                and len(line.split()) > 2 \
                and check_roman_chapters(line.split()[0]) \
                and line.split()[-1].isdigit():
            temp_section = line

        text.append(line)
        leading_spaces = len(line) - len(line.lstrip(' '))

        if line.strip() and len(line.split()[0]) > 1 \
                and len(line.split()) > 1 \
                and not line.split()[-1].isdigit() \
                and leading_spaces < 2:

            # Part III with tables
            if temp_part.strip() == title_dict['partIII']['partIII'] \
                    and line_cutting(temp_section) == title_dict['partIII']['section']:
                if line.lstrip()[0].isdigit() and line.split()[0][1] == '.':
                    if check_spaces(line):
                        if check_special_words(line):
                            if partIII_titles and line_cutting(line) == partIII_titles[0]:

                                if text:
                                    cursor = mydb.cursor()
                                    sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                    val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
                                    cursor.execute(sql, val)
                                    mydb.commit()
                                    text = []

                                if partIII_titles and line_cutting(line) == partIII_titles[0]:
                                    partIII_titles.pop(0)
                                    pos = line_cutting(line)
                                    part = temp_part
                                    section = line_cutting(temp_section)
                                    title = ""

                continue


            if len(line.split()[0]) > 2:
                if line.lstrip()[0].isdigit() and line.split()[0][2] == '.':
                    if check_spaces(line):
                        if check_special_words(line):

                            if text:
                                cursor = mydb.cursor()
                                sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
                                cursor.execute(sql, val)
                                mydb.commit()
                                text = []

                            if len(line.split()[0]) == 3:
                                part = temp_part
                                section = line_cutting(temp_section)
                                pos = line_cutting(line)
                                title = ""

                            else:
                                title = line_cutting(line)

                    else:
                        if text:
                            cursor = mydb.cursor()
                            sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
                            cursor.execute(sql, val)
                            mydb.commit()
                            text = []

                        if len(line.split()[0]) == 3:
                            part = temp_part
                            section = line_cutting(temp_section)
                            pos = line_cutting(line)
                            title = ""

                        else:
                            title = line_cutting(line)

            if line.lstrip()[0].isdigit() and line.split()[0][1] == '.':
                if check_spaces(line):
                    if check_special_words(line):

                        if temp_part.strip() == title_dict['partII']['partII'] \
                                and line_cutting(temp_section) == title_dict['partII']['section'] \
                                and pos == title_dict['partII']['pos']:
                            continue

                        if temp_part.strip() == title_dict['partIII']['partIII'] \
                                and line_cutting(temp_section) == title_dict['partIII']['section']:

                            continue

                        if text:
                            cursor = mydb.cursor()
                            sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
                            cursor.execute(sql, val)
                            mydb.commit()
                            text = []

                        if len(line.split()[0]) == 2:
                            part = temp_part
                            section = line_cutting(temp_section)
                            pos = line_cutting(line)
                            title = ""

                        else:
                            title = line_cutting(line)
                else:

                    if temp_part.strip() == 'PART Ⅲ. OUTFITTING & MACHINERY PART' \
                            and line_cutting(temp_section) == 'Ⅱ. CATEGORIES OF INSPECTION AND TEST ITEMS':
                        continue

                    if text:
                        cursor = mydb.cursor()
                        sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
                        cursor.execute(sql, val)
                        mydb.commit()
                        text = []

                    if len(line.split()[0]) == 2:
                        part = temp_part
                        section = line_cutting(temp_section)
                        pos = line_cutting(line)
                        title = ""

                    else:
                        title = line_cutting(line)

if text:
    cursor = mydb.cursor()
    sql = "INSERT INTO " + table_name + " (part, section, pos, title, par_text, page, file_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (part, section, pos, title, print_text(text), page_cnt, FILE_NAME)
    cursor.execute(sql, val)
    mydb.commit()

cursor.close()