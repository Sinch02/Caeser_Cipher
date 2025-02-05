from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Vigenère Cipher function
def vigenere(message, key, direction=1):
    key_index = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    final_message = ''

    for char in message.lower():
        if not char.isalpha():  # Keep non-alphabet characters unchanged
            final_message += char
        else:        
            key_char = key[key_index % len(key)]
            key_index += 1

            offset = alphabet.index(key_char)
            index = alphabet.find(char)
            new_index = (index + offset * direction) % len(alphabet)
            final_message += alphabet[new_index]
    
    return final_message

def encrypt(message, key):
    return vigenere(message, key)

def decrypt(message, key):
    return vigenere(message, key, -1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_text():
    data = request.json
    text = data.get("text", "")
    key = data.get("key", "")
    encrypted_text = encrypt(text, key)
    return jsonify({"result": encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt_text():
    data = request.json
    text = data.get("text", "")
    key = data.get("key", "")
    decrypted_text = decrypt(text, key)
    return jsonify({"result": decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
