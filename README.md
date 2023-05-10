# Vietnamese Poem Generation & The Prospect Of Cross-Language Poem-To-Poem Translation

Poetry generation has been a challenging task in the field of Natural Language Processing, as it requires
the model to understand the nuances of language, sentiment, and style. Our proposed system will use
Language Model and deep learning techniques to generate poems from natural language prompt that is
both intuitive and offers greater control over the generated content. The model will be trained on a large
corpus of poems written in a Vietnamese language, and will be evaluated using custom metrics tailtored
specifically for Vietnamese poem

Our team hopes that the results of this research will contribute to the ongoing efforts to advance the
field of AI-generated poetry, especially in Vietnamese, and have potential applications in creative writing,
education, and entertainment.

_This project was inspired by_ ```fsoft-ailab```_'s_ [SP-GPT2 Poem-Generator](https://github.com/fsoft-ailab/Poem-Generator)

## Dataset
We used the same dataset as ```fsoft-ailab```. Download [here](https://github.com/fsoft-ailab/Poem-Generator/raw/master/dataset/poems_dataset.zip)

## Pre-evaluation

We trained a custom [poem classifier](https://github.com/Anshler/poem_generator/blob/master/utils/poem_classifier.py) based on bert with the accuracy of ```99.7%``` to classify the correct genre before scoring. This would be helpful during blind test (where genre is not specified).

```python
from utils.poem_classifier import poem_classifier

poem = '<insert poem here>'

classifier = poem_classifier()
print(classifier.predict(poem))
```

## Evaluation

We use a custom function to score the quality of a poem, based soldly on its conformation to the rigid rule of various types of vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow:

```score = L/10 + 3T/10 + 6R/10```

Currently, the ```Luc Bat``` genre score highest due to sheer sample size. So when we refer to the score, we mean the ```Luc Bat``` score. It also has the tendency to genrerate ```Luc Bat``` when the genre is not specified, so it also scores very high during blind test.

## Inference

The opensource version use a Lora for ```Bloom-7b1 in 8bit``` and can run on colab. It achieve a score of ```67/100```

You can try it here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Mw_MsCix-NeUGRu77E-BkkvW6tut-AI-?usp=sharing)

The openAI version was finetuned on the ```Babbage``` model. It achieves the score of ```80/100```
