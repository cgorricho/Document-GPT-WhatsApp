import time
from datetime import datetime
import random
import redis
from ast import literal_eval

from flask import Flask, request

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.twilio_api import send_message

# Incicializa una variable tipo create_conversation --> ConversationalRetrieverChain
qa = create_conversation()

# inicializa un diccionario para llevar la memoria de chat
users_history = {}

# se conecta a un instancia de Redis en Render
redis_external_url = 'rediss://red-cj8obc8eba7s73ea3bc0:h8ccn0CtO07AX2uk0IG2I8kH9mCowkAz@oregon-redis.render.com:6379'
r = redis.from_url(redis_external_url)

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
    
    print('//'*50)
    print('Pregunta inicial: ', sender_id.split(':')[1], query)
    print('*'*50)
    
    # Captura información del usuario
    user = sender_id.split(':')[1]

    # confirma si existe el key de este hash en Redis
    if r.hget(user, 'chat_history'):
        chat_history = [literal_eval(item) for item in str(r.hget(user, 'chat_history')).split('###')]
    else:
        chat_history = []

    # Genera una respuesta a la pregunta
    res = qa(
        {
        'question': query,
        'chat_history': chat_history
        }
    )

    print('Respuesta del modelo: ', res)
    print('*'*50)
    
    print('Largo de la historia: ', len(res['chat_history']))
    print('Largo de la respuesta: ', len(res['answer']))
    
    chat_history.append((query, res['answer']))
    chat_history_redis = '###'.join([str(item) for item in chat_history])
    chat_history_redis = chat_history_redis[-500:]
    separator = chat_history_redis.find('###') + 3
    chat_history_redis = chat_history_redis[separator:]
        
    # users_history[user] = {
    #     'date': datetime.now(),
    #     'chat_history': chat_history,
    # }

    # crea / actualiza chat_history en Redis 
    r.hset(user, mapping={
       'date': str(datetime.now()), 
       'chat_history': chat_history_redis})

    cont = 0                                        # contador de mensajes
    
    for message in res['answer'].split('\n\n'):
        cont += 1
        send_message(sender_id, message)            # utiliza función send_message para enviar mensaje via Twilio
        print('Largo del mensaje ', cont, ': ',     # imprime a la consola
              len(message), sep='')
        print('Mensaje: ', message)
        time.sleep(1 + random.randint(0,2))         # espera un tiempo aleatorio entre 1 y 4 segundos
                                                    # se añade esto para no sobrepasar el rate de Twilio
    
    print('*'*50)
    print('Historia de chat de todos los usuarios: ', r.hgetall(user))
    print('*'*50)

    print('Historia de chat del modelo: ', res['chat_history'])
    print('Historia de chat del usuario: ', chat_history)
    print('*'*50)


    return 'OK', 200
