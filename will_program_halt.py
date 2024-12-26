import subprocess
import time

def will_program_halt(program_code, timeout=5):
    """
    判断程序是否会在指定时间内停机。
    
    参数:
    - program_code (str): 要测试的 Python 程序代码。
    - timeout (int): 超时时间，单位为秒。
    
    返回:
    - True: 程序在超时时间内停机。
    - False: 程序未停机（可能进入死循环）。
    """
    try:
        # 创建一个临时 Python 脚本文件
        with open("test_program.py", "w") as f:
            f.write(program_code)
        
        # 使用 subprocess 运行测试程序
        process = subprocess.Popen(["python", "test_program.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待指定时间
        start_time = time.time()
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.kill()  # 超时终止进程
                return False  # 程序未在指定时间内停机
            time.sleep(0.1)
        
        return True  # 程序在指定时间内停机
    
    except Exception as e:
        print(f"发生错误: {e}")
        return False


# 测试代码
program_1 = """
import time
time.sleep(3)  # 停机后结束
"""

program_2 = """
while True:
    pass  # 死循环
"""

print("Program 1 是否停机:", will_program_halt(program_1, timeout=5))  # 应输出 True
print("Program 2 是否停机:", will_program_halt(program_2, timeout=5))  # 应输出 False
