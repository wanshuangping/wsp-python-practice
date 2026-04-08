def reverseWords(input_str):
    inputWords = input_str.split()
    inputWords = inputWords[-1::-1]
    output = ''.join(inputWords)
    return output
if __name__ == '__main__':
    input_str = 'i leke rob'
    rw = reverseWords(input_str)
    print(rw)
