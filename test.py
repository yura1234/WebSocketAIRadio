import string
import random

countSym = 1000
countLines = 1000
fileName = f'text_{countSym}.txt'


with open(fileName, mode='w', encoding='utf-8') as file:
    #кол-во строк текста
    for _ in range(countLines):
        s = ''
        #длина строки текста
        for _ in range(countSym):
            if  random.randint(0, 1):
                s += random.choice(string.ascii_letters)
            else:
                s += random.choice(string.digits)

        file.write(s + '\n')

print(f'Total symbols in file - {countSym * countLines}')