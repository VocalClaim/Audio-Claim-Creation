from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load model and tokenizer once
model = AutoModelForSeq2SeqLM.from_pretrained('./llm_model')
tokenizer = AutoTokenizer.from_pretrained('./llm_model')

def infer_payload(text):
    try:
        # Handle empty input
        if not text or text.strip() == "":
            return "Input text is empty."

        # Tokenize input and generate output
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(**inputs)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text

    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return "An error occurred during inference."
