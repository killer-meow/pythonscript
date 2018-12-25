# -*- coding: utf-8 -*-
# Monday, December 24, 2018
# Author:nianhua
# Blog:https://github.com/nian-hua/

from multiprocessing import Pool, Manager
import requests
import time
import re


def remove_control_chars(s):

    s = s.replace('"', '')

    s = s.replace('\n', '')

    s = s.replace('\r', '')

    control_chars = ''.join(map(unichr, range(0, 32) + range(127, 160)))

    control_char_re = re.compile('[%s]' % re.escape(control_chars))

    return s if control_char_re.sub('', s) == s else 'NULL'


def post_password(queue):

    while True:

        try:

            password = queue.get()

            if(len(password) < 16):

                if(password != 'NULL'):

                    password = remove_control_chars(password)

                    if (password != 'NULL'):

                        r = requests.get(
                            'http://192.168.1.128/?dictname=password&dictvalue=%s' % password)
        except:

            pass


def readata(queue):

    fr = open('soeng.csv')

    print "打开文件成功...."

    print "正在读取文件...."

    for i in fr:

        queue.put(i)

    print "文件读取完毕...."

    fr.close()

    print "文件正在关闭...."


pool = Pool(30)

poolr = Pool(1)

queue = Manager().Queue(1000000)

for i in range(30):

    pool.apply_async(post_password, args=(queue,))

poolr.apply_async(readata, args=(queue,))

print "线程创建成功...."

while True:

    time.sleep(3)

    print "队列剩余:" + str(queue.qsize())

    if queue.qsize() == 0:

        break
