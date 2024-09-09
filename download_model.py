from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Specify the model name you want to download, for example, "t5-small"
model_name = "t5-small"

# Download and save the model to the ./llm_model directory
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer files to the specified directory
model.save_pretrained("./llm_model")
tokenizer.save_pretrained("./llm_model")

print("Model and tokenizer have been successfully downloaded and saved to ./llm_model")
