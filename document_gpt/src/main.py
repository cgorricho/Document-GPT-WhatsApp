import time
import random

from flask import Flask, request

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.twilio_api import send_message

qa = create_conversation()
users_history = {}

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

    # Chequea si hay historia para este usuario
    if user in users_history:
        chat_history = users_history[user]['chat_history']
    else:
        chat_history = ''
        users_history[user] = {
            'date': time.now()
            'chat_history': chat_history
        }

    # TODO
    # get the user
    # if not create
    # create chat_history from the previous conversations
    # question and answer
    # debo terminar esta parte del codigo

    res = qa(
        {
        'question': query,
        'chat_history': chat_history
        }
    )

    print(res)
    print('*'*50)
    
    print('Largo de la historia: ', len(res['chat_history']))
    print('Largo de la respuesta: ', len(res['answer']))
    
    users_history[user] = {
        'date': time.now(),
        'chat_history' = res['chat_history'],
        }

    print(users_history)
    print('*'*50)

    cont = 0
    
    for message in res['answer'].split('\n\n'):
        cont += 1
        send_message(sender_id, message)            # utiliza función send_message para enviar mensaje via Twilio
        print('Largo del mensaje ', cont, ': ',     # imprime a la consola
              len(message), sep='')
        print('Mensaje: ', message)
        time.sleep(1 + random.randint(0,2))         # espera un tiempo aleatorio entre 1 y 4 segundos
                                                    # se añade esto para no sobrepasar el rate de Twilio

    return 'OK', 200
