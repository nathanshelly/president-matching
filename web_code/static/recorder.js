(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.Recorder = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
"use strict";

module.exports = require("./recorder").Recorder;

},{"./recorder":2}],2:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.Recorder = undefined;

var _createClass = function () {
    function defineProperties(target, props) {
        for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
        }
    }return function (Constructor, protoProps, staticProps) {
        if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
    };
}();

var _inlineWorker = require('inline-worker');

var _inlineWorker2 = _interopRequireDefault(_inlineWorker);

function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : { default: obj };
}

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

var Recorder = exports.Recorder = function () {
    function Recorder(source, cfg) {
        var _this = this;

        _classCallCheck(this, Recorder);

        this.recording = false;
        this.config = {
            buffer_len: 4096,
            num_channels: 2,
            mime_type: 'audio/wav'
        };
        this.callbacks = {
            getBuffer: [],
            exportWAV: [],
        };

        Object.assign(this.config, cfg);
        this.context = source.context;
        this.node = (this.context.createScriptProcessor || this.context.createJavaScriptNode).call(this.context, this.config.buffer_len, this.config.num_channels, this.config.num_channels);

        this.node.onaudioprocess = function (e) {
            if (!_this.recording) return;

            var buffer = [];
            for (var channel = 0; channel < _this.config.num_channels; channel++) {
                buffer.push(e.inputBuffer.getChannelData(channel));
            }

            _this.worker.postMessage({
                command: 'record',
                buffer: buffer
            });
        };

        source.connect(this.node);
        this.node.connect(this.context.destination); //this should not be necessary

        var self = {};
        this.worker = new _inlineWorker2.default(function () {
            var rec_length = 0,
                rec_buffers = [],
                sample_rate = void 0,
                num_channels = void 0,
                ws = void 0;

            this.onmessage = function (e) {
                switch (e.data.command) {
                    case 'init':
                        init(e.data.config);
                        break;
                    case 'record':
                        record(e.data.buffer);
                        break;
                    case 'done_recording':
                        sendEndMessage(e);
                        break;
                    case 'close_websocket':
                        closeWebSocket();
                        break;
                    case 'exportWAV':
                        exportWAV(e.data.type);
                        break;
                    case 'getBuffer':
                        getBuffer();
                        break;
                    case 'clear':
                        clear();
                        break;
                }
            };

            function init(config) {
                sample_rate = config.sample_rate;
                num_channels = config.num_channels;
                initBuffers();
                initWebSocket();
            }

            function record(input_buffer) {
                for (var channel = 0; channel < num_channels; channel++) {
                    rec_buffers[channel].push(input_buffer[channel]);
                }
                rec_length += input_buffer[0].length;

                var msg = {
                    type: "recording",
                    text: 'chunk',
                    data: input_buffer[0]
                };

                ws.send(JSON.stringify(msg));
            }

            function closeWebSocket() {
                ws.close();
            }

            function sendEndMessage(e) {
                var msg = {
                    type: "recording",
                    text: 'done'
                };
                ws.send(JSON.stringify(msg));
            }

            function exportWAV(type) {
                var buffers = [];
                for (var channel = 0; channel < num_channels; channel++) {
                    buffers.push(mergeBuffers(rec_buffers[channel], rec_length));
                }
                var interleaved = void 0;
                if (num_channels === 2) {
                    interleaved = interleave(buffers[0], buffers[1]);
                } else {
                    interleaved = buffers[0];
                }
                var dataview = encodeWAV(interleaved);
                var audio_blob = new Blob([dataview], { type: type });

                this.postMessage({ command: 'exportWAV', data: audio_blob });
            }

            function getProcessingResults() {

            }

            function getBuffer() {
                var buffers = [];
                for (var channel = 0; channel < num_channels; channel++) {
                    buffers.push(mergeBuffers(rec_buffers[channel], rec_length));
                }
                this.postMessage({ command: 'getBuffer', data: buffers });
            }

            function clear() {
                rec_length = 0;
                rec_buffers = [];
                initBuffers();
            }

            function initBuffers() {
                for (var channel = 0; channel < num_channels; channel++) {
                    rec_buffers[channel] = [];
                }
            }

            function mergeBuffers(rec_buffers, rec_length) {
                var result = new Float32Array(rec_length);
                var offset = 0;
                for (var i = 0; i < rec_buffers.length; i++) {
                    result.set(rec_buffers[i], offset);
                    offset += rec_buffers[i].length;
                }
                return result;
            }

            function interleave(input_left, input_right) {
                var length = input_left.length + input_right.length;
                var result = new Float32Array(length);

                var index = 0,
                    input_index = 0;

                while (index < length) {
                    result[index++] = input_left[input_index];
                    result[index++] = input_right[input_index];
                    input_index++;
                }
                return result;
            }

            function floatTo16BitPCM(output, offset, input) {
                for (var i = 0; i < input.length; i++, offset += 2) {
                    var s = Math.max(-1, Math.min(1, input[i]));
                    output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
                }
            }

            function writeString(view, offset, string) {
                for (var i = 0; i < string.length; i++) {
                    view.setUint8(offset + i, string.charCodeAt(i));
                }
            }

            function encodeWAV(samples) {
                var buffer = new ArrayBuffer(44 + samples.length * 2);
                var view = new DataView(buffer);

                /* RIFF identifier */
                writeString(view, 0, 'RIFF');
                /* RIFF chunk length */
                view.setUint32(4, 36 + samples.length * 2, true);
                /* RIFF type */
                writeString(view, 8, 'WAVE');
                /* format chunk identifier */
                writeString(view, 12, 'fmt ');
                /* format chunk length */
                view.setUint32(16, 16, true);
                /* sample format (raw) */
                view.setUint16(20, 1, true);
                /* channel count */
                view.setUint16(22, num_channels, true);
                /* sample rate */
                view.setUint32(24, sample_rate, true);
                /* byte rate (sample rate * block align) */
                view.setUint32(28, sample_rate * 4, true);
                /* block align (channel count * bytes per sample) */
                view.setUint16(32, num_channels * 2, true);
                /* bits per sample */
                view.setUint16(34, 16, true);
                /* data chunk identifier */
                writeString(view, 36, 'data');
                /* data chunk length */
                view.setUint32(40, samples.length * 2, true);

                floatTo16BitPCM(view, 44, samples);

                return view;
            }

            function passAlongData(data) {
                this.postMessage({command: 'displayPredictions', data: data});
            }

            function initWebSocket() {
				// webworker doesn't have access to window.location.hostname, this is workaround
				parts = self.location.origin.split('/') 
                ws = new WebSocket('wss://' + parts[parts.length - 1] + '/websocket');
                ws.binaryType = 'arraybuffer';

                ws.onclose = function (close_event) {
                    console.log('socket closed');
                };

                ws.onopen = function (open_event) {
                    console.log('socket opened');
                };

                ws.onmessage = function(message) {
                    if(message.data != 'None') {
                        console.log('received a message');
                        console.log(message);
                        decoded_data = JSON.parse(message.data)
                        if(decoded_data['type'] == 'result') {
                            passAlongData(decoded_data);
                        }
                    }
                };

                ws.onerror = function (error_event) {
                    console.log('Whoops... that\'s an error');
                    console.log(error_event);
                };
            }
        }, self);

        this.worker.postMessage({
            command: 'init',
            config: {
                sample_rate: this.context.sampleRate,
                num_channels: this.config.num_channels
            }
        });

        this.worker.onmessage = function (e) {
            if(e.data.command == 'displayPredictions') {
                console.log(this);
                _this.displayPredictions(e.data.data);
            }
            else {
                var cb = _this.callbacks[e.data.command].pop();
                if (typeof cb == 'function') {
                    cb(e.data.data);
                }
            }
        };
    }

    // END OF CONSTRUCTOR

    _createClass(Recorder, [{
        key: 'record',
        value: function record() {
            this.recording = true;
        }
    }, {
        key: 'stop',
        value: function stop() {
            this.recording = false;
            this.worker.postMessage({ command: 'done_recording' });
        }
    }, {
        key: 'clear',
        value: function clear() {
            this.worker.postMessage({ command: 'clear' });
        }
    }, {
        key: 'closeWebSocket',
        value: function closeWebSocket() {
            this.worker.postMessage({ command: 'close_websocket' });
        }
    }, {
        key: 'getBuffer',
        value: function getBuffer(cb) {
            cb = cb || this.config.callback;
            if (!cb) throw new Error('Callback not set');

            this.callbacks.getBuffer.push(cb);

            this.worker.postMessage({ command: 'getBuffer' });
        }
    }, {
        key: 'exportWAV',
        value: function exportWAV(cb, mime_type) {
            mime_type = mime_type || this.config.mime_type;
            cb = cb || this.config.callback;
            if (!cb) throw new Error('Callback not set');

            this.callbacks.exportWAV.push(cb);

            this.worker.postMessage({
                command: 'exportWAV',
                type: mime_type
            });
        }
    }, {
        key: 'displayPredictions',
        value: function displayPredictions(data) {
            var top_five = data.probs.slice(-5).reverse();

            var prediction = document.getElementById('prediction');
            prediction.innerHTML = '</h3>Congratulations, you sound most like: ' + this.capitalizeFirstLetter(data.pred) + '</h3>'

            var predictions_node = document.getElementById('predictions_list');
            // if there are results currently, remove them
            while (predictions_node.firstChild) {
                predictions_node.removeChild(predictions_node.firstChild);
            }

            for (var index in top_five) {
                var temp_node = document.createElement('li');
                temp_node.innerText = this.capitalizeFirstLetter(top_five[index][0]) + ': ' + top_five[index][1].toFixed(2) + '%'
                predictions_node.appendChild(temp_node);
            }

            console.log(data);
            console.log(prediction);
            console.log(top_five);
        }
    }, {
        key: 'capitalizeFirstLetter',
        value: function capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
    }]);

    return Recorder;
}();

