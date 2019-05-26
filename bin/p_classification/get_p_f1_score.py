# -*- coding: utf-8 -*-

import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def load_p_file(filepath):
    result_dic = {}
    count = 0.0
    with codecs.open(filepath, 'r', 'utf-8') as fr:
        for line in fr.readlines():
            split_list = line.split('	')
            dic = json.loads(split_list[0].strip(), encoding='utf-8')
            relation = split_list[1].strip()
            text = dic['text']
            if text in result_dic:
                result_dic[text].append(relation)
            else:
                result_dic[text] = [relation]
            count += 1
    return count, result_dic

def load_spo_file(filepath):
    spo_dic = {}
    count = 0.0
    with codecs.open(filepath, 'r', 'utf-8') as fr:
        for line in fr.readlines():
            dic = json.loads(line.strip(), encoding='utf-8')
            spo_dic[dic['text']] = []
            for spo in dic['spo_list']:
                spo_dic[dic['text']].append(spo['predicate'])
                count += 1
    return count, spo_dic

def get_accuracy(all_relation_num, correct_num):
    accuracy = correct_num / all_relation_num
    return accuracy

def get_precision(predicted_num, predict_dic, spo_dic):
    correct_num = 0.0
    for key in list(predict_dic.keys()):
        if key in spo_dic:
            for p in predict_dic[key]:
                if p in spo_dic[key]:
                    correct_num += 1
                    spo_dic[key].remove(p)

    precision = correct_num / predicted_num
    return correct_num, precision

def get_recall(all_relation_num, predicted_num, correct_num):
    recall = correct_num / (correct_num + all_relation_num - predicted_num)
    return recall

def get_f1_score(precision, recall):
    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score







if __name__ == '__main__':
    predicted_num, predict_dic = load_p_file("../../data/test_data.p")
    all_relation_num, spo_dic = load_spo_file("../../data/test_data_spo.json")
    correct_num, precision = get_precision(predicted_num, predict_dic, spo_dic)
    recall = get_recall(all_relation_num, predicted_num, correct_num)
    accuracy = get_accuracy(all_relation_num, correct_num)
    f1_score = get_f1_score(precision, recall)
    print "Accuracy:", accuracy
    print "Precision:", precision
    print "Recall:", recall
    print "F1_Score:", f1_score