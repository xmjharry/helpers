# @Time : 2021/1/7 17:31
# @Author : Xuki
# @File : download.py
# @Annotation :

from qiniu import Auth
from qiniu import BucketManager
import json

access_key = '2y9GnYh6aBPTS3bfTnAWELrEnjh87_W7azNJk6-p'
secret_key = 'aX0oNPlE_R_pf1_osjx6NC9eLxrswA_A1Mi8-rSf'

q = Auth(access_key, secret_key)
bucket = BucketManager(q)

# bucket_name = 'wyeth-course'
bucket_name = 'uploadsites'
# 前缀
prefix = None
# 列举条目
limit = 1000
# 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
delimiter = None
# 标记
marker = None

with open('wyeth_qiniu_filepath_new.txt', mode='w+', encoding='utf-8') as f:
    while True:
        ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
        text_body = json.loads(info.text_body)
        marker = text_body.get('marker', '')
        print('marker=' + marker)
        for i in ret.get('items', []):
            path = i['key']
            if path.startswith('/'):
                path = path[1:]
            if not path:
                continue
            base_url = 'http://wyeth-course.nibaguai.com/' + path
            base_url = 'http://wyeth-course.nibaguai.com/' + path
            f.write('%s\n' % base_url)
            # 如果空间有时间戳防盗链或是私有空间，可以调用该方法生成私有链接
            private_url = q.private_download_url(base_url, expires=100)
            # print('private_url' + private_url)
        if eof:
            break
print('success')
