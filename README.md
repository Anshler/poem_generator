# poem_generator

## Data filtering (already filterd)

download **pytorch_model.bin** from [here](https://www.mediafire.com/file/hlow33i2y0ajac0/pytorch_model.bin/file) and put it in the [poem_classifier](https://github.com/Anshler/poem_generator/tree/main/modeling/poem_classifier) folder. Or retrain it yourself by running [poem_classifier_training.py](https://github.com/Anshler/poem_generator/blob/main/utils/poem_classifier_training.py) (model from trituenhantaoio/bert-base-vietnamese-uncased)

## Dataset building <- DO THIS ONE

```python
# Set your OpenAI API key
openai.api_key = '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'
```

run [test_GPT3.py](https://github.com/Anshler/poem_generator/blob/main/dataset/test_GPT3.py).
