import time
import random

from flask import Flask, request

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.twilio_api import send_message

qa = create_conversation()

app = Flask(__name__)

# crea el endpoint estandar
@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

# crea el endpoint (o ruta) a través de la cual se reciben y envían mensajes via Twilio
@app.route('/twilio', methods=['POST'])
def twilio():
    # Recibe mensaje de Whatsapp via Twilio
    query = request.form['Body']
    sender_id = request.form['From']
    print(sender_id.split(':')[1], query)
    print('*'*50)
    
    # Captura información del usuario
    user = sender_id.split(':')[1]

    # TODO
    # get the user
    # if not create
    # create chat_history from the previous conversations
    # question and answer
    # debo terminar esta parte del codigo

    res = qa(
        {
        'question': query,
        'chat_history': {}
        }
    )

    # print(res)
    # print('*'*50)
    
    print('Largo de la historia: ', len(res['chat_history']))
    print('Largo de la respuesta: ', len(res['answer']))
    
    cont = 0
    
    for message in res['answer'].split('\n\n'):
        cont += 1
        send_message(sender_id, message)
        print('Largo del mensaje ', cont, ': ', len(message), sep='')
        print('Mensaje: ', message)
        time.sleep(1 + random.randint(0,3))

    return 'OK', 200
