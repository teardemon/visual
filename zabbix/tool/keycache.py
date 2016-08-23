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


class CKeyStore():
    '''
    #TypeError: String or Integer object expected for key, unicode found
    #该模块使用的类型不能是unicode,即，需要使用str进行编码
    '''

    def __init__(self, str_path_db, str_mode='c'):
        self.m_object_db = anydbm.open(str_path_db, str_mode)

    def close(self):
        self.m_object_db.close()

    def store(self, dict_cache):
        if not isinstance(dict_cache, dict):
            return
        for k, v in dict_cache.iteritems():
            self.m_object_db[str(k)] = str(v)

    def key(self, str_key):
        if str(str_key) in self.m_object_db:
            return self.m_object_db[str(str_key)]

    def has_key(self, str_key):
        if str(str_key) in self.m_object_db:
            return 1
        return 0

    def all(self):
        return self.m_object_db.copy()


if __name__ == '__main__':
    # n ： 总是新建一个
    oKeyStore = CKeyStore('/tmp/a.db', 'n')
    # oKeyStore.store({'a': 'a'})
    print oKeyStore.has_key('a')
    print oKeyStore.has_key('b')
    print oKeyStore.key('a')
