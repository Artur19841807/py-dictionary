from typing import Any, Iterator, Optional


class Node:
    """Represents a single key-value entry in the hash table."""

    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = key_hash


class Dictionary:
    """Custom dictionary implementation using open addressing."""

    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self._capacity: int = self.INITIAL_CAPACITY
        self._table: list[Optional[Node]] = [None] * self._capacity
        self._length: int = 0

    def _get_slot(self, key_hash: int, capacity: int) -> int:
        return abs(key_hash) % capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self._length + 1) > self._capacity * self.LOAD_FACTOR:
            self._resize()

        key_hash = hash(key)
        slot = self._get_slot(key_hash, self._capacity)

        while self._table[slot] is not None:
            if self._table[slot].key == key:
                self._table[slot].value = value
                self._table[slot].hash = key_hash
                return
            slot = (slot + 1) % self._capacity

        self._table[slot] = Node(key, value, key_hash)
        self._length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        slot = self._get_slot(key_hash, self._capacity)
        start_slot = slot

        while self._table[slot] is not None:
            if self._table[slot].key == key:
                return self._table[slot].value
            slot = (slot + 1) % self._capacity
            if slot == start_slot:
                break

        raise KeyError(key)

    def delitem(self, key: Any) -> None:
        key_hash = hash(key)
        slot = self._get_slot(key_hash, self._capacity)
        start_slot = slot

        while self._table[slot] is not None:
            if self._table[slot].key == key:
                self._table[slot] = None
                self._length -= 1
                self._rehash_cluster((slot + 1) % self._capacity)
                return
            slot = (slot + 1) % self._capacity
            if slot == start_slot:
                break

        raise KeyError(key)

    def _rehash_cluster(self, start_slot: int) -> None:
        slot = start_slot
        while self._table[slot] is not None:
            node_to_rehash = self._table[slot]
            self._table[slot] = None
            self._length -= 1
            self[node_to_rehash.key] = node_to_rehash.value
            slot = (slot + 1) % self._capacity

    def __len__(self) -> int:
        return self._length

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._table = [None] * self._capacity
        self._length = 0

    def pop(self, key: Any, default: Any = ...) -> Any:
        try:
            target_value = self[key]
            del self[key]
            return target_value
        except KeyError:
            if default is not ...:
                return default
            raise

    def update(self, other: Any) -> None:
        if isinstance(other, (dict, Dictionary)):
            items = (
                other.items()
                if hasattr(other, "items")
                else other.iter_items()
            )
            for k, v in items:
                self[k] = v
        else:
            for k, v in other:
                self[k] = v

    def __iter__(self) -> Iterator[Any]:
        for node in self._table:
            if node is not None:
                yield node.key
