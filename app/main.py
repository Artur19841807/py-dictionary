from typing import Any


class Dictionary:
    def __init__(self, data: Any = None) -> None:
        self._items: list[tuple[Any, Any]] = []
        if data:
            self.update(data)

    def _find_index(self, key: Any) -> int:
        for index, (k, _) in enumerate(self._items):
            if k == key:
                return index
        return -1

    def __getitem__(self, key: Any) -> Any:
        index = self._find_index(key)
        if index == -1:
            raise KeyError(f"Key '{key}' not found in Dictionary.")
        return self._items[index][1]

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._find_index(key)
        if index != -1:
            self._items[index] = (key, value)
        else:
            self._items.append((key, value))

    def __delitem__(self, key: Any) -> None:
        index = self._find_index(key)
        if index == -1:
            raise KeyError(f"Key '{key}' not found in Dictionary.")
        self._items.pop(index)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(key for key, _ in self._items)

    def items(self):
        return iter(self._items)

    def update(self, other: Any = None, **kwargs: Any) -> None:
        if other is not None:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key in other:
                    self[key] = other[key]

        for key, value in kwargs.items():
            self[key] = value

    def clear(self) -> None:
        self._items.clear()

    def get(self, key: Any, default: Any = None) -> Any:
        index = self._find_index(key)
        if index != -1:
            return self._items[index][1]
        return default
