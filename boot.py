import os
import sys

# 获取exe所在文件夹路径
exe_path = os.path.abspath(sys.executable)
base_dir = os.path.dirname(exe_path)
script_file = os.path.join(base_dir, "main.py")

if not os.path.exists(script_file):
    input(f"错误：在程序目录找不到 main.py\n{script_file}\n按回车关闭窗口")
else:
    # 加载外部main.py的代码并运行
    with open(script_file, encoding="utf-8") as f:
        code = f.read()
    exec(code)
