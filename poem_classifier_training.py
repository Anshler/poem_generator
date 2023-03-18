import pandas as pd
from datasets import DatasetDict, Dataset
import transformers
from sklearn.model_selection import train_test_split
import evaluate
import numpy as np
import torch

# train a model for poem classification
# mapping genres
id2label = {0:'4 chu', 1:'5 chu', 2:'7 chu', 3:'luc bat', 4:'8 chu'}
label2id = {'4 chu':0, '5 chu':1, '7 chu':2, 'luc bat':3, '8 chu':4}

def to_lines_len(text): #string of list of length of each line
    text = text.split('\n')
    return str([len(x.split()) for x in text])

data = pd.read_csv("resource/dataset/poems_dataset.csv")
data = data.sample(frac=1).reset_index(drop=True)[:20000]
data['content'] = data['content'].astype(str).apply(lambda x: to_lines_len(x)) # turn poem into list of line length: [6,8,6,8,6,8...]
data['labels'] = data['genre'].apply(lambda x: label2id[x]) # map labels to number
data_train, data_test = train_test_split(data[['content','labels']],test_size=0.2)

#custom dataset
class PoemDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.tokenizer = tokenizer
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        prompt = self.data.iloc[index]['content']
        completion = self.data.iloc[index]['labels']
        content = self.tokenizer(prompt, truncation=True, padding='max_length', max_length=64,
                                   return_tensors='pt').input_ids.squeeze()
        return {'input_ids': content, 'labels': completion}

#custom weight
class MyTrainer(transformers.Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs['labels']
        # Generate output using the model
        outputs = model(**inputs)
        logits = outputs.logits

        loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
        loss = loss_fct(logits.view(-1, logits.shape[-1]), labels.view(-1)).mean()

        return (loss, outputs) if return_outputs else loss

tokenizer = transformers.BertTokenizer.from_pretrained("trituenhantaoio/bert-base-vietnamese-uncased")
tokenized_poem_train = PoemDataset(data_train)
tokenized_poem_test = PoemDataset(data_test)

accuracy = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

model = transformers.BertForSequenceClassification.from_pretrained("trituenhantaoio/bert-base-vietnamese-uncased", num_labels=5, ignore_mismatched_sizes=True, id2label=id2label)
model = model.to('cuda:0')

training_args = transformers.TrainingArguments(
    output_dir="modeling",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=2,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=False,
)

trainer = MyTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_poem_train,
    eval_dataset=tokenized_poem_test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model('modeling/poem_classifier')