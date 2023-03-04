# poem_generator

## Data filtering

download **pytorch_model.bin** from [here](https://www.mediafire.com/file/hlow33i2y0ajac0/pytorch_model.bin/file) and put it in the [poem_classifier](https://github.com/Anshler/poem_generator/tree/main/modeling/poem_classifier) folder. Or retrain it yourself by running [poem_classifier_training.py](https://github.com/Anshler/poem_generator/blob/main/utils/poem_classifier_training.py) (model from trituenhantaoio/bert-base-vietnamese-uncased)

## Dataset building <- DO THIS ONE

trong [test_GPT3.py](https://github.com/Anshler/poem_generator/blob/main/dataset/test_GPT3.py)

```python
# Set your OpenAI API key
openai.api_key = '<API-KEY>'

recent = 0 # current index
```
Tạo tài khoản openai mới, mình xài model gpt-3.5-turbo rẻ hơn gpt-3 nhiều

trong vòng lặp for:
```python
for index, poem in dataset[recent:33000].iterrows():
```
Quân làm [0:33000], mỗi lần dừng thì phải cập nhật biến recent để lần sau chạy tiếp.

