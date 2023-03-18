from utils.check_rule import *
import pandas as pd
import json
import re

# filter good poem (score > 0.9) take many hours
def filter_09():
    dataset = pd.read_csv('dataset/poems_dataset.csv')
    dataset['content'] = dataset['content'].astype(str)
    dataset = dataset[dataset['content'].apply(lambda x: calculate_score(x)[0]) > 0.9]
    print(dataset.shape[0])
    dataset[['content','genre']].to_csv('dataset/poems_dataset_0.9.csv')

def train_dataset():
    # preprocess dataset for training
    dataset = pd.read_csv('dataset/dataset.csv')
    dataset['prompt'] = dataset['prompt'].astype(str)
    dataset['completion'] = dataset['completion'].astype(str)
    dataset['prompt'] = dataset['prompt'] + '\n###\n'
    dataset['completion'] = ' ' + dataset['completion'].apply(lambda x: '.\n\n'.join(x.split('\n\n')[:3])) + '.@@@'
    f = open('dataset/dataset_train_gpt_3.jsonl', 'a', encoding='utf-8')
    for index, row in dataset.iterrows():
        a = {'prompt': row['prompt'], 'completion': row['completion']}
        json.dump(a, f)
        f.write('\n')

data = pd.DataFrame([json.loads(a) for a in open('dataset/dataset_train_translator.jsonl', 'r', encoding='utf-8')])
data = data.drop_duplicates().reset_index(drop=True)
print(data.shape[0])