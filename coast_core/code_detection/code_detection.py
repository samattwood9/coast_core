"""
    Title: code_detection

    Author: Yann Le Norment

    Description: Find code in texts
"""
import json
import sys
import re


def feature_detection(word):
    features = []
    match_num = 0

    try:
        with open("patterns.json") as patterns:
            features_file = json.load(patterns)
            for type, pattern in features_file.items():
                matches = re.finditer(pattern, word)
                if matches:
                    for num, match in enumerate(matches):
                        match_num += 1
                        features.append({
                            "type": type,
                            "match_num": match_num,
                            "expression": match.group()
                        })
    except Exception as e:
        print("\nError: ")
        sys.stdout.write(str(e))

    # Keywords
    try:
        with open("keywords.txt") as keywords_file:
            lines = keywords_file.readlines()
            for keyword in lines:
                keyword = keyword.rstrip()
                keyword_rules = "(^| )" + keyword + "( |\(|\{|:|$)"
                if re.search(keyword_rules, word):
                    match_num += 1
                    features.append(({
                        "type": "KEYWORD",
                        "match_num": match_num,
                        "expression": word
                    }))
    except Exception as e:
        sys.stdout.write(str(e))
        print('\n')

    return features


def extract_features_from_text(text, print_results):
    text_data = []

    total_char = 0
    total_words = 0
    total_lines = 0

    lines_data = []
    lines = text.split('\n')

    for line in lines:

        total_lines += 1
        words_data = []
        words = line.split()

        line_length_by_words = len(words)
        line_length_by_char = sum(len(word) for word in words)

        try:
            first_word = words[0]
            last_word = words[line_length_by_words - 1]
            first_char = first_word[0]
            last_char = last_word[len(last_word) - 1]
        except Exception as e:
            first_word = str(e)
            first_char = str(e)
            last_word = str(e)
            last_char = str(e)

        position = 0
        for word in words:
            word_data = []
            position += 1
            total_char += len(word) + 1
            features = feature_detection(word)
            if features:
                word_data.append({
                    "word": word,
                    "position": position,
                    "features": features
                })
            if not features:
                word_data.append({
                    "word": word,
                    "position": position
                })

            words_data.append(word_data)
        total_words += position

        lines_data.append({
            "line_num": total_lines,
            "line_length_by_words": line_length_by_words,
            "line_length_by_char": line_length_by_char,
            "first_word": first_word,
            "first_char": first_char,
            "last_word": last_word,
            "last_char": last_char,
            "words_data": words_data
        })
        if print_results:
            print("line_num:", total_lines, "\nline_length words:", line_length_by_words,
                  "\nline_length char:", line_length_by_char, "\nfirst word:", first_word,
                  "\nfirst char", first_char, "\nlast_word:", last_word, "\nlast_char", last_char,
                  "\n==========================")

    text_data.append({
        "total_char": total_char,
        "total_lines": total_lines,
        "total_words": total_words,
        "lines_data": lines_data
    })
    if print_results:
        print("Total char:", total_char, "\nTotal words:", total_words, "\nTotal lines:", total_lines)

    return text_data


def binary_transformation(text_data, print_results):
    binary_text = ''
    binary_lines = []

    for data in text_data:

        for line in data['lines_data']:
            binary_line = ''
            for word in line['words_data']:
                word = word[0]
                # Default word value
                word_value = ''
                try:
                    if word['features']:
                        word_value = '1'
                except:
                    word_value = '0'
                binary_line += word_value
            # Default binary line value
            binary_line_value = '0'
            if '1' in binary_line:
                binary_line_value = '1'
            # Updating the list of lines in the text
            binary_lines.append(binary_line)
            # Updating the string which represent the text
            binary_text += binary_line_value
            if print_results:
                print("Line num:", line['line_num'], "\nBinary line:", binary_line,
                      "\n=======================")
    return binary_text, binary_lines


def absolute_transformation(text_data, print_results):
    absolute_lines = []

    for data in text_data:
        for line in data['lines_data']:
            absolute_line = ''
            absolute_line_value = 0
            for word in line['words_data']:
                word = word[0]

                # Default word value
                word_value = ''

                try:
                    if word['features']:
                        word_value = str(len(word['features']))
                except:
                    word_value = '0'
                absolute_line += word_value
                absolute_line_value += int(word_value)
            absolute_lines.append(absolute_line)

            if print_results:
                print("Line num:", line['line_num'], "\nAbsolute line:", absolute_line,
                      "\nValue:", absolute_line_value, "\n=======================")

    return absolute_lines


def binary_code_percentage(binary_lines):
    code_presence = 0
    words_nb = 0
    percentage = None

    for line in binary_lines:
        words_nb += len(line)
        for i in range(0, len(line)):
            if '0' in line:
                pass
            if '1' in line:
                code_presence += 1

    percentage = (code_presence / words_nb) * 100
    # print("Percentage", percentage)
    return percentage


def absolute_code_percentage(absolute_lines):
    code_presence = 0
    words_nb = 0
    percentage = None

    for line in absolute_lines:
        words_nb += len(line)
        for i, char in enumerate(line):
            if char is not '0' and not None:
                code_presence += int(char)
    if words_nb is not 0:
        percentage = (code_presence / words_nb) * 100
    # print("Percentage", percentage)
    return percentage


def run_all_detection(text, print_results=True):
    print("\nFeatures extraction")
    text_data = extract_features_from_text(text, print_results)

    print("\nBinary and absolute data extraction\n=======================")
    binary_data = binary_transformation(text_data, print_results)
    absolute_lines = absolute_transformation(text_data, print_results)

    print("\nCode percentage calculation")
    binary_percentage = binary_code_percentage(binary_data[1])
    absolute_percentage = absolute_code_percentage(absolute_lines)

    print("binary_percentage:", binary_percentage)
    print("absolute_percentage:", absolute_percentage)
