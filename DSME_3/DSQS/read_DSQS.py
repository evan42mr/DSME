import re
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
# FILE_NAME = "2019_DSQS_English.txt"
FILE_NAME = "2019_DSQS_.txt" # Korean

text = []
pos = ""
title = ""
part = ""
part_2 = ""
temp_part = ""
temp_part_2 = ""
# partIII_titles = title_dict['partIII']['partIII_titles']
partIII_titles = title_dict['partIII']['partIII_titles_kor']
partIII_text = ""

with open(FILE_NAME) as f:
    for i, line in enumerate(f):

        #         if line and line[0] == '\x0c':
        #             continue
        if line.strip() and line.split()[0] == 'PART':
            temp_part = line

        if line.strip() and line.split()[0] in ['1장.', '2장.'] \
                or line.strip() and len(line.split()) > 2 and line.split()[0].isdigit() and line.split()[1] == '장.':
            temp_part = line

        if line.strip() \
                and len(line.split()) > 2 \
                and check_roman_chapters(line.split()[0]) \
                and line.split()[-1].isdigit():
            temp_part_2 = line

        text.append(line)
        leading_spaces = len(line) - len(line.lstrip(' '))

        if line.strip() and len(line.split()[0]) > 1 \
                and len(line.split()) > 1 \
                and not line.split()[-1].isdigit() \
                and leading_spaces < 2:

            # Part III with tables
            if temp_part.strip() in title_dict['partIII']['partIII'] \
                    and line_cutting(temp_part_2) in title_dict['partIII']['section']:
                if line.lstrip()[0].isdigit() and line.split()[0][1] == '.':
                    if check_spaces(line):
                        if check_special_words(line):
                            if partIII_titles and line_cutting(line) == partIII_titles[0]:

                                if text:
                                    print(f"part: {part}")
                                    print(f"part_2: {part_2}")
                                    print(f"pos: [{pos}]")
                                    print(f"title: {title}")
                                    #print(f"text:")
                                    #print(print_text(text))
                                    print("-" * 60)
                                    text = []

                                if partIII_titles and line_cutting(line) == partIII_titles[0]:
                                    partIII_titles.pop(0)
                                    # pos = line
                                    # pos = stop_words(line)
                                    pos = line_cutting(line)
                                    part = temp_part
                                    part_2 = line_cutting(temp_part_2)
                                    # part_2 = temp_part_2

                                    title = ""

                continue

            # For titles and sub-titles with pos of 2 figures ex. 12. Title
            if len(line.split()[0]) > 2:
                if line.lstrip()[0].isdigit() and line.split()[0][2] == '.':
                    if check_spaces(line):
                        if check_special_words(line):

                            if text:
                                print(f"part: {part}")
                                print(f"part_2: {part_2}")
                                print(f"pos: [{pos}]")
                                print(f"title: {title}")
                                #print("text:")
                                #print(print_text(text))
                                text = []
                                print('-' * 60)

                            if len(line.split()[0]) == 3:
                                pos = line_cutting(line)
                                part = temp_part
                                part_2 = line_cutting(temp_part_2)

                                title = ""
                            else:
                                title = line_cutting(line)


                    else:
                        if text:
                            print(f"part: {part}")
                            print(f"part_2: {part_2}")
                            print(f"pos: [{pos}]")
                            print(f"title: {title}")
                            #print("text:")
                            #print(print_text(text))
                            text = []
                            print('-' * 60)

                        if len(line.split()[0]) == 3:
                            pos = line_cutting(line)
                            part = temp_part
                            part_2 = line_cutting(temp_part_2)
                            title = ""
                        else:
                            title = line_cutting(line)

            if line.lstrip()[0].isdigit() and line.split()[0][1] == '.':
                if check_spaces(line) and line.strip() != "1. 재                  료":
                    # print(f"if --> {i} : {line}")
                    # print(f"if check_spaces(line):\n{i} : {line}")
                    if check_special_words(line):
                        if temp_part.strip() in title_dict['partII']['partII'] \
                                and line_cutting(temp_part_2) in title_dict['partII']['section'] \
                                 and pos in title_dict['partII']['pos']:

                            continue

                        if temp_part.strip() in title_dict['partIII']['partIII'] \
                                and line_cutting(temp_part_2) in title_dict['partIII']['section']:

                            continue

                        if text:
                            print(f"part: {part}")
                            print(f"part_2: {part_2}")
                            print(f"pos: [{pos}]")
                            print(f"title: {title}")
                            #print("text:")
                            #print(print_text(text))
                            text = []
                            print('-' * 60)

                        if len(line.split()[0]) == 2:
                            pos = line_cutting(line)
                            part = temp_part
                            part_2 = line_cutting(temp_part_2)

                            title = ""
                        else:
                            title = line_cutting(line)


                else:
                    # print(f"else --> {i} : {line}")
                    if temp_part.strip() in title_dict['partIII']['partIII'] \
                            and line_cutting(temp_part_2) in title_dict['partIII']['section']:
                        continue

                    if text:
                        print(f"part: {part}")
                        print(f"part_2: {part_2}")
                        print(f"pos: [{pos}]")
                        print(f"title: {title}")
                        #print("text:")
                        #print(print_text(text))
                        text = []
                        print('-' * 60)

                    if len(line.split()[0]) == 2:
                        if line.strip() == "1. 재                  료":
                            pos = line
                        else:
                            pos = line_cutting(line)
                        part = temp_part
                        part_2 = line_cutting(temp_part_2)

                        title = ""
                    else:

                        title = line_cutting(line)

if text:
    print(f"part: {part}")
    print(f"part_2: {part_2}")
    print(f"pos: [{pos}]")
    print(f"title: {title}")
    #print("text:")
    #print(print_text(text))
    text = []