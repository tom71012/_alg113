# 方法 a
def power2n_a(n):
    return 2**n

# 方法 b：用遞迴 （慢）
def power2n_b(n):
    if n == 0: return 1
    return power2n_b(n-1) + power2n_b(n-1)

# 方法 c：用遞迴 (快)
def power2n_c(n):
    if n == 0: return 1
    return 2 * power2n_c(n-1)

# 方法 d：用遞迴+查表
def power2n_d(n, memo={}):
    if n in memo:  # 如果已經計算過，直接返回記錄的值
        return memo[n]
    if n == 0:  # 基礎情況
        memo[n] = 1
    else:  # 遞迴計算並存入查表
        memo[n] = 2 * power2n_d(n-1, memo)
    return memo[n]

# 測試程式
print('power2n_a(10) =', power2n_a(10))
print('power2n_b(10) =', power2n_b(10))  # 注意：此方法較慢，不建議對大數使用
print('power2n_c(10) =', power2n_c(10))
print('power2n_d(10) =', power2n_d(10))

# 對較大數字進行測試
print('power2n_c(40) =', power2n_c(40))
print('power2n_d(40) =', power2n_d(40))
