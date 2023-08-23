vals = [2, 3, 5, 8, 10, 18, 20, 28, 30]


class Solution:
    def __init__(self, arr, target):
        self.arr = arr
        self.target = target

    def inner_bi_search(self, start_index, end_index):
        if start_index > end_index or self.target < self.arr[start_index] or self.target > self.arr[end_index]:
            return None
        mid = (start_index + end_index) // 2
        if self.arr[mid] == self.target:
            return mid
        elif self.arr[mid] < self.target:
            return self.inner_bi_search(mid + 1, end_index)
        else:
            return self.inner_bi_search(start_index, mid)

    def bi_search(self):
        return self.inner_bi_search(0, len(self.arr) - 1)


# print(Solution(vals, 1).bi_search())
# print(Solution(vals, 2).bi_search())
# print(Solution(vals, 5).bi_search())
# print(Solution(vals, 7).bi_search())
# print(Solution(vals, 8).bi_search())
# print(Solution(vals, 30).bi_search())
# print(Solution(vals, 31).bi_search())
# print(Solution([1], 1).bi_search())


def bi_search(arr, e):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == e:
            return mid
        elif arr[mid] < e:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


print(bi_search(vals, 1))
