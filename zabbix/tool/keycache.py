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

    def __del__(self):
        '''
        当一个对象在删除的时候需要更多的清洁工作的时候此方法很有用，比如套接字对象或者文件对象。
        '''
        self.close()

    def close(self):
        '''
        # 每次执行keycache.store后如果该类的实例化被销毁前没有手动关闭anydbm,销毁后文件句柄不会马上释放
        # 新初始化的keycache必须等到系统将超时的文件句柄关闭以后才能使用anydbm.
        # 注意，即使没有获得文件句柄依然能使用anydbm的方法，只是无法写入数据到磁盘。一切操作均在内存中进行
        '''
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
            raise Exception('keycahce.store()期待字典')
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
        return self.m_object_db


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


    # 查看项目已经缓存了多少数据
    def demo3():
        oKeyStore = CKeyStore('/home/yzs/Documents/code/gitlab/visual/static/adsl/cache/key_value.db', 'c')
        print oKeyStore.key('adsl')
        print oKeyStore.all()


    def demo4():
        # n ： 总是新建一个
        oKeyStore = CKeyStore('/tmp/a.db', 'n')
        oKeyStore.store({'a': {'少年': 'a'}})
        oKeyStore.store({'a': {'a': 'b'}})
        print oKeyStore.has_key('a')
        print oKeyStore.key('a')


    demo3()
