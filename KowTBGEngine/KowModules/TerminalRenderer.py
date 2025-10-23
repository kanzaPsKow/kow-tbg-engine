"""
TerminalRenderer\n
控制台渲染器\n
便于用控制台设计图形和键盘操作程序，以增强程序的可读性
与其他控制台程序一样，TerminalRenderer不适合实时高速渲染\n
By ATN\n
函数列表：\n
change_title\n
place\n
render\n
getch\n
get_terminal_size\n
"""

import os, msvcrt, time, random

_string_list = []
_fore_colors = {'sys_default' : '39', 'blue' : '34', 'red' : '31', 'yellow' : '33', 'green' : '32', 'cyan' : '36', 'magenta' : '35', 'black' : '30', 'white' : '37'}
_back_colors = {'sys_default' : '49', 'blue' : '44', 'red' : '41', 'yellow' : '43', 'green' : '42', 'cyan' : '46', 'magenta' : '45', 'black' : '40', 'white' : '47'}
_styles = {'default' : '0', 'highlight' : '1', 'non-highlight' : '22', 'underline' : '4', 'non-underline' : '24', 'flick' : '5', 'non-flick' : '25', 'reverse' : '7', 'non-reverse' : '27', 'non-visible' : '8', 'visible' : '28'}

def _decorate_string(string, fore_color='sys_default', back_color='sys_default', style='default'):
    """对字符进行彩色修饰。在使用前景色时，背景色必须设定。\n
    string ->str 要修饰的字符\n
    fore_color='sys_default' ->str 前景色\n
    back_color='sys_default' ->str 背景色\n
    style='default' ->str 样式\n
    return str: 修饰后的字符"""
    display_style = '\033[0;'
    display_style += _styles[style] + ';'
    display_style += _fore_colors[fore_color] + ';'
    display_style += _back_colors[back_color] + 'm'
    string = display_style + string + '\033[0m'
    return string

def _len_in_size(string):
    """以字符串所占的位置为标准计算长度\n
    string ->str 要判断的字符串\n
    return int: 长度"""
    length = 0
    for a in string:
        if len(a.encode()) == 1:
            length += 1
        elif len(a.encode()) > 1:
            length += 2
    return length

def change_title(title):
    """更改标题\n
    title ->str: 标题"""
    os.system('title ' + title)

def _get_terminal_size():
    """获取控制台行数和列数\n
    return int: 列数, int: 行数"""
    terminal_size = os.get_terminal_size()
    return terminal_size.columns, terminal_size.lines

def getch():
    """在不阻断程序的情况下获取键盘输入。\n
    return b'string': 输入键值"""
    get = None
    if msvcrt.kbhit():  # 如果键盘有输入
        get = msvcrt.getch()  # 读取键盘输入
    return get

def place(string, pos, fore_color='default', back_color='default', style='default'):
    """在指定位置放置字符\n
    string ->str 字符\n
    pos ->(int, int) 坐标\n
    fore_color='default' ->str 前景色\n
    back_color='default' ->str 背景色\n
    style='default' ->str 字符样式"""
    string = str(string)
    now_x, now_y = pos[0], pos[1]
    a = -1
    add = ''
    while a < len(string) - 1:
        a += 1
        add = string[a]
        _string_list.append([add, now_x, now_y, fore_color, back_color, style])
        now_x += _len_in_size(add)
        add = ''
    if add != '':
        _string_list.append([add, now_x, now_y, fore_color, back_color, style])

def render(origin_colors=('sys_default', 'sys_default'), clear_window=True):
    """渲染界面。\n
    origin_colors=['sys_default', 'sys_default'] ->list 默认颜色
    clear_window=True ->bool 是否清空界面"""
    final_string = '\n'
    max_x, max_y = _get_terminal_size()
    x, y = -1, -1
    while y < max_y - 1:
        final_string += '\n'
        y += 1

        # 若行内无渲染内容则跳过
        sth_in_line = False
        for a in _string_list:
            if a[2] == y:
                sth_in_line = True
                break
        if not sth_in_line:
            continue

        x = -1
        while x < max_x - 1:
            x += 1
            printed = False
            for n in range(0, len(_string_list)):
                s = _string_list[len(_string_list) - n - 1]  # 从string_list的后往前渲染
                colors = [s[3], s[4]]
                if s[3] == 'default':
                    colors[0] = origin_colors[0]
                if s[4] == 'default':
                    colors[1] = origin_colors[1]
                if s[1] == x and s[2] == y:
                    now_print = s[0]
                    style = s[5]
                    if x + _len_in_size(now_print) > max_x:
                        if _len_in_size(now_print) == 1:  # 中文字符
                            now_print = _decorate_string(' ', colors[0], colors[1], style)
                        elif _len_in_size(now_print) == 2:  # 英文字符
                            now_print = _decorate_string(now_print[0], colors[0], colors[1], style)
                    final_string += _decorate_string(now_print, colors[0], colors[1], style)
                    printed = True
                    x += _len_in_size(now_print) - 1
                    break
            if not printed:
                final_string += ' '
    if final_string[-1] == '\n':
        final_string += ' ' * max_x
    print(final_string[1:], end='', flush=True)  # 刷新print
    if clear_window:
        _clear()

def _clear():
    """清空界面。默认在TerminalRenderer.update()中调用"""
    global _string_list
    _string_list = []

def get_terminal_size():
    """获取控制台行数和列数\n
    return (int: 列数, int: 行数)"""
    a, b = _get_terminal_size()
    return (a, b)

if __name__ == '__main__':
    os.system('cls')
    background = 'Welcome  TerminalRenderer  Welcome'
    color = list(_fore_colors.keys())[random.randint(0, len(_fore_colors) - 1)]
    while 1:
        place(background, (int(get_terminal_size()[0] / 2) - int(_len_in_size(background) / 2), int(get_terminal_size()[1] / 2)), color, 'default', 'highlight')
        render()
        time.sleep(1 / 60)

if __name__ != '__main__':
    os.system('cls')  # 不明原因，在程序开始时必须清空一次才会正确显示