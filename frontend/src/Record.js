import React from "react";
import axios from 'axios';
import ReactAudioPlayer from "react-audio-player";
import ReactPlayer from 'react-player'
import './Record.css';

const Record = () => {
    const [file, setFile] = React.useState([]);
    const [audioState, setAudioState] = React.useState(true);
    const audioRef = React.useRef();
    let [url, setURL] = React.useState(null);
    let [output_url, setOutputURL] = React.useState(null);
    let [video_url, setVideoURL] = React.useState(null);
    let [texts, setTexts] = React.useState([]);

    React.useEffect(() => {
        // マイクへのアクセス権を取得
        navigator.getUserMedia =
          navigator.getUserMedia || navigator.webkitGetUserMedia;
        //audioのみtrue
        navigator.getUserMedia(
          {
            audio: true,
            video: false,
          },
          handleSuccess,
          hancleError
        );
      }, []);

    const hancleError = () => {
        alert("エラーです。");
    };

    const handleSuccess = (stream) => {
        // レコーディングのインスタンスを作成
        audioRef.current = new MediaRecorder(stream, {
          mimeType: "video/webm;codecs=vp9",
        });
        // 音声データを貯める場所
        var chunks = [];
        // 録音が終わった後のデータをまとめる
        audioRef.current.addEventListener("dataavailable", (ele) => {
          if (ele.data.size > 0) {
            chunks.push(ele.data);
          }
          // 音声データをセット
          setFile(chunks);
        });
        // 録音を開始したら状態を変える
        audioRef.current.addEventListener("start", () => setAudioState(false));
        // 録音がストップしたらchunkを空にして、録音状態を更新
        audioRef.current.addEventListener("stop", () => {
          setAudioState(true);
          chunks = [];
        });
    };

    // 録音開始
    const handleStart = () => {
        audioRef.current.start();
    };

    // 録音停止
    const handleStop = () => {
        audioRef.current.stop();
    };

    // firebaseに音声ファイルを送信
    const handleSubmit = () => {
        const blob = new Blob(file)
        console.log(blob)
        url = URL.createObjectURL(blob)
        setURL(url)
        console.log('INPUT Data')
        console.log(url)

        const formData = new FormData();
        formData.append("file", new File([blob], 'recording.wav'))
        setAudioState(true);
        setFile([]);
  
        axios.post('http://127.0.0.1:8000/upload/sound', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(async res => {
            console.log('success')
            console.log(res.data)
            let body = {
              'user_wav_path': res.data.filename, 'history': texts
            }

            await axios.post('http://127.0.0.1:8000/user/response', body, {
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(async res => {
              output_url = 'http://127.0.0.1:8000' + res.data.response_url
              setOutputURL(output_url)
              console.log('OUTPUT Data')
              console.log(output_url)
  
              video_url = 'http://127.0.0.1:8000' + res.data.video_url
              setVideoURL(video_url)
              console.log('Video Data')
              console.log(video_url)

              let tmp = []
              await texts.forEach(element => {
                tmp.push(element)
              });
              tmp.push(res.data.user_uttence + ': user');
              tmp.push('AI: ' + res.data.bot_response);
              setTexts(tmp)
              console.log(tmp)
            }).catch(error =>{
              new Error(error)
            });
        }).catch(error => {
            new Error(error)
        })
    };

    return (
        <div>
            <h1>How to record audio using Web Audio API in JavaScript</h1>
            <div>
                <button onClick={handleStart}>Start</button>
                <button onClick={handleStop} disabled={audioState}>Stop</button>
                <button onClick={handleSubmit} disabled={file.length === 0}>送信</button>
            </div>

            <h2>Input audio</h2>
            <div>
                <ReactAudioPlayer src={url} controls />
            </div>

            <h2>Output audio</h2>
            <div>
                <ReactAudioPlayer src={output_url} controls />
            </div>
            <div>
              <ReactPlayer url={video_url} controls width="100%"/>
            </div>

            <h2>TextContents</h2>
            <div className="chat-area">
              {texts.map((text, index) => {
                if(index % 2 === 1) {
                  return <div key={index} className='text-left'>{text}</div>
                }else{
                  return <div key={index} className='text-right'>{text}</div>
                }
              })}
            </div>
        </div>
    )
}

export default Record;