# Vietnamese poem generation with GPT-3.5 for data creation and LoRa finetuning on GPT-J

## Raw data filtering

Download **pytorch_model.bin** from [here](https://www.mediafire.com/file/hlow33i2y0ajac0/pytorch_model.bin/file) and put it in the [poem_classifier](https://github.com/Anshler/poem_generator/tree/main/modeling/poem_classifier) folder. Or retrain it yourself by running [poem_classifier_training.py](https://github.com/Anshler/poem_generator/blob/main/utils/poem_classifier_training.py)
## Data building <- DO THIS ONE

Trong [data_builder.py](https://github.com/Anshler/poem_generator/blob/main/dataset/data_builder.py)

```python
# Set your OpenAI API key
openai.api_key = '<API-KEY>'
```
Nếu hêt tiền thì tạo tài khoản openai mới.

Rồi cứ chạy, sẽ tốn 3-4 ngày. Lâu quá thì ngừng lần sau chạy tiếp, nó tự động tiếp tục chỗ bỏ dỡ. (cứ mỗi 10-20 sample nó mới lưu vào file, ko hiểu tại sao, nên khi ngắt chương trình số sample lưu lại sẽ ít hơn 10-20 so với hiển thị trong cửa sổ log)

Muốn nhanh hơn thì tạo nhiều acc openai, cho mỗi acc chạy một phần của dataset

Mình xài gpt-3.5-turbo. Trên lý thuyết nỏ rẻ gấp 10 lần gpt-3, nhưng em xài tới h tiền trial chưa giảm, nên chắc unlimited :v

