'''
https://huggingface.co/docs/transformers/model_doc/blenderbot
'''

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

class Chatbot:
    def __init__(self):
        model_name = "facebook/blenderbot-400M-distill"
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)

    def response(self, message):
        inputs = self.tokenizer([message], return_tensors='pt')
        reply_ids = self.model.generate(**inputs)
        return self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

if __name__=="__main__":
    cb = Chatbot()

    print("Type \"q\" to quit")
    while True:
        message = input("MESSAGE: ")
        if message in ["", "q", "quit"]:
            break
        res = cb.response(message)
        print(f"Blenderbot 2.0 response: {res}")