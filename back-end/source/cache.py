from __future__ import annotations
import sys
from collections import OrderedDict
from typing import Optional


class CacheOverflowError(Exception):
    """Exception raised when the cache exceeds its size limit."""


class Cache[V]:

    def __init__(self, cache_size: int, parent: Cache | None = None):
        """
        An instance of Cache object, with its own memory.

        :param cache_size: Cache size in bytes.
        """
        self.data: OrderedDict[str, V] = OrderedDict()
        self.cache_size: int = cache_size
        self.parent = parent
        self.children: list[Cache] = []
        if parent is not None:
            parent.children.append(self)

    def get(self, key: str, default: Optional[V] = None) -> Optional[V]:
        return self.data.get(key, default)

    def put(self, key: str, item: V) -> None:
        if (item_size := self.sizeof(item)) > self.cache_size:
            raise CacheOverflowError(f"Item size {item_size} exceeds cache size {self.cache_size}")

        if self.parent is not None and key not in self.parent:
            raise KeyError("Provided key doesn't exists in parent object.")

        while self.free_space - self.sizeof(item) < 0:
            self.pop()

        self.data[key] = item

    def pop(self, key: str | None = None, silent: bool = False):
        """Removes last item in the cache and all of its children."""
        if key:
            default = [None] if silent else []
            self.data.pop(key, *default)
        else:
            key, _ = self.data.popitem(last=False)  # Removes items in FIFO order

        for child in self.children:
            child.pop(key, silent=True)

    @property
    def free_space(self) -> int:
        return self.cache_size - sum(self.sizeof(item) for item in self.data.values())

    def sizeof(self, item: V) -> int:
        """
        Basic implementation of size of.
        Won't work on more complex objects, like custom classes and nested containers
        """
        return sys.getsizeof(item)

    def __contains__(self, key: str) -> bool:
        if isinstance(key, str):
            return key in self.data

        return False

    def __getitem__(self, key: str) -> V:
        return self.data[key]

    def __del__(self):
        if self.parent is not None:
            self.parent.children.remove(self)
