// this is horrifying, can we avoid it?
var dup_flag = true;

var recording = false;
var audio_context;
var recorder;

function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  // Uncomment if you want the audio to feedback directly
  //input.connect(audio_context.destination);
  recorder = new Recorder(input);
}

function stopRecording() {
    // create WAV download link using audio data blob
    createDownloadLink();
    recorder.clear();
}

function createDownloadLink() {
  recorder && recorder.exportWAV(function(blob) {
    var url = URL.createObjectURL(blob);
    var li = document.createElement('li');
    var au = document.createElement('audio');

    au.controls = true;
    au.src = url;
    li.appendChild(au);
    $('#recordingslist li').length > 0
        ? recordingslist.replaceChild(li, recordingslist.childNodes[0]) 
        : recordingslist.appendChild(li);
  });
}

window.onload = function init() {
  try {
    // webkit shim
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
    window.URL = window.URL || window.webkitURL;
    
    audio_context = new AudioContext;
  } catch (e) {
    alert('No web audio support in this browser!');
  }
  
  navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
  });

  document.getElementById("record_button").addEventListener("click", function() {
        if (dup_flag) {
            recorder && recorder.record();
            if (recording) stopRecording();
            recording = !recording;
        }
        dup_flag = !dup_flag;
    });
};