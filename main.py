import os
import requests
import datetime
import fuzzywuzzy
from fuzzywuzzy import process
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.metrics import distance

token = "6912814259:AAF1Kyc9zTA6MftmUWoN3lGx8fNHC8lxRPc"
path_dic = r"tbot_dataset.txt"

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        resp_json = resp.json()

        if 'result' in resp_json:
            result_json = resp_json['result']
            return result_json
        else:
            print('Error: Response does not contain the "result" field.')
            return []

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result
        return last_update

def read_dictionary(our_file):
    with open(our_file, "r", encoding="utf-8") as fi:
        data = fi.readlines()
    return data

def handle_question(data, question):
    question = question.lower()
    question = word_tokenize(question)
    closest_question = ""
    closest_distance = float("inf")
    closest_answer = ""
    for entry in data:
        q = entry["question"].lower()
        q_text = word_tokenize(q)
        dist = distance.edit_distance(question, q_text)
        if dist < closest_distance:
            closest_distance = dist
            closest_question = q
            closest_answer = entry["answer"]
    if closest_distance < 3:
        return closest_answer
    else:
        return "Извините, у меня пока нет ответа на этот вопрос. Но я работаю над этим."

greet_bot = BotHandler(token)

now = datetime.datetime.now()

def write_chats(filename, information, today):
    with open(filename, "a", encoding="utf-8") as new:
        new.write(today + "\n")
        new.write(str(information) + "\n")

rate = 77

def main():
    new_offset = None
    hour = now.hour
    dicti = []
    resp = read_dictionary(path_dic)
    dicti.append(resp)

    data = []

    unanswered_questions = []

    while True:
        updates = greet_bot.get_updates(new_offset)

        if len(updates) > 0:
            for update in updates:
                last_update = update
                last_update_id = last_update['update_id']
                last_chat_id = last_update['message']['chat']['id']
                last_chat_name = last_update['message']['chat']['first_name']
                try:
                    first_chat_name = last_update['message']['chat']['last_name']
                except:
                    first_chat_name = "none"

                if 'text' in last_update['message']:
                    last_chat_text = last_update['message']['text']

                    if last_chat_text == "/start":
                        greet_bot.send_message(last_chat_id, 'Привет, {}! Этот чат-бот разработала команда неравнодушных разработчиц и эксперток. Если вам хочется узнать о цифровой гигиене, о том как защитить свои цифровые данные или узнать о кибербуллинге и способах защиты от него – помните, вы не одни, многие сталкиваются с такими проблемами. В данном чат боте вы сможете понять как определить кибербуллинг, как самостоятельно удалить оскорбительные материалы  или контакты служб поддержки, куда вы сможете обратиться. Пожалуйста, задайте свой вопрос.'.format(last_chat_name))
                    else:
                        counter = 0
                        best_match = None
                        greet_bot.send_message(last_chat_id, 'Пожалуйста, подождите немного, {}.'.format(last_chat_name))
                        for el in dicti[0]:
                            if el.startswith("вопрос:"):
                                components = el.split("ответ:")
                                if len(components) == 2:
                                    question, answer = components
                                    leven = fuzzywuzzy.fuzz.partial_ratio(last_chat_text.lower(), question.lower().strip())
                                    if leven >= rate and leven > counter:
                                        print("Understand")
                                        counter = leven
                                        best_match = answer.strip()

                        if best_match:
                            greet_bot.send_message(last_chat_id, best_match)
                        else:
                            response = handle_question(data, last_chat_text)
                            greet_bot.send_message(last_chat_id, response)
                else:
                    greet_bot.send_message(last_chat_id, 'Извините, я могу отвечать только на текстовые сообщения.')

                write_chats(last_chat_name + "_" + first_chat_name, last_update, str(datetime.datetime.now()))
                new_offset = last_update_id + 1

        else:
            print("No updates")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
