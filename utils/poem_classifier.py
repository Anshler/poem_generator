from transformers import pipeline
import pandas as pd

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


class poem_classifier:
    def __init__(self):
        self.__classifier = pipeline("text-classification", model=resources.path('modeling','poem_classifier'))
    def __count_per_lines(self, text):
        text = text.split('\n')
        return str([len(x.split()) for x in text])
    def predict(self,poem):
        if type(poem) is not list and type(poem) is not pd.Series and type(poem) is not str:
            raise TypeError('Must be either str, list[str] or Series(Panda)')
        if type(poem) is str:
            poem = [poem]
        poem = pd.Series(poem).astype(str) # convert to Series
        poem = poem.apply(lambda x: self.__count_per_lines(x)) # convert to word count format like: "[6,8,6,8,6,8]"
        return self.__classifier(list(poem))