from utils.check_rule import *
import pandas as pd
import openai
import json
from googletrans import Translator

translator = Translator()

def data_cleaning(text):
    text = text.replace('chu','chữ')
    text = text.replace('luc bat','lục bát')
    return text

def post_process(completion):
    completion = completion.split('\n\n')
    if len(completion) >= 2:
        if '.' not in completion[-1]:
            completion = completion[:-1]
        completion = '\n\n'.join(completion)
    else:
        completion = completion[0]
        completion = completion.split('\n')
        if len(completion) % 2 != 0:
            completion = '\n'.join(completion[:-1])
        elif len(completion)>2:
            if '.' not in completion[-1]:
                completion = completion[:-2]
            completion = '\n'.join(completion)
        else:
            completion = '\n'.join(completion)

    return completion.strip()

def eval_score(prompt, completion):
    if 'lục bát' in prompt:
        score = calculate_score(completion, 'luc bat')
    elif '4 chữ' in prompt:
        score = calculate_score(completion, '4 chu')
    elif '5 chữ' in prompt:
        score = calculate_score(completion, '5 chu')
    elif '7 chữ' in prompt:
        score = calculate_score(completion, '7 chu')
    elif '8 chữ' in prompt:
        score = calculate_score(completion, '8 chu')
    else:
        score = calculate_score(completion)
    return score

def blind_preprocess(prompt:str):
    if 'lục bát ' in prompt:
        prompt = prompt.replace('lục bát ','')
    elif '4 chữ ' in prompt:
        prompt = prompt.replace('4 chữ ','')
    elif '5 chữ ' in prompt:
        prompt = prompt.replace('5 chữ ','')
    elif '7 chữ ' in prompt:
        prompt = prompt.replace('7 chữ ','')
    else:
        prompt = prompt.replace('8 chữ ','')
    return prompt

def eval_gpt3(genre, num=10):
    openai.api_key = '<API-KEY>'
    genre = data_cleaning(genre)
    dataset = pd.DataFrame([json.loads(a) for a in open('resource/dataset/dataset_test.json', 'r', encoding='utf-8')]).drop_duplicates()

    dataset = dataset[dataset['prompt'].str.contains(genre)].reset_index(drop=True)
    #dataset = dataset.sample(frac=1).reset_index(drop=True)
    #dataset['prompt'] = dataset['prompt'].apply(lambda x: blind_preprocess(x))

    dataset['prompt'] = dataset['prompt']+'\n###\n'
    eval_data = dataset['prompt'].tolist()

    scores = []
    for prompt in eval_data[:num]:
        resp = openai.Completion.create(
                    engine='babbage:ft-personal-2023-03-15-14-03-11', # Babbage model
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=256,
                    stop = ['@@@','###']
                )

        completion = post_process(resp['choices'][0]['text'])
        print(prompt, completion)

        score = eval_score(prompt,completion)
        print(score[0])
        print(score[1])
        scores.append(score[0])

    print (sum(scores)/len(scores))

def eval_chatgpt(genre, num=10):
    openai.api_key = '<API-KEY>'
    genre = data_cleaning(genre)
    dataset = pd.DataFrame([json.loads(a) for a in open('resource/dataset/dataset_test.json', 'r', encoding='utf-8')]).drop_duplicates()

    dataset = dataset[dataset['prompt'].str.contains(genre)].reset_index(drop=True)
    #dataset = dataset.sample(frac=1).reset_index(drop=True)
    #dataset['prompt'] = dataset['prompt'].apply(lambda x: blind_preprocess(x))

    eval_data = dataset['prompt'].tolist()

    scores = []
    for prompt in eval_data[:num]:
        while True:
            try:
                prompt_template = {"role": "user", "content": prompt}
                resp = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[prompt_template]
                    )
                completion = str(resp['choices'][0]['message']['content'])
                while completion.startswith('\n'):
                    completion = completion[1:]
                print(prompt,'\n', completion)

                score = eval_score(prompt, completion)
                print(score[0])
                print(score[1])
                scores.append(score[0])
                break
            except: pass

    print(sum(scores) / len(scores))

def generate_gpt3(prompt:str):
    openai.api_key = '<API-KEY>'
    prompt = prompt.lower() + '\n###\n'
    prompt = prompt.replace('\'', '\"')
    resp = openai.Completion.create(
        engine='babbage:ft-personal-2023-03-15-14-03-11',  # Babbage model
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        stop=['@@@', '###']
    )

    completion = post_process(resp['choices'][0]['text'])
    print(completion)

def generate_chatgpt(prompt:str):
    openai.api_key = '<API-KEY>'
    prompt = prompt.lower() + '\n###\n'
    prompt = prompt.replace('\'','\"')
    prompt_template = {"role": "user", "content": prompt}
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[prompt_template]
    )
    completion = str(resp['choices'][0]['message']['content'])
    while completion.startswith('\n'):
        completion = completion[1:]
    print(completion)

def preprocess(text:str):
    text = text.lower()
    text = text.replace('\n',' ')
    text = re.sub(' +', ' ', text)
    return text.strip()

def generate_translator(prompt:str):
    openai.api_key = '<API-KEY>'

    prompt = preprocess(prompt)
    prompt = translator.translate(prompt, dest='vi').text + '\n###\n'
    prompt = prompt.lower()
    prompt = prompt.replace('\'', '\"')
    resp = openai.Completion.create(
        engine='babbage:ft-personal-2023-03-17-16-27-22',  # Paragraph to poem Babbage
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        stop=['@@@', '###']
    )

    completion = post_process(resp['choices'][0]['text'])
    print(completion)

def translate_poem(poem:str):
    poem = '\n'.join(poem.split('\n')[:15])
    poem = preprocess(poem)
    poem = translator.translate(poem,dest='en').text
    poem = translator.translate(poem, dest='vi').text
    poem = poem.lower()
    poem = poem.replace('\'', '\"')
    print(poem)
    return poem

def eval_translator(num=100):
    openai.api_key = '<API-KEY>'
    dataset = pd.read_csv('resource/dataset/dataset_test_translator.csv')
    eval_data = dataset['completion'].tolist()

    scores = []
    for prompt in eval_data[:num]:
        resp = openai.Completion.create(
                    engine='babbage:ft-personal-2023-03-17-16-27-22', # Paragraph to poem Babbage
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=256,
                    stop = ['@@@','###']
                )

        completion = post_process(resp['choices'][0]['text'])
        print(prompt, completion)

        score = eval_score(prompt,completion)
        print(score[0])
        print(score[1])
        scores.append(score[0])

    print (sum(scores)/len(scores))

#eval_gpt3('8 chu',100)
#eval_chatgpt('5 chu',100)
eval_translator()

#generate_gpt3('Viết bài thơ lục bát về tình yêu.')
#generate_translator('')