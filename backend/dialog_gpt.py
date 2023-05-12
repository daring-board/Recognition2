'''
https://huggingface.co/docs/transformers/model_doc/blenderbot
'''

from transformers import AutoTokenizer, AutoModelWithLMHead
import torch

class Chatbot:
    def __init__(self):
        model_name = 'microsoft/DialoGPT-small'
        self.model = AutoModelWithLMHead.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def response(self, message, history):
        history = [self.tokenizer(m + tokenizer.eos_token, return_tensors='pt') for m in history]
        for h in history:
            chat_history_ids += h
        new_user_input_ids = self.tokenizer(message + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = self.model.generate(
            bot_input_ids, max_length=512,
            pad_token_id=tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=0.8
        )

        return self.tokenizer.batch_decode(chat_history_ids, skip_special_tokens=True)[0]

if __name__=="__main__":
    cb = Chatbot()

    print("Type \"q\" to quit")
    while True:
        message = input("MESSAGE: ")
        if message in ["", "q", "quit"]:
            break
        res = cb.response(message)
        print(f"Blenderbot 2.0 response: {res}")