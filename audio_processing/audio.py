import pyaudio
import wave
import audioop

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio()

print("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get("deviceCount")


# for ii in range(audio.get_device_count()):
    # print(audio.get_device_info_by_index(ii).get("name"))
for i in range(0, numdevices):
    if (
        audio.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels")
    ) > 0:
        print(
            "Input Device id ",
            i,
            " - ",
            audio.get_device_info_by_host_api_device_index(0, i).get("name"),
        )

print("-------------------------------------------------------------")

# exit(0)

index = int(input())
print("recording via index " + str(index))

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=index,
    frames_per_buffer=CHUNK,
)
print("recording started")
Recordframes = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    sound_byte = stream.read(CHUNK)
    Recordframes.append(sound_byte)
    audioop.rms(sound_byte, 2)
print("recording stopped")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b"".join(Recordframes))
waveFile.close()
