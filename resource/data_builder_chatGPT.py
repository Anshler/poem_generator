#   WARNING: THIS CODE IS DEPRECATED
#   CHATGPT NOW HAS OFFICAL API
#   THIS WEB VERSION'S AUTHENTICATION-BYPASS TRICK IS ALREADY PATCHED

import time
from pyChatGPT import ChatGPT
import json
import os
import pandas as pd

def data_cleaning(text):
    text = text.replace('chu','chữ')
    text = text.replace('luc bat','lục bát')
    return text
def prompt_cleaning(text):
    text = text.replace('\nhoặc','')
    text = text.replace('\nHoặc', '')
    text = text.replace('\n', '')
    if text[0] == "\"":
        text = text[1:-1]
    return text

dataset = pd.read_csv("dataset/poems_dataset_0.9.csv")
dataset['genre'] = dataset['genre'].apply(lambda x: data_cleaning(x))

#ChatGPT
session_token = '<SESSION-TOKEN>'
api = ChatGPT(session_token)

current = 0 # current index, whenever encounter error, restart from it
outfile = open("dataset/dataset.json", "a", encoding='utf-8')
start = 0 # first prompt must be good, so chatgpt can base the latter prompts off of it
error = 0 # count consecutive error
resp = '' # initiate first response, in case of duplicate
while True:
    try:
        for index, poem in dataset[current:].iterrows():
            print(index)
            current = index
            # ----Limit Poem Length (chatGPT can't handle too long)----
            new_poem = poem['content'].split('\n')
            new_poem = '\n'.join(new_poem[:19]) # 4 paragraphs, or 19 lines
            # -----------------------------------------PROMPT------------------------------------------------
            prompt = """
            Tôi có một bài thơ và cần tạo prompt làm input để train một language model để tạo ra bài thơ. Làm theo một trong hai cách sau:
            - Tóm gọn bài thơ thành văn xuôi, sử dụng câu từ khác bài thơ nhưng giữ càng nhiều ý chính càng tốt. Có thể trích dẫn 1-5 chữ hoặc câu từ bài thơ, ví dụ như: "có chứa từ khóa "xyz"". Bắt đầu với "Prompt: Viết một bài thơ %s về"
            - Tóm gọn bài thơ thành một câu ngắn dưới 20 chữ. Bắt đầu với "Prompt: Viết một bài thơ". (Có thể nêu rõ bài thơ thuộc thể thơ %s)
            
            Bài thơ là như sau:
    
            %s""" % (poem['genre'],poem['genre'], new_poem)
            # -----------------------------------------------------------------------------------------------
            old_resp = resp
            resp = api.send_message(prompt)
            if "Prompt:" not in resp['message']: # faulty response, not in format
                raise Exception('Faulty response')
            if start == 0 and len(resp['message'].split('Prompt:'))>2: # multiple prompts -> bad start
                raise Exception('Bad start')
            if old_resp == resp: # response somehow got duped, new poem got same response as previous
                raise Exception('Dupe response')
            start = 1
            error = 0
            # ----------------------------------------OUTPUT-------------------------------------------------
            print(resp['message'])
            message = prompt_cleaning(resp['message'].split('Prompt:')[1].strip()) # post processing
            data = {"prompt":message, "completion":poem['content']}
            json.dump(data, outfile)
            outfile.write('\n')

            # reset the conversation
            api.reset_conversation()
    except Exception as e:
        error += 1
        print(e)
        # cooldown
        if 'Too many requests' in str(e): # Too many requests in 1 hour. Try again later.
            print('30m cooldown from current index...')
            time.sleep(1800)
        else:
            print('60s cooldown from current index...')
            time.sleep(60)
        # ---------------------------------Refresh or start new window--------------------------------------
        if error == 5:
            os.system("taskkill /im chrome.exe /f") # close chrome window
            time.sleep(1)
            api = ChatGPT(session_token) # open new window
            error = 0
        else:
            api.refresh_chat_page()  # refresh chat page
        start = 0
        continue
    break