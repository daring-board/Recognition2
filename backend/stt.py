import torch
import whisper

class STT:
    def __init__(self, size='base'):
        self.model = whisper.load_model(size)

    def stt(self, data_path, language='en'):
        result = self.model.transcribe(data_path, verbose=True, language=language)
        return result['text']

if __name__=='__main__':
    stt = STT('medium')

    test_data_path = './data/test_math.mp3'
    result = stt.stt(test_data_path, verbose=True, language='ja')
    print(result['text'])
    
    # result = model.transcribe(test_data_path, verbose=True, language='ja',task="translate")
    # print(result['text'])