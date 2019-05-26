# -*- coding: utf-8 -*-

"""
This module to generate char list
"""

import random
import os
import codecs
import sys
import json
import io

reload(sys)
sys.setdefaultencoding('utf-8')

def load_char_file(f_input):
    """
    Get all words in files
    :param string: input file
    """
    file_chars = {}
    with codecs.open(f_input, 'r', 'utf-8') as fr:
        for line in fr.readlines():
            try:
                dic = json.loads(line.strip().encode("utf-8"))
                text = dic['text']
                chars = [item.strip() for item in text]
            except:
                continue
            for c in chars:
                file_chars[c] = file_chars.get(c, 0) + 1
    return file_chars


def get_char(train_file, dev_file):
    """
    Get vocabulary file from the field 'postag' of files
    :param string: input train data file
    :param string: input dev data file
    """
    char_dic = load_char_file(train_file)
    if len(char_dic) == 0:
        raise ValueError('The length of train char is 0')
    dev_char_dic = load_char_file(dev_file)
    if len(dev_char_dic) == 0:
        raise ValueError('The length of dev char is 0')
    for dev_c in dev_char_dic:
        if dev_c in char_dic:
            char_dic[dev_c] += dev_char_dic[dev_c]
        else:
            char_dic[dev_c] = dev_char_dic[dev_c]
    print('<UNK>')
    char_set = set()
    value_list = sorted(char_dic.items(), key=lambda d: d[1], reverse=True)
    for c in value_list[:30000]:
        print(c[0])
        char_set.add(c[0])

    # add predicate in all_50_schemas
    if not os.path.exists('./data/all_50_schemas'):
        raise ValueError("./data/all_50_schemas not found.")
    with codecs.open('./data/all_50_schemas', 'r', 'utf-8') as fr:
        for line in fr.readlines():
            dic = json.loads(line.strip())
            p = dic['predicate']
            for p_c in p:
                if p_c not in char_set:
                    char_set.add(p)
                    print(p)


if __name__ == '__main__':
    train_file = sys.argv[1]
    dev_file = sys.argv[2]
    get_char(train_file, dev_file)
