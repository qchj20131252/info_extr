"""
This module to generate training data for training a so-labeling model
"""

import random
import codecs
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def get_p(input_file):
    """
    Generate training data for so labeling model
    """
    with codecs.open(input_file, 'r', 'utf-8') as fr:
        for line in fr:
            try:
                dic = json.loads(line.decode('utf-8').strip())
            except:
                continue
            spo_list = dic['spo_list']
            p_list = [item['predicate'] for item in spo_list]
            for p in p_list:
                print "\t".join([json.dumps(dic, ensure_ascii=False), p]).encode('utf-8')


if __name__ == '__main__':
    input_file = sys.argv[1]
    get_p(input_file)