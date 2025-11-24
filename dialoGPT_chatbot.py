# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# class Chatbot:

#     model_name = "microsoft/DialoGPT-small"

#     def __init__(self):
        
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         print(f"Chatbot is using device: {self.device}")
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
#         self.chat_history_ids = None
#         self.system_prompt = "You are a helpful assistant. Respond to the end of this conversation accordingly.\n"
#         print(f"Model requested: {self.model_name}")
#         print(f"Device used: {self.device}")


#     def encode_prompt(self, prompt: str):
#         encoded =self.tokenizer(prompt, return_tensors="pt").to(self.device)
#         return encoded
#     # Output should be a dictionary with 'input_ids' and 'attention_mask' tensors.
    
#     def decode_reply(self, reply_ids: list[int]) -> str:
#         decode = self.tokenizer.decode(reply_ids, skip_special_tokens=True)
#         return decode
#     # Pass in a string of generated token IDs here from your tokenizer
#     # output really words "gjhgkjhg"

#     def generate_reply(self, prompt: str) -> str:
#         prompt = prompt+"\n"
        
#         #encoded has 2 part: input_ids, attention_mask(both have class 'torch.Tensor', shape like nested lists) )
#         encoded_self_system_prompt = self.encode_prompt(self.system_prompt)
#         encoded = self.encode_prompt(prompt)
        
#         if self.chat_history_ids == None:
#             # Type: torch.Tensor
#             self.chat_history_ids = torch.cat([encoded_self_system_prompt["input_ids"], encoded["input_ids"]], dim=1).to(self.device)   
#             # self.chat_history_ids is tensor
#             #shape of tensor(1,5) (batch_size=1 (#num of rows), (#довжина послідовності = 5 (len of total_history_length )        
#             old_history_len = self.chat_history_ids.shape[1] # get only sequence
            
#         else:
#             self.chat_history_ids = torch.cat([self.chat_history_ids, 
#                                                 encoded["input_ids"]], # or encoded.get("input_ids")
#                                                 dim=1).to(self.device) 
#             # self.chat_history_ids is tensor
#             #shape of tensor(1,5) (batch_size=1 (#num of rows), (#довжина послідовності = 5 (len of total_history_length )        
#             old_history_len = self.chat_history_ids.shape[1] # get only sequence
           
#         # Mask must be same shape as chat_history_ids and filled with 1s (no padding)
#         attention_mask = torch.ones_like(self.chat_history_ids).to(self.device)

#         generated_output_ids = self.model.generate(input_ids = self.chat_history_ids,
#                                                    attention_mask=attention_mask,
#                                                    pad_token_id=self.tokenizer.eos_token_id,  # Prevent EOS warnings
#                                                    do_sample=True,       # Enable randomness
#                                                    temperature=0.9,      # Adjust creativity
#                                                    top_p=0.8,            # Nucleus sampling
#                                                    top_k=500)             # Limit choices to top 50 tokens
        
#         # generated_output_ids is a tensor with shape: tensor.shape(x,y) (batch_size=x (#num of rows), (#довжина послідовності = y (len of послідовності)
#         # generated_output_ids: output looks like [[10, 20, 30],[15, 23, 46]](nested lists)
#         self.chat_history_ids = generated_output_ids
        
#         # get only new reply(new generated token)
#         # new token = first nested list, where len = slice: from <old_history_len> to <:>
#         new_token = self.chat_history_ids[0][old_history_len:]
#         output_ids = new_token.tolist() 
#         reply = self.tokenizer.decode(output_ids, skip_special_tokens=True)
       
#         return reply
    
#     def reset_history(self):    
#         self.chat_history_ids = None
    

    
