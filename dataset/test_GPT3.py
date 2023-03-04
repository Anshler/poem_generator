import openai
import pandas as pd
import json
import time
from utils.check_rule import *
dataset = pd.read_csv("poems_dataset_0.9.csv")
def cleaning(text):
    text = text.replace('chu','chữ')
    text = text.replace('luc bat','lục bát')
    return text

dataset['genre'] = dataset['genre'].apply(lambda x: cleaning(x))


# Set your OpenAI API key
openai.api_key = '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'

recent = 49109 # current index. (hàng cuối cùng dataset.json phải trống, current index sẽ trên nó 1 hàng. Nếu hàng index đó ko đầy đủ (ngắt chương trình nên chưa kịp lưu hết), thì phải xóa)
outfile = open("dataset.json", "a", encoding='utf-8')
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
            
            """ % (poem['genre'],new_poem)}

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[prompt]
            )
            message = response['choices'][0]['message']['content'].split('Prompt: ')[1].replace('\n',' ')
            print('\n'+message)
            data = {"prompt":message, "completion":poem['content']}
            json.dump(data, outfile)
            outfile.write('\n')
            time.sleep(5)

    except Exception as e:
        print(e)
        print('continue from most recent index...')
        time.sleep(10)
        continue
    break
