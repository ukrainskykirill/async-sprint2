import os


def file_system_job():
    write = 'Hello'
    dirs = os.listdir()
    if 'folder' in dirs:
        os.remove("folder/kit.txt")
        os.rmdir("folder")
    os.mkdir('folder')
    with open("folder/kit.txt", "w") as file:
        file.write(str(write)+'\n')
    print("Текущая директория изменилась на ", os.getcwd())