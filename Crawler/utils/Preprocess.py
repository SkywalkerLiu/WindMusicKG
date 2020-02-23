# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 20:34
# @Author  : GaleHuang (Huang Dafeng)
# @github: https://github.com/Galehuang

import json
DEFAULT_ENCODING = 'utf-8'
def extract_singer_names(file, encoding=DEFAULT_ENCODING):
    names = set()
    try:
        f = open(file, encoding=encoding)
        singers = json.load(f)
        for singer in singers:
            names.add(singer['name'])
        return names
    except:
        print("Error when extracting singer names!")