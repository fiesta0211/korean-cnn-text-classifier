#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import re
from konlpy.tag import Kkma


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    # string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    # string = re.sub(r"\'s", " \'s", string)
    # string = re.sub(r"\'ve", " \'ve", string)
    # string = re.sub(r"n\'t", " n\'t", string)
    # string = re.sub(r"\'re", " \'re", string)
    # string = re.sub(r"\'d", " \'d", string)
    # string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r"[^ ㄱ-ㅣ가-힣ㅋㅎ\.\^0-9(),!?\'\"♥]", " ", string)
    string = re.sub(r"[ㄱ-ㅊㅌ-ㅍㅏ-ㅛㅣ]", "", string)  # ㅋ ㅎ ㅜ ㅠ ㅡ 빼고 제거
    string = re.sub(r"\.", " . ", string)
    string = re.sub(r",", " , ", string)  # 온점과 쉼표를 기준으로 나누기
    string = re.sub(r"[\'\"]", "", string)  # 작은따옴표, 큰따옴표 제거
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\?", " ? ", string)  # 느낌표 물음표 띄어쓰기로 나누기
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"♥", " ♥ ", string)
    return string.strip()


def split_func(iterator):
    return (x.split() for x in iterator)


def tokenize(string):
    """
    형태소 분석
    "나는 너가 좋아" -> "나 는 너 가 좋아"
    """
    kkma = Kkma()
    tokenized_string = ""
    for i in kkma.morphs(string):
        tokenized_string += i + ' '
    return tokenized_string


def load_data_and_labels(positive_data_file, negative_data_file, positive_data_file_morph, negative_data_file_morph):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(
        open(positive_data_file, "r", encoding='utf-8').readlines())
    positive_examples_morph = list(
        open(positive_data_file_morph, "r", encoding='utf-8').readlines())

    negative_examples = list(
        open(negative_data_file, "r", encoding='utf-8').readlines())
    negative_examples_morph = list(
        open(negative_data_file_morph, "r", encoding='utf-8').readlines())

    # positive_tagged = open("./tagged_data/positive.txt", 'w', encoding="utf-8")
    # negative_tagged = open("./tagged_data/negative.txt", 'w', encoding="utf-8")

    # for s in positive_examples:
    #     positive_tagged.write(tokenize(clean_str(s.strip())) + "\n")
    # for s in negative_examples:
    #     negative_tagged.write(tokenize(clean_str(s.strip())) + "\n")

    # positive_examples = [s.strip() for s in positive_examples]

    # negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text_morph = positive_examples_morph + negative_examples_morph
    # x_text = [tokenize(clean_str(sent)) for sent in x_text]

    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)

    return [x_text, x_text_morph, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


if __name__ == '__main__':
    load_data_and_labels("./tagged_data/positive.txt",
                         "./tagged_data/negative.txt",
                         "./morph_tagged_data/positive.txt",
                         "./morph_tagged_data/negative.txt")
