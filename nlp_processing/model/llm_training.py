from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset

def preprocess_function(examples, tokenizer):
    inputs = tokenizer(examples['input'], max_length=128, truncation=True)
    targets = tokenizer(examples['target'], max_length=128, truncation=True)
    inputs['labels'] = targets['input_ids']
    return inputs

def train_llm():
    # Load dataset
    dataset = load_dataset('json', data_files={'train': 'train_claims.json', 'test': 'test_claims.json'})

    # Load model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    tokenizer = AutoTokenizer.from_pretrained("t5-small")

    # Tokenize and preprocess dataset
    tokenized_datasets = dataset.map(lambda x: preprocess_function(x, tokenizer), batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./llm_model",
        evaluation_strategy="epoch",
        save_total_limit=1,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=500,
        logging_steps=100,
    )
    
    # Data collator for dynamic padding
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    # Train the model
    trainer.train()
    model.save_pretrained("./llm_model")
    tokenizer.save_pretrained("./llm_model")

if __name__ == "__main__":
    train_llm()
