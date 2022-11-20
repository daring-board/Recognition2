async function main () {
  try {
    const buttonStart = document.querySelector('#buttonStart')
    const buttonStop = document.querySelector('#buttonStop')
    const audio = document.querySelector('#audio')
    const output_audio = document.querySelector('#output_audio')

    const stream = await navigator.mediaDevices.getUserMedia({ // <1>
      vide: false,
      audio: true,
    })

    const [track] = stream.getAudioTracks()
    const settings = track.getSettings() // <2>

    const audioContext = new AudioContext() 
    await audioContext.audioWorklet.addModule('audio-recorder.js') // <3>

    const mediaStreamSource = audioContext.createMediaStreamSource(stream) // <4>
    const audioRecorder = new AudioWorkletNode(audioContext, 'audio-recorder') // <5>
    const buffers = []

    audioRecorder.port.addEventListener('message', event => { // <6>
      buffers.push(event.data.buffer)
    })
    audioRecorder.port.start() // <7>

    mediaStreamSource.connect(audioRecorder) // <8>
    audioRecorder.connect(audioContext.destination)

    buttonStart.addEventListener('click', event => {
      buttonStart.setAttribute('disabled', 'disabled')
      buttonStop.removeAttribute('disabled')

      const parameter = audioRecorder.parameters.get('isRecording')
      parameter.setValueAtTime(1, audioContext.currentTime) // <9>

      buffers.splice(0, buffers.length)
    })

    buttonStop.addEventListener('click', async event => {
      buttonStop.setAttribute('disabled', 'disabled')
      buttonStart.removeAttribute('disabled')

      const parameter = audioRecorder.parameters.get('isRecording')
      parameter.setValueAtTime(0, audioContext.currentTime) // <10>

      const blob = encodeAudio(buffers, settings) // <11>
      const url = URL.createObjectURL(blob)
      console.log('INPUT Data')
      console.log(url)
      audio.src = url
      await post_blob(blob)

      const download_url = 'http://127.0.0.1:8000/download/response'
      console.log('OUTPUT Data')
      console.log(download_url)
      output_audio.src = download_url

    })
  } catch (err) {
    console.error(err)
  }
}

async function post_blob(blob){
  const formData = new FormData();
  let file = new File([blob], 'recording.wav');
  formData.append("file", file)

  await axios.post('http://127.0.0.1:8000/user/response', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(res => {
      console.log('success')
      console.log(res)
  }).catch(error => {
      new Error(error)
  });
}

main()