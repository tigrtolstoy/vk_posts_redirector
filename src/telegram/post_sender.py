import requests


class PostSender:
    def __init__(self, tg_token):
        self.__token = tg_token   
    
    def send_message(self, message, chat_id):
        print('sending message...')
        method = 'sendMessage'
        url = f"https://api.telegram.org/bot{self.__token}/{method}"
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        response = requests.post(url, data=data)
        print(response.status_code)
        print(response.headers)
        print(response.json())


