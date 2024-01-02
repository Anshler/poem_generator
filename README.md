# Vietnamese Poem Generation & The Prospect Of Cross-Language Poem-To-Poem Translation 📜🖋️
[\[paper\]]() [\[model\]](./modeling/poem_generator_(bloom)) [\[demo\]](https://colab.research.google.com/drive/1Mw_MsCix-NeUGRu77E-BkkvW6tut-AI-?usp=sharing)

Poetry generation has been a challenging task in the field of Natural Language Processing, as it requires the model to understand the nuances of language, sentiment, and style. In this paper, we propose using Large Language Models to generate Vietnamese poems from natural language prompts, thereby facilitating an intuitive process with enhanced content control. 

Our most efficacious model, the GPT-3 Babbage variant, achieves a custom evaluation score of ```0.8```, specifically tailored to the "luc bat" genre of Vietnamese poetry. Furthermore, we also explore the idea of paraphrasing poems into normal text prompts and yield a relatively high score of ```0.718``` in the "luc bat" genre. This experiment presents the potential for cross-Language poem-to-poem translation with translated poems as the inputs while concurrently maintaining complete control over the generated content.

_Read our report_ [here](VNese-poem-generation-&-poem-translation.pdf)

## Dataset
A collection of 171188 Vietnamese poems with different genres: luc-bat, 5-chu, 7-chu, 8-chu, 4-chu. Download [here](https://github.com/fsoft-ailab/Poem-Generator/raw/master/dataset/poems_dataset.zip)

For more detail, refer to the _Acknowledgments_ section

## Pre-evaluation

We trained a custom genre classifier based on BERT with the accuracy of ```99.7%``` to classify the correct genre before scoring. This would be helpful during blind test (where genre is not specified). For more detail, refer to our [vietnamese-poem-classifier](https://github.com/Anshler/vietnamese-poem-classifier) repo.

The training code is in this repo. To train the classifier, run:

```
python poem_classifier_training.py
```

## Evaluation

We use a custom function to score the quality of a poem, based soldly on its conformation to the rigid rule of various types of vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow: ```score = L/10 + 3T/10 + 6R/10```

*Table 1: Result comparison of models*
<table>
  <tr>
    <th>Models</th>
    <th>Luc Bat</th>
    <th>Blind</th>
    <th>7 Chu</th>
    <th>8 Chu</th>
    <th>5 Chu</th>
    <th>4 Chu</th>
  </tr>
  <tr>
    <td colspan="7" align="center"><strong>text-to-poem</strong></td>
  </tr>
  <tr>
    <td>ChatGPT (zero-shot)</td>
    <td>0.440</td>
    <td>0.345</td>
    <td>0.292</td>
    <td>0.197</td>
    <td>0.284</td>
    <td>0.238</td>
  </tr>
  <tr>
    <td>Davinci (1000 samples)</td>
    <td>0.580</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>BLOOM (20k samples)</td>
    <td>0.678</td>
    <td>0.596</td>
    <td>0.367</td>
    <td>0.279</td>
    <td>0.480</td>
    <td>0.440</td>
  </tr>
  <tr>
    <td>Babbage (20k samples)</td>
    <td>0.718</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
  <tr>
    <td>Babbage</td>
    <td>0.805</td>
    <td>0.795</td>
    <td>0.661</td>
    <td>0.500</td>
    <td>0.382</td>
    <td>0.392</td>
  </tr>
  <tr>
    <td colspan="7" align="center"><strong>poem-to-poem</strong></td>
  </tr>
  <tr>
    <td>Babbage</td>
    <td>0.781</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
  </tr>
</table>


Currently, the ```Luc Bat``` genre score highest due to sheer sample size. It also has the tendency to genrerate ```Luc Bat``` when the genre is not specified, so it also scores very high during blind test.

## Inference

The opensource version use a Lora for ```Bloom-7b1``` in 8bit and can run on colab. You can try it here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Mw_MsCix-NeUGRu77E-BkkvW6tut-AI-?usp=sharing) (probably run out of memory and crash. It used to run fine, new library versions conflict a lot)

## Citation

_Citation temporarily unavailable_ ⏱️

## Acknowledgments

_This project was inspired by the evaluation method from ```fsoft-ailab```'s_ [SP-GPT2 Poem-Generator](https://github.com/fsoft-ailab/Poem-Generator)

_Dataset also taken from their repo_
