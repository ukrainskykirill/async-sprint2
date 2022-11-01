def write_text():
    text = []
    with open('web.txt', 'r') as file:
        for line in file:
            text.append(line)
    with open('folder/kit.txt', 'w+') as file:
            for i in text:
                file.write(i+'\n')
    print('записали в файл ')
