import sys
from collections import OrderedDict
from typing import Optional


class CacheOverflowError(Exception):
    """Exception raised when the cache exceeds its size limit."""


class Cache[T]:

    def __init__(self, cache_size: int):
        """
        An instance of Cache object, with its own memory.

        :param cache_size: Cache size in bytes.
        """
        self.data: OrderedDict[str, T] = OrderedDict()
        self.cache_size: int = cache_size

    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        return self.data.get(key, default)

    def put(self, key: str, item: T) -> None:
        if (item_size := self.sizeof(item)) > self.cache_size:
            raise CacheOverflowError(f"Item size {item_size} exceeds cache size {self.cache_size}")

        while self.free_space - self.sizeof(item) < 0:
            self.data.popitem(last=False)  # Removes items in FIFO order

        self.data[key] = item

    @property
    def free_space(self) -> int:
        return self.cache_size - sum(self.sizeof(item) for item in self.data.values())

    def sizeof(self, item: T) -> int:
        """
        Basic implementation of size of.
        Won't work on more complex objects, like custom classes and nested containers
        """
        return sys.getsizeof(item)

    def __contains__(self, key: str) -> bool:
        if isinstance(key, str):
            return key in self.data

        return False

    def __getitem__(self, key: str) -> T:
        return self.data[key]
