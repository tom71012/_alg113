import subprocess
import time

def will_program_halt(program_code, timeout=5):
    """
    判斷程式是否會在指定時間內停機。
    
參數：
    - program_code （str）： 要測試的 Python 程式代碼。
    - timeout （int）： 超時時間，單位為秒。
    
返回：
    - True： 程式在超時時間內停機。
    - False： 程式未停機（可能進入死迴圈）。
    """
    try:
        # 創建一個臨時 Python 腳本檔
        with open("test_program.py", "w") as f:
            f.write(program_code)
        
        # 使用 subprocess 執行測試程式
        process = subprocess.Popen(["python", "test_program.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待指定時間
        start_time = time.time()
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.kill()  # 超時終止進程
                return False  # 程式未在指定時間內停機
            time.sleep(0.1)
        
        return True  # 程式在指定時間內停機
    
    except Exception as e:
        print(f"發生錯誤: {e}")
        return False


# 測試代碼
program_1 = """
import time
time.sleep(3)  # 停機後結束
"""

program_2 = """
while True:
    pass  # 死循環
"""

print("Program 1 是否停機:", will_program_halt(program_1, timeout=5))  # 應输出 True
print("Program 2 是否停機:", will_program_halt(program_2, timeout=5))  # 應输出 False
