import random

def monte_carlo_integral(num_points):
    total = 0.0
    
    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        z = random.uniform(0, 1)
        total += 3 * x**2 + y**2 + 2 * z**2
    
    volume = 1  # 積分區域的體積 (0到1的立方體)
    return total / num_points * volume

# 計算積分，增加 num_points 提高精度
num_points = 100000
print("蒙地卡羅積分結果:", monte_carlo_integral(num_points))
