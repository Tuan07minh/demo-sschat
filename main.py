import speech_recognition as sr
from flask import Flask, render_template, request
from .chat import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response = ask_question_and_get_response(message)
    cleaned_response = remove_id_flag(response) 
    return cleaned_response

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='vi-VN') 
        response = ask_question_and_get_response(text)
        cleaned_response = remove_id_flag(response) 
        text_to_speech(cleaned_response)
        return cleaned_response
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)

if __name__ == '__main__':
    app.run(debug=True)
