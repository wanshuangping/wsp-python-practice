# def reverseWords(input_str):
#     inputWords = input_str.split()
#     inputWords = inputWords[-1::-1]
#     output = ''.join(inputWords)
#     return output
# if __name__ == '__main__':
#     input_str = 'i leke rob'
#     rw = reverseWords(input_str)
#     print(rw)
tuple = ('abc',123,2.3,'roy',70.1)
tinytuple = (123,'roy')
print(tuple)
print(tuple[0])
print(tuple[2:])
print(tinytuple * 2)
print(tuple + tinytuple)