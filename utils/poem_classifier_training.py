import pandas as pd
from datasets import DatasetDict, Dataset
import transformers
from sklearn.model_selection import train_test_split
import evaluate
import numpy as np

# train a model for poem classification
# mapping genres
id2label = {0:'4 chu', 1:'5 chu', 2:'7 chu', 3:'luc bat', 4:'8 chu'}
label2id = {'4 chu':0, '5 chu':1, '7 chu':2, 'luc bat':3, '8 chu':4}

def to_lines_len(text): #string of list of length of each line
    text = text.split('\n')
    return str([len(x.split()) for x in text])


data = pd.read_csv("../dataset/poems_dataset.csv")
data = data.sample(frac=1).reset_index(drop=True)[:20000]
data['content'] = data['content'].astype(str).apply(lambda x: to_lines_len(x)) # turn poem into list of line length: [6,8,6,8,6,8...]
data['labels'] = data['genre'].apply(lambda x: label2id[x]) # map labels to number
data_train, data_test = train_test_split(data[['content','labels']],test_size=0.2)
poems = DatasetDict({
    "train": Dataset.from_pandas(data_train),
    "test": Dataset.from_pandas(data_test)
    })


tokenizer = transformers.BertTokenizer.from_pretrained("../modeling/Tokenizer_bert")
def preprocess_function(examples):
    return tokenizer(examples["content"], max_length=64, padding=True, truncation=True)
tokenized_poem = poems.map(preprocess_function, batched=True)

data_collator = transformers.DataCollatorWithPadding(tokenizer=tokenizer)

accuracy = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

model = transformers.BertForSequenceClassification.from_pretrained("../modeling/Model_bert", num_labels=5, ignore_mismatched_sizes=True, id2label=id2label)
model = model.to('cuda:0')

training_args = transformers.TrainingArguments(
    output_dir="../modeling",
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

trainer = transformers.Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_poem["train"],
    eval_dataset=tokenized_poem["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model('../modeling/poem_classifier')
