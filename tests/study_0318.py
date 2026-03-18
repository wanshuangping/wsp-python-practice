'''
基础语法
第一个字符必须以字母（a-z, A-Z）或下划线 _ 。
标识符的其他的部分由字母、数字和下划线组成。
标识符对大小写敏感，count 和 Count 是不同的标识符。
标识符对长度无硬性限制，但建议保持简洁（一般不超过 20 个字符）。
禁止使用保留关键字，如 if、for、class 等不能作为标识符
'''

'''
age = 26 #普通变量名最常见
user_name = 'roy' #用下划线连接单词，清晰易读
_salary = 7200  #下划线开头通常表示“内部使用”或“私有”
MAX_AGE = 26 #全大写通常表示“常量”（固定不变的值）
_private_var # 双下划线开头，有特殊含义


class StudentInfo:
    pass


StudentInfo  #类名，首字母大写（驼峰命名法）

def calculate_age():
    pass


calculate_age() # 函数名，动词+名词
Python 3 允许使用 Unicode 字符作为标识符，可以用中文作为变量名，非 ASCII 标识符也是允许的了。 
姓名 = "张三"  # 合法
π = 3.14159   # 合法
'''

'''
2nd_place = "silver"    # 错误：以数字开头
user-name = "Bob"       # 错误：包含连字符
class = "Math"          # 错误：使用关键字
$price = 9.99          # 错误：包含特殊字符
for = "loop"           # 错误：使用关键字
'''
# 测试标识符是否合法
def is_vaild_identifier(name):
    try:
        exec (f'{name} = None')
        return True
    except:
        return False
# print(is_vaild_identifier('2var'))
# print(is_vaild_identifier('var2'))

# Python 保留关键字
import keyword
# print(keyword.kwlist)
# IndentationError: unindent does not match any outer indentation level 缩进不一致导致运行错误
# Python 通常是一行写完一条语句，但如果语句很长，我们可以使用反斜杠 \ 来实现多行语句
item_01 = 1
item_02 = 2
item_03 = 3
# total = item_01 +\
#     item_02 + \
#     item_03
total = ['item_01','item_02','item_03']
print(total)
