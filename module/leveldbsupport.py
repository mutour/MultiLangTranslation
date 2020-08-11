#!/usr/bin/python
# -*- coding:utf-8 -*-


import leveldb


class DB(object):
    def __init__(self, dirpath):
        self.db = leveldb.LevelDB(dirpath)

    def get(self, key):
        try:
            return self.db.Get(key)
        except Exception:
            return None

    def put(self, key, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self.db.Put(key, value)

    def delete(self, key):
        self.db.Delete(key)

    def write(self, key_values):
        batch = leveldb.WriteBatch()
        for (key, value) in key_values.iteritems():
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            batch.Put(key, value)
        self.db.Write(batch)

    def __iter__(self):
        return self.db.RangeIter()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)


if __name__ == '__main__':
    db = DB('../out/testdb')
    db.put("key1", "value1")
    db.write({'key2': 'v2', 'k3': 'v3'})
    for (key, value) in db:
        print key, value

    print db['k3']
    db['k4'] = u'AIS可以'.encode('utf-8')
    print db['k4']

    db['k5'] = u'You can 😁😁😁😁Cancel anytime😁😁😁. I Can😁😁😁😁Cancel anytime😁😁😁.'
    print db['k5']
