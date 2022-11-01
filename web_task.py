import requests

def get_request_job():
    link = 'http://icanhazip.com'
    response = requests.get(link)
    if response.status_code:
        with open('web.txt', 'w+') as file:
            file.write(response.text)
    print('записали результат запроса в файл')