import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer


load_dotenv()
token = os.getenv("HF_TOKEN")

model_id = "Qwen/Qwen3-8B"
save_path = "./models/llm/Qwen3-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
model = AutoModelForCausalLM.from_pretrained(model_id, token=token)

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
print(f"Model saved to {save_path}")