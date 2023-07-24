import time
import random

from flask import Flask, request

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.twilio_api import send_message

qa = create_conversation()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

@app.route('/twilio', methods=['POST'])
def twilio():
    query = request.form['Body']
    sender_id = request.form['From']
    print(sender_id, query)
    print('*'*50)
    # TODO
    # get the user
    # if not create
    # create chat_history from the previous conversations
    # question and answer

    res = qa(
        {
        'question': query,
        'chat_history': {}
        }
    )

    print(res)
    print('*'*50)
    
    print('Largo de la respuesta: ', len(res['answer']))
    cont = 0
    
    for message in res['answer'].split('\n\n'):
        cont += 1
        send_message(sender_id, message)
        print('Largo del mensaje ', cont, ': ', len(res['answer']), sep='')
        time.sleep(1 + random.randint(0,3))

    return 'OK', 200
