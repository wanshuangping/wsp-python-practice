# print(fixed)以下是一个示例，假设有一个包含人员信息的列表，要筛选出年龄大于 20 岁且性别为'female'的人员：
people = [ {'name':'aimy','age':18,'gender':'man'},
    {'name':'bob','age':22,'gender':'man'},
    {'name':'roy','age':24,'gender':'women'}]
def filter_person(person):
    # try:
    #     age = int(person['age'])
    return person['age'] > 20 and person['gender'] == 'women'
    # except ValueError:
    #     return False
filter_person_list = list(filter(filter_person,people))
print(filter_person_list)


