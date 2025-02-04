from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def vigenere_cipher(message, key, encrypt=True):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    final_message = ""
    key = key.lower()
    key_index = 0

    for char in message.lower():
        if char not in alphabet:
            final_message += char
            continue

        key_char = key[key_index % len(key)]
        key_offset = alphabet.index(key_char)
        char_index = alphabet.index(char)

        if encrypt:
            new_index = (char_index + key_offset) % len(alphabet)
        else:
            new_index = (char_index - key_offset + len(alphabet)) % len(alphabet)

        final_message += alphabet[new_index]
        key_index += 1

    return final_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data.get("text", "")
    key = data.get("key", "")
    encrypted_text = vigenere_cipher(text, key, True)
    return jsonify({"result": encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    text = data.get("text", "")
    key = data.get("key", "")
    decrypted_text = vigenere_cipher(text, key, False)
    return jsonify({"result": decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
