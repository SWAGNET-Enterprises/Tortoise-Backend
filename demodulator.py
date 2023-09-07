import ggwave
import pyaudio
import cryptocode

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32, channels=1,
                rate=48000, input=True, frames_per_buffer=1024)

print('Listening ... Press Ctrl+C to stop')
instance = ggwave.init()


def decrypt(encMessage=None):

try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        res = ggwave.decode(instance, data)
        if (not res is None):
            try:
                decrypt(encMessage=data)
            except:
                pass
except KeyboardInterrupt:
    pass

ggwave.free(instance)

stream.stop_stream()
stream.close()

p.terminate()
