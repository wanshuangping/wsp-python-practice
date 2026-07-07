from pygments.lexers import python
import PyPDF2
import re

# 读取PDF文件
pdf_path = '/Users/temu/Downloads/附件1：认租一房户型审核结果名单.pdf'
pdf_reader = PyPDF2.PdfReader(pdf_path)

# 检查是否存在数据行里的不合格（即同时包含队列分类和不合格的行）
unqualified_data_lines = []
for page in pdf_reader.pages:
    text = page.extract_text()
    lines = text.split('\n')
    for line in lines:
        # 同时匹配队列分类和不合格
        if re.search(r'(第一队列|第二队列|第三队列)', line) and re.search(r'不合格', line):
            unqualified_data_lines.append(line)

print(f"找到的同时包含队列分类和不合格的数据行数：{len(unqualified_data_lines)}")
if len(unqualified_data_lines) > 0:
    print("示例行：")
    for line in unqualified_data_lines[:10]:
        print(line)
else:
    print("未找到任何数据行里的不合格记录，所有数据行的审核情况均为合格")

