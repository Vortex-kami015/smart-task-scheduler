class MaxHeap:
    """Binary max-heap. Entries are (key, item_id, item); larger key = higher up."""

    def __init__(self):
        self._data = []
        self._pos = {}                    # item_id -> index in _data

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return not self._data

    def push(self, key, item_id, item):           # O(log n)
        self._data.append((key, item_id, item))
        self._pos[item_id] = len(self._data) - 1
        self._sift_up(len(self._data) - 1)

    def peek(self):                               # O(1)
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0][2]

    def pop(self):                                # O(log n)
        if self.is_empty():
            raise IndexError("pop from empty heap")
        return self._remove_at(0)

    def remove(self, item_id):                    # O(log n)
        if item_id not in self._pos:
            raise KeyError(item_id)
        return self._remove_at(self._pos[item_id])

    def contains(self, item_id):
        return item_id in self._pos

    # ---------- internals ----------
    def _remove_at(self, i):
        last = len(self._data) - 1
        self._swap(i, last)
        key, item_id, item = self._data.pop()
        del self._pos[item_id]
        if i < len(self._data):               # fix the element we moved into slot i
            self._sift_down(i)
            self._sift_up(i)
        return item

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._pos[self._data[i][1]] = i
        self._pos[self._data[j][1]] = j

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i][0] > self._data[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left, right, largest = 2 * i + 1, 2 * i + 2, i
            if left < n and self._data[left][0] > self._data[largest][0]:
                largest = left
            if right < n and self._data[right][0] > self._data[largest][0]:
                largest = right
            if largest == i:
                break
            self._swap(i, largest)
            i = largest