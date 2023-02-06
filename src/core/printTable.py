# coding: utf-8
from prettytable import PrettyTable

def printTable(titleArr=[], align=None, isPrint=True):
    """
    命令工具通常需要输出执行结果，而数据一般以表格的方式输出更符合查看需求，该方法用于生成并打印表格

    **Usage:**

    ```
    >>> from sunday.core.printTable import printTable
    >>> printTable(['姓名', '年龄', '性别'])([['张三', 18, '男'], ['翠花', 20, '女']])
    +------+------+------+
    | 姓名 | 年龄 | 性别 |
    +------+------+------+
    | 张三 |  18  |  男  |
    | 翠花 |  20  |  女  |
    +------+------+------+
    ```

    **Parameters:**

    * **titleArr:** `list` -- 表格头数组
    * **align:** `str` -- 数据对齐方式, l（左对齐）、r（右对齐）、c（局中）
    * **isPrint:** `bool` -- 是否在命令行中打印表格
    """
    table = PrettyTable(titleArr)
    if align:
        for title in titleArr:
            table.align[title] = align
    def log(rowArr=[], alone=False):
        if alone: rowArr = [rowArr]
        for row in rowArr:
            table.add_row(row)
        if isPrint: print(table)
        return table
    return log
