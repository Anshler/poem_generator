# poem_generator

## Data filtering

download **pytorch_model.bin** from [here](https://www.mediafire.com/file/hlow33i2y0ajac0/pytorch_model.bin/file) and put it in the [poem_classifier](https://github.com/Anshler/poem_generator/tree/main/modeling/poem_classifier) folder. Or retrain it yourself by running [poem_classifier_training.py](https://github.com/Anshler/poem_generator/blob/main/utils/poem_classifier_training.py) (model from trituenhantaoio/bert-base-vietnamese-uncased)

## Dataset building <- DO THIS ONE

trong [test_GPT3.py](https://github.com/Anshler/poem_generator/blob/main/dataset/test_GPT3.py)

```python
# Set your OpenAI API key
openai.api_key = '<API-KEY>'
```
Nếu hêt tiền thì tạo tài khoản openai mới.

rồi cứ chạy, lâu quá thì ngừng lần sau chạy tiếp, nó tự động tiếp tục chỗ bỏ dỡ. (cứ mỗi 10-20 sample nó mới lưu vào file, ko hiểu tại sao, nên khi ngắt chương trình số sample lưu lại sẽ ít hơn 10-20 so với hiển thị trong cửa sổ log)

