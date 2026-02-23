import torch
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from .schemas.logger import Logger


class LLM:
    def __init__(
        self,
        model_name: Optional[str],
        device: Optional[str] = None,
        max_new_tokens: int = 256,
        temperature: float = 0.2
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        # Quantisation for using 4-bit configuration
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,  # or bfloat16 for RTX 30/40/50 series
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        # Initialise tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16 if self.device == "cuda" else torch.float32,
            quantization_config=quant_config,
            local_files_only=True  # Force to find local files for now
        ).to(self.device)

        Logger.info("LLM", f"Model Initialised on {self.device}.")


    def build_prompt(self, system_prompt, user_input):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        if hasattr(self.tokenizer, "apply_chat_template"):
            return self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False  # TODO
            )
        
        # Fallback response
        return f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    

    def clean_qwen_response(self, response):
        try:
            # Extract main response portion
            response = response.split("</think>")[-1]

            # Clean up special characters
            return response.strip()

        except Exception as e:
            Logger.error("LLM", f"Error cleaning LLM response due to {e}")
            return None
    

    def generate(self, system_prompt, user_input, temperature=None):
        try:
            Logger.debug("LLM", "Generating LLM response.")

            prompt = self.build_prompt(system_prompt, user_input)

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt"
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    temperature=temperature if temperature else self.temperature,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            generated = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            response = self.clean_qwen_response(generated)
            
            if response:
                return response
            return '{"action": "respond", "parameters": {}}'

        except Exception as e:
            Logger.error("LLM", f"Error generating response due to {e}")
            return '{"action": "respond", "parameters": {}}'
        