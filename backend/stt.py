import whisper

def stt(data_path, language='en'):
    model = whisper.load_model('small')
    result = model.transcribe(data_path, verbose=True, language=language)
    return result['text']

if __name__=='__main__':
    model = whisper.load_model('medium')

    test_data_path = './data/test_math.mp3'
    result = model.transcribe(test_data_path, verbose=True, language='ja')
    print(result['text'])
    
    # result = model.transcribe(test_data_path, verbose=True, language='ja',task="translate")
    # print(result['text'])