exports.default = Recorder;

},{"inline-worker":3}],3:[function(require,module,exports){
"use strict";

module.exports = require("./inline-worker");
},{"./inline-worker":4}],4:[function(require,module,exports){
(function (global){
"use strict";

var _createClass = (function () { function defineProperties(target, props) { for (var key in props) { var prop = props[key]; prop.configurable = true; if (prop.value) prop.writable = true; } Object.defineProperties(target, props); } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

var _classCallCheck = function (instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } };

var WORKER_ENABLED = !!(global === global.window && global.URL && global.Blob && global.Worker);

var InlineWorker = (function () {
  function InlineWorker(func, self) {
    var _this = this;

    _classCallCheck(this, InlineWorker);

    if (WORKER_ENABLED) {
      var functionBody = func.toString().trim().match(/^function\s*\w*\s*\([\w\s,]*\)\s*{([\w\W]*?)}$/)[1];
      var url = global.URL.createObjectURL(new global.Blob([functionBody], { type: "text/javascript" }));

      return new global.Worker(url);
    }

    this.self = self;
    this.self.postMessage = function (data) {
      setTimeout(function () {
        _this.onmessage({ data: data });
      }, 0);
    };

    setTimeout(function () {
      func.call(self);
    }, 0);
  }

  _createClass(InlineWorker, {
    postMessage: {
      value: function postMessage(data) {
        var _this = this;

        setTimeout(function () {
          _this.self.onmessage({ data: data });
        }, 0);
      }
    }
  });

  return InlineWorker;
})();

module.exports = InlineWorker;
}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{}]},{},[1])(1)
});
