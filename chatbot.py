from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Chatbot:

    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    def __init__(self):
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Chatbot is using device: {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
        self.history: list[tuple[str, str]] = []
        self.system_prompt = "<|system|>\nYou are a helpful assistant.<|end|>\n"
        print(f"Model requested: {self.model_name}")
        print(f"Device used: {self.device}")


    def build_prompt(self, new_user_message: str) -> str:
        prompt = self.system_prompt
        for user_msg, assistant_msg in self.history: # add new masssage to the prompt
            prompt += f"<|user|>\n{user_msg}\n<|end|>\n"
            prompt += f"<|assistant|>\n{assistant_msg}\n<|end|>\n"
        
        prompt += f"<|user|>\n{new_user_message}\n<|end|>\n<|assistant|>\n"
        return prompt

    def encode_prompt(self, prompt: str):
        encoded =self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        return encoded
    # Output should be a dictionary with 'input_ids' and 'attention_mask' tensors.
    
    
    def generate_reply(self, prompt: str) -> str:
        user_message = prompt.strip()
        full_prompt = self.build_prompt(user_message)
        
        encoded = self.encode_prompt(full_prompt)
     
        generated_output = self.model.generate(**encoded,
                                                   pad_token_id=self.tokenizer.eos_token_id,  # Prevent EOS warnings
                                                   do_sample=True,       # Enable randomness
                                                   max_new_tokens=100,
                                                   temperature=0.3,      # Adjust creativity
                                                   top_p=0.9,            # Nucleus sampling
                                                   top_k=500)             # Limit choices to top 50 tokens
        
        
        decoded = self.tokenizer.decode(generated_output[0], skip_special_tokens=False)# we need special_token
        assistant_part = decoded.split("<|assistant|>")[-1]
        reply = assistant_part.split("<|end|>")[0].strip()
        self.history.append((user_message,reply))
        
        return reply
    
    def reset_history(self):    
        self.history = []
    

    
