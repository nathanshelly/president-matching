// this is horrifying, can we avoid it?
var dup_flag = true;
var recorded_once = false;
var audio_context;
var recorder;

function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    config = {
        buffer_len: 4096,
        num_channels: 1,
        mime_type: 'audio/wav'
    };
    recorder = new Recorder(input, config);
}

function startRecording() {
    recorder.record();
    document.getElementById("instructions").innerHTML = "<h3>Click again to stop recording and see your matches<\h3>";
}

function stopRecording() {
    recorder.stop();

    displayAudio();
    recorder.clear();

    document.getElementById("instructions").innerHTML = "<h3>Click the button to start a new recording<\h3>";
}

function displayAudio() {
    recorder && recorder.exportWAV(function (blob) {
        var url = URL.createObjectURL(blob);
        var li = document.createElement('li');
        var au = document.createElement('audio');

        au.controls = true;
        au.src = url;
        li.appendChild(au);
        $('#recordings_list li').length > 0
            ? recordings_list.replaceChild(li, recordings_list.childNodes[0])
            : recordings_list.appendChild(li);
    });
}

window.onload = function init() {
    try {
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
    } catch (e) {
        alert('No web audio support in this browser!');
    }

    navigator.mediaDevices.getUserMedia({ audio: true }).then(startUserMedia);

    document.getElementById("record_button").addEventListener("click", function () {
        if (dup_flag) {
            !recorded_once
                ? recorded_once = true
                : getCSSRule('.recordings_paragraph').style.display = 'initial';

            recorder.recording
                ? stopRecording()
                : startRecording();
        }
        dup_flag = !dup_flag;
    });
};

window.onbeforeunload = function pageClosing() {
    recorder.closeWebSocket();
}

// helpful utility
function getCSSRule(ruleName, deleteFlag) {               // Return requested style obejct
    ruleName = ruleName.toLowerCase();                       // Convert test string to lower case.
    if (document.styleSheets) {                            // If browser can play with stylesheets
        for (var i = 0; i < document.styleSheets.length; i++) { // For each stylesheet
            var styleSheet = document.styleSheets[i];          // Get the current Stylesheet
            var ii = 0;                                        // Initialize subCounter.
            var cssRule = false;                               // Initialize cssRule. 
            do {                                             // For each rule in stylesheet
                if (styleSheet.cssRules) {                    // Browser uses cssRules?
                    cssRule = styleSheet.cssRules[ii];         // Yes --Mozilla Style
                } else {                                      // Browser usses rules?
                    cssRule = styleSheet.rules[ii];            // Yes IE style. 
                }                                             // End IE check.
                if (cssRule) {                               // If we found a rule...
                    if (cssRule.selectorText.toLowerCase() == ruleName) { //  match ruleName?
                        if (deleteFlag == 'delete') {             // Yes.  Are we deleteing?
                            if (styleSheet.cssRules) {           // Yes, deleting...
                                styleSheet.deleteRule(ii);        // Delete rule, Moz Style
                            } else {                             // Still deleting.
                                styleSheet.removeRule(ii);        // Delete rule IE style.
                            }                                    // End IE check.
                            return true;                         // return true, class deleted.
                        } else {                                // found and not deleting.
                            return cssRule;                      // return the style object.
                        }                                       // End delete Check
                    }                                          // End found rule name
                }                                             // end found cssRule
                ii++;                                         // Increment sub-counter
            } while (cssRule)                                // end While loop
        }                                                   // end For loop
    }                                                      // end styleSheet ability check
    return false;                                          // we found NOTHING!
}                                                         // end getCSSRule 