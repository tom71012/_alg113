def riemann_integral(n):
    dx = 1 / n
    dy = 1 / n
    dz = 1 / n
    integral = 0.0
    
    for i in range(n):
        x = (i + 0.5) * dx
        for j in range(n):
            y = (j + 0.5) * dy
            for k in range(n):
                z = (k + 0.5) * dz
                integral += (3 * x**2 + y**2 + 2 * z**2) * dx * dy * dz
    
    return integral

# 計算積分，增加 n 提高精度
n = 100  # 分成 100x100x100 區域
print("黎曼積分結果:", riemann_integral(n))
