# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:44:16 2022

@author: xiaoqingtech01
"""

import os, json, shutil

historyPath = r'\\Xqdata\公用\标注文件'
historyLabels = {
    'cloud':{},
    'cover':{},
    'deep':{},
    'snow':{},
    'ice':{},
    'frost':{},
    'dew':{},
    'glaze':{},
    'sori':{},
    'vis':{},
    }

def _is_lb_auth_time(val):
    if not isinstance(val, list) or len(val)!=3:
        return False
    if not isinstance(val[2], str) or len(val[2])!=14:
        return False
    return True

for file in os.listdir(historyPath):
    if not file.endswith('.json'):continue
    try:
        with open(historyPath+'/'+file,'r')as f:
            one = json.load(f, strict=False)
        for wea in one:
            for p in one[wea]:
                name = os.path.split(p)[1]
                if not _is_lb_auth_time(one[wea][p]):
                    historyLabels[wea][name]=[one[wea][p],file]
                else:
                    historyLabels[wea][name]=[one[wea][p][0],file]
    except Exception as e:
        print(e, file)
        
aim = r'\\Xqdata\公用\分好的九省数据\广东\ice'
data = r'\\Xqdata\李丑保\9省数据\广东\结冰'
wea = 'ice'

for lb in ['yes', 'no', 'other']:
    if not os.path.exists(aim+'/'+lb):
        os.makedirs(aim+'/'+lb)
        
        
for p in os.listdir(data):
    if not p.endswith('.jpg'):continue
    if p not in historyLabels[wea]:continue
    if historyLabels[wea][p][0]=='有':
        if not os.path.exists(aim+'/yes/'+p):
            shutil.copy(data+'/'+p, aim+'/yes/'+p)
    elif historyLabels[wea][p][0]=='无':
        if not os.path.exists(aim+'/no/'+p):
            shutil.copy(data+'/'+p, aim+'/no/'+p)
    elif historyLabels[wea][p][0]=='无效':
        if not os.path.exists(aim+'/other/'+p):
            shutil.copy(data+'/'+p, aim+'/other/'+p)