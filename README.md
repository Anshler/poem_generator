# Vietnamese Poem Generation & The Prospect Of Cross-Language Poem-To-Poem Translation 📜🖋️
Poetry generation has been a challenging task in the field of Natural Language Processing, as it requires the model to understand the nuances of language, sentiment, and style. In this paper, we propose using Large Language Models to generate Vietnamese poems from natural language prompts, thereby facilitating an intuitive process with enhanced content control. 

Our most efficacious model, the GPT-3 Babbage variant, achieves a custom evaluation score of ```0.8```, specifically tailored to the "luc bat" genre of Vietnamese poetry. Furthermore, we also explore the idea of paraphrasing poems into normal text prompts and yield a relatively high score of ```0.718``` in the "luc bat" genre. This experiment presents the potential for cross-Language poem-to-poem translation with translated poems as the inputs while concurrently maintaining complete control over the generated content.

_Read our report_ [here](VNese-poem-generation-&-poem-translation.pdf)

## Dataset
We used the same dataset as ```fsoft-ailab```. Download [here](https://github.com/fsoft-ailab/Poem-Generator/raw/master/dataset/poems_dataset.zip)

## Pre-evaluation

We trained a custom [poem classifier](utils/poem_classifier.py) based on bert with the accuracy of ```99.7%``` to classify the correct genre before scoring. This would be helpful during blind test (where genre is not specified).

```python
from utils.poem_classifier import poem_classifier

poem = '''<insert poem here>'''

classifier = poem_classifier()
print(classifier.predict(poem))
```

## Evaluation

We use a custom function to score the quality of a poem, based soldly on its conformation to the rigid rule of various types of vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow:

```score = L/10 + 3T/10 + 6R/10```

Currently, the ```Luc Bat``` genre score highest due to sheer sample size. So when we refer to the score, we mean the ```Luc Bat``` score. It also has the tendency to genrerate ```Luc Bat``` when the genre is not specified, so it also scores very high during blind test.

## Inference

The opensource version use a Lora for ```Bloom-7b1 in 8bit``` and can run on colab. It achieve a score of ```67/100```

You can try it here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Mw_MsCix-NeUGRu77E-BkkvW6tut-AI-?usp=sharing) (probably run out of memory and crash. It used to run fine, you might need colab pro now)

The openAI version was finetuned on the ```Babbage``` model. It achieves the score of ```80/100```

## Acknowledgments

_This project was inspired by_ ```fsoft-ailab```_'s_ [SP-GPT2 Poem-Generator](https://github.com/fsoft-ailab/Poem-Generator)
