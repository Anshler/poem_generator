import openai
import pandas as pd
import json
import time

#------------------USE OPENAI API TO BUILD NEW DATA FROM THE POEMS DATASET-------------------------------

def cleaning(text):
    text = text.replace('chu', 'chữ')
    text = text.replace('luc bat', 'lục bát')
    return text

dataset = pd.read_csv("dataset/poems_dataset_0.9.csv")
dataset['genre'] = dataset['genre'].apply(lambda x: cleaning(x))

# Set your OpenAI API key
openai.api_key = '<API-KEY>'

start = 0
def process_outfile():
    recent = start # CURRENT INDEX

    try:
        readfile = open("dataset/dataset.json", 'r', encoding='utf-8').readlines()
        if readfile == []:
            outfile = open("dataset/dataset.json", 'a', encoding='utf-8')
            return recent, outfile

        recent = len(readfile) - 1 + start
        writefile = open("dataset/dataset.json", 'w', encoding='utf-8')
        for a in readfile[:-1]:
            writefile.write(a)
        outfile = open("dataset/dataset.json", 'a', encoding='utf-8')
        return recent, outfile

    except:
        outfile = open("dataset/dataset.json", 'a', encoding='utf-8')
        return recent, outfile

recent, outfile = process_outfile()

while True:
    try:
        for index, poem in dataset[recent:].iterrows():
            print(index)
            recent = index
            new_poem = poem['content'].split('\n')
            new_poem = '\n'.join(new_poem[:9])
            print(new_poem)
            prompt = {"role": "user", "content": """

            Tóm tắt bài thơ sau thành một prompt dưới 20 từ theo công thức "Prompt: Viết bài thơ %s về ...". Có thể trích dẫn 1-3 cụm từ trong bài thơ theo dạng "Có chứa từ khóa "xyz"".

            %s

            """ % (poem['genre'], new_poem)}

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[prompt]
            )
            message = response['choices'][0]['message']['content'].split('Prompt: ')[1].replace('\n', ' ')
            print('\n' + message)
            data = {"prompt": message, "completion": poem['content']}
            json.dump(data, outfile)
            outfile.write('\n')
            time.sleep(5)

    except Exception as e:
        print(e)
        print('continue from most recent index...')
        time.sleep(10)
        continue
    break