
import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()

def run_model(query: str):
    try:
        # Get Hugging Face token from environment
        hf_token = os.getenv("HF_TOKEN")

        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B", token=hf_token)
        model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3-8B",
            device_map="auto",
            dtype="auto",
            token=hf_token
        )
        gen = pipeline("text-generation", model=model, tokenizer=tokenizer)
        out = gen(query, max_new_tokens=200)
        return out[0]['generated_text']
    except Exception as e:
        return "Model not available locally. Error: " + str(e)
