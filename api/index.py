from flask import Flask, request, jsonify,render_template
import requests

app = Flask(__name__)

@app.route('/') 
def index():
    
    return render_template('bot.html')
    
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'Message manquant'}), 400

    try:
        qwen_url = "https://sandipbaruwal.onrender.com/qwen" 
        qwen_response = requests.get(qwen_url, params={"prompt": user_message})
        qwen_response.raise_for_status()  
        qwen_data = qwen_response.json()
        bot_reply = qwen_data.get('answer', "Désolé, je n'ai pas de réponse.")

        return jsonify({'message': bot_reply})

    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête vers Qwen: {e}")
        return jsonify({'error': 'Erreur de communication avec le service de chatbot.'}), 500
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return jsonify({'error': 'Une erreur est survenue.'}), 500
