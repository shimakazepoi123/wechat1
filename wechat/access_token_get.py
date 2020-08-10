#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import csv
import os
import time
import json


class wechat(object):

    def __init__(self):
        self.filename = '1.csv'
        self.Appid = ''
        self.Appsecreat = ''
        self.Token = ''

    def read_csv(self,filename):
        with open(filename,'r') as file:
            file1 = csv.reader(file)
            access_token = list(file1)[0][0]
            file.close()
        return access_token

    def write_csv(self,r1):
        with open(self.filename, 'w', newline='') as file:
            file1 = csv.writer(file)
            file1.writerow([r1])
            file.close()

    def get_access(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.Appid,self.Appsecreat)
        time1 = time.time()
        if time1 - os.path.getmtime('1.csv') >= 7200:
            r1 = requests.get(url).json()['access_token']
            self.write_csv(r1)
            self.read_csv(self.filename)
        else:
            pass

    def picture(self):
        data = {
            'type': 'image',
            'offset': 0,
            'count': 5
        }
        data1 = json.dumps(data)
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % (self.read_csv(self.filename))
        r2 = requests.post(url,data=data1)
        for i in range(data['count']):
            if r2.json()['item'][i]['name'] == 'homework.jpg':
                return r2.json()['item'][0]['media_id'] #返回作业文件mediaid，方便发送图片时对mediaid的调用
            else:
                pass

