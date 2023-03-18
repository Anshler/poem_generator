import openai
import pandas as pd
import json
import time
import re

dataset = pd.read_csv("dataset/dataset.csv")
dataset = dataset[dataset['genre']=='luc bat'].reset_index(drop=True)

# Set your OpenAI API key
openai.api_key = '<API-KEY>'

start = 0
def process_outfile():
    recent = start

    try:
        readfile = open("dataset/dataset_train_translator.jsonl", 'r', encoding='utf-8').readlines()
        if readfile == []:
            outfile = open("dataset/dataset_train_translator.jsonl", 'a', encoding='utf-8')
            return recent, outfile

        recent = len(readfile) - 1 + start
        writefile = open("dataset/dataset_train_translator.jsonl", 'w', encoding='utf-8')
        for a in readfile[:-1]:
            writefile.write(a)
        outfile = open("dataset/dataset_train_translator.jsonl", 'a', encoding='utf-8')
        return recent, outfile

    except:
        outfile = open("dataset/dataset_train_translator.jsonl", 'a', encoding='utf-8')
        return recent, outfile

def preprocess(text:str):
    text = text.lower()
    text = text.replace('\n',' ')
    text = re.sub(' +', ' ', text)
    return text.strip()

recent, outfile = process_outfile()

while True:
    try:
        for index, poem in dataset[recent:].iterrows():
            print(index)
            recent = index
            new_poem = poem['completion'].split('\n')
            new_poem = '\n'.join(new_poem[:15])
            #print(new_poem)
            prompt = {"role": "user", "content": """

            tóm gọn nội dung bài thơ sau thành một đoạn văn xuôi (ngắn dưới 50 từ, không được dài), thay thế bằng các từ đồng nghĩa:
            
            %s""" %new_poem}

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[prompt]
            )
            message = str(response['choices'][0]['message']['content'])
            message = preprocess(message)
            print(message)
            data = {"prompt": message, "completion": new_poem}
            json.dump(data, outfile)
            outfile.write('\n')
            #time.sleep(2)

    except Exception as e:
        print(e)
        print('continue from most recent index...')
        time.sleep(10)
        continue
    break