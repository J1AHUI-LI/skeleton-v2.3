"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will be used for marking.

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in m_entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in m_util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation. Sorry for any inconvenience this causes (hopefully none!).
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any

from structures.m_entry import Entry


class Map:
    LOAD_FACTOR = 0.75  # 一般来说，装填因子设置为 0.75 是比较合适的

    def __init__(self) -> None:
        self.size = 10
        self.map = [None] * self.size
        self.element_count = 0

    def _resize(self):
        old_map = self.map
        self.size = self.size * 2
        self.map = [None] * self.size
        self.element_count = 0  # 重新计数
        for bucket in old_map:
            if bucket is not None:
                for entry in bucket:
                    self.insert(entry)

    def _get_hash(self, key):
        return hash(key) % self.size

    def insert(self, entry: Entry) -> Any | None:
        if self.element_count / self.size > self.LOAD_FACTOR:  # 装填因子超过阈值时扩容
            self._resize()

        key_hash = self._get_hash(entry.get_key())
        if self.map[key_hash] is None:
            self.map[key_hash] = [entry]
            self.element_count += 1
        else:
            for stored_entry in self.map[key_hash]:
                if stored_entry.get_key() == entry.get_key():
                    stored_entry.update_value(entry.get_value())
                    return
            self.map[key_hash].append(entry)
            self.element_count += 1

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which wraps a given key/value in an Entry type.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind.
        """
        entry = Entry(key, value)
        return self.insert(entry)
      
    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        """
        entry = Entry(key, value)
        self.insert(entry)

    def remove(self, key: Any) -> None:
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for i, entry in enumerate(self.map[key_hash]):
                if entry.get_key() == key:
                    self.map[key_hash].pop(i)
                    self.element_count -= 1
                    if not self.map[key_hash]:
                        self.map[key_hash] = None  # 如果列表为空，则设置为 None
                    return

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        """
        # You may or may not need this variable depending on your impl.
        # dummy_entry = Entry(key, None) # Feel free to remove me...
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for entry in self.map[key_hash]:
                if entry.get_key() == key:  # 使用 Entry 对象的方法获取键
                    return entry.get_value()  # 返回 Entry 对象的值
        return None


    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        """
        # You may or may not need this variable depending on your impl.
        return self.find(key)

    def get_size(self) -> int:
        return self.element_count

    def is_empty(self) -> bool:
        return self.get_size() == 0


# def test_map():
#     map = Map()
#
#     # 测试插入
#     map.insert_kv("a", 1)
#     assert map.find("a") == 1  # 检查是否可以找到刚刚插入的元素
#
#     # 测试更新
#     map.insert_kv("a", 2)
#     assert map.find("a") == 2  # 检查元素是否已更新
#
#     # 测试删除
#     map.remove("a")
#     assert map.find("a") == None  # 检查删除后元素是否不存在
#
#     # 测试 __setitem__ 和 __getitem__
#     map["b"] = 3
#     assert map["b"] == 3  # 检查是否可以通过 __getitem__ 找到元素
#
#     # 测试 get_size 和 is_empty
#     assert map.get_size() == 1  # 目前 map 中应该有一个元素
#     assert not map.is_empty()  # map 不应该是空的
#
#     # 再次测试删除
#     map.remove("b")
#     assert map.get_size() == 0  # 现在 map 应该是空的
#     assert map.is_empty()  # 确认 map 是空的
#
#     print("All tests passed!")
#
#
# if __name__ == "__main__":
#     test_map()
