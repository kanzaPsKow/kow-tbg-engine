"""
LogWrapper\n
日志包装器\n
使程序的错误报告存储到 log 目录中\n
By ATN\n
函数列表：\n
logwrap\n
使用方法：
@LogWrapper.logwrap()
def main():
    ...
"""

import time, traceback, os, sys

def _write_log(fname, text):
    '''保存日志\n
    fname ->str 文件名。无需.txt后缀\n
    text ->str 日志内容\n'''
    try:
        fi = open('log\\' + fname + '.txt', 'a', encoding="utf8")
    except FileNotFoundError:
        os.makedirs('log')
        fi = open('log\\' + fname + '.txt', 'a', encoding="utf8")
    fi.write(text + '\n')
    fi.close()

def logwrap(pause=True):
    '''对修饰函数进行日志包装并立刻执行\n
    pause ->bool 是否在输出日志后暂停程序\n'''
    def decorator(func):
        try:
            func()
        except Exception:
            print('\n\n' + '-' * 50)
            now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            log_time = f"error_{now_time}"
            log_text = traceback.format_exc()
            _write_log(log_time, log_text)
            print("错误日志已保存在 log 目录下\n")
            print(log_text)
            if pause:
                input('按下回车键退出...')
    return decorator