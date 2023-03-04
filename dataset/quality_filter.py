from utils.check_rule import *
import pandas as pd

#filter good poem (score > 0.9) take many hours
def filter_09():
    dataset = pd.read_csv('poems_dataset.csv')
    dataset['content'] = dataset['content'].astype(str)
    dataset = dataset[dataset['content'].apply(lambda x: calculate_score(x)[0]) > 0.9]
    print(dataset.shape[0])
    dataset[['content','genre']].to_csv('poems_dataset_0.9.csv')

#filter perfect poem (score = 1)
def filter_10():
    dataset = pd.read_csv('poems_dataset_0.9.csv')
    dataset['content'] = dataset['content'].astype(str)
    dataset = dataset[dataset['content'].apply(lambda x: calculate_score(x)[0]) == 1]
    print(dataset.shape[0])
    dataset[['content', 'genre']].to_csv('poems_dataset_1.0.csv')