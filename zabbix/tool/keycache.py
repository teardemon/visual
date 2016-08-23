#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-8-22 下午8:53
# @Author  : youzeshun
# 参考资料  :
'''
https://pymotw.com/2/anydbm/
'''
# 用途：提供键值对的缓存

import anydbm
import unicodedata


class CKeyStore():
    '''
    #TypeError: String or Integer object expected for key, unicode found
    #该模块使用的类型不能是unicode,即，需要使用str进行编码
    '''

    def __init__(self, str_path_db, str_mode='c'):
        self.m_object_db = anydbm.open(str_path_db, str_mode)

    def close(self):
        self.m_object_db.close()

    def transcoding(self, string):
        '''
        # anydbm模块仅能解析ascii编码字符集的,而python编码字符集为unicode,
        '''
        if isinstance(string, unicode):
            string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        return string

    def store(self, dict_cache):
        if not isinstance(dict_cache, dict):
            return
        for str_k, v in dict_cache.iteritems():
            str_k = self.transcoding(str_k)
            self.m_object_db[str_k] = str(v)

    def key(self, str_key):
        str_key = self.transcoding(str_key)
        if str_key in self.m_object_db:
            return self.m_object_db[str_key]

    def has_key(self, str_key):
        str_key = self.transcoding(str_key)
        if str(str_key) in self.m_object_db:
            return 1
        return 0

    def all(self):
        return self.m_object_db.copy()


if __name__ == '__main__':
    def demo1():
        # n ： 总是新建一个
        oKeyStore = CKeyStore('/tmp/a.db', 'n')
        oKeyStore.store({'a': 'a'})
        print oKeyStore.has_key('a')
        print oKeyStore.has_key('b')
        print oKeyStore.key('a')


    def demo2():
        '''
        存储中文
        :return:
        '''
        oKeyStore = CKeyStore('/tmp/a.db', 'n')
        dict_data = {
            u'\u4e2d\u5c71\u7535\u4fe1': '{"type": "switch", "line": "\\u4e2d\\u5c71\\u7535\\u4fe1", "traffic": {"1day": "http://10.32.64.64/zabbix/chart2.php?graphid=27721&period=86400&updateProfile=1&profileIdx=web.screens&width=700", "7day": ["http://10.32.64.64/zabbix/chart2.php?graphid=27721&period=604800&updateProfile=1&profileIdx=web.screens&width=700"], "graphid": "27721"}, "ip": "121.201.102.1"}'}
        oKeyStore.store(dict_data)
        print oKeyStore.key(u'\u4e2d\u5c71\u7535\u4fe1')


    demo2()
