import random

def random_permutations(elements, n):
    """
    生成指定數量的隨機排列。

    :param elements: 待排列的元素列表
    :param n: 需要生成的排列數量
    :return: 包含隨機排列的列表
    """
    permutations = []
    for _ in range(n):
        shuffled = elements[:]
        random.shuffle(shuffled)
        permutations.append(shuffled)
    return permutations

def unique_random_permutations(elements, n):
    """
    生成指定數量的唯一隨機排列。

    :param elements: 待排列的元素列表
    :param n: 需要生成的排列數量
    :return: 包含唯一隨機排列的列表
    """
    from itertools import permutations
    all_perms = list(permutations(elements))
    random.shuffle(all_perms)
    return [list(p) for p in all_perms[:n]]

def main():
    print("隨機排列測試")
    elements = list(range(1, 6))  # 要排列的元素
    n = 10  # 生成的排列數量

    print("\n隨機排列:")
    random_perms = random_permutations(elements, n)
    for i, p in enumerate(random_perms):
        print(f"排列 {i + 1}: {p}")

    print("\n唯一隨機排列:")
    unique_perms = unique_random_permutations(elements, n)
    for i, p in enumerate(unique_perms):
        print(f"排列 {i + 1}: {p}")

if __name__ == "__main__":
    main()
