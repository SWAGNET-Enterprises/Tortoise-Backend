from flask import Flask, request, render_template, jsonify
import ggwave
import pyaudio
import cryptocode

app = Flask(__name__)
p = pyaudio.PyAudio()


def modulate(sender=None, recipient=None, message=None, password=None):
    encMessage = cryptocode.encrypt(message, password)
    waveform = ggwave.encode(
        f"{sender}-{recipient}: {encMessage}", protocolId=1, volume=20)

    stream = p.open(format=pyaudio.paFloat32, channels=1,
                    rate=48000, output=True, frames_per_buffer=4096)
    stream.write(waveform, len(waveform)//4)
    stream.stop_stream()
    stream.close()

    p.terminate()


@app.route('/modulate', methods=['POST'])
def api():
    if request.method == 'POST':
        sender = request.json.get('sender', None)
        recipient = request.json.get('recipient', None)
        message = request.json.get('message', None)
        password = request.json.get('password', None)

        return jsonify(modulate(sender=sender, recipient=recipient, message=message, password=password))
