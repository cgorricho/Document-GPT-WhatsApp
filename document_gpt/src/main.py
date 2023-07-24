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
    
    #if  len(res['answer']) > 1500:
    send_message(sender_id, res['answer'])

    return 'OK', 200
