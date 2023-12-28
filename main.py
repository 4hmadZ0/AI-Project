import os
import openai
import time
import pyaudio
from playsound import playsound
from gtts import gTTS
import speech_recognition as sr


api_key = 'API-KEY'

lang = 'en'

openai.api_key = 'API-KEY'

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    print("Available audio devices:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        print(f"{i}: {device_name}")

    p.terminate()

# Run the function to list audio devices

while True:
    def get_audio(microphone_index):
        r = sr.Recognizer()
        with sr.Microphone(device_index=microphone_index) as source:
            print("Say something!")
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio, language=lang)
                print(said)
                print(f'You said: {said}')

                if 'Hello' in said:
                    completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user','content':said}])
                    text = completion.choices[0].message['content']
                    speech = gTTS(text=text, lang=lang, slow=False)
                    speech.save('welcome1.mp3')
                    playsound.playsound('welcome1.mp3')
                    print('Hello there!')
                if 'goodbye' in said:
                    print('Goodbye Habibi')
            except sr.UnknownValueError as e:
                print(f'Sorry, could not understand.')
            except sr.RequestError as e:
                print(f'Could not request results from Google Speech Recognition service; {e}')
        return said

list_audio_devices()

your_mic_index = int(input('What is your microphone index? '))

while True:
    text = get_audio(your_mic_index)

    if 'goodbye' in text:
        print('Exiting...')
        exit()
