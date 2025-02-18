from flask import Flask, request, Response
import ollama  # Ensure you have installed the ollama Python package

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # Expecting messages to be a list of dictionaries, e.g.:
    # [{"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there!"}]
    messages = data.get('messages', [])
    
    def generate():
        # Use your local Ollama model; adjust 'llama3.2' as needed.
        stream = ollama.chat(model='llama3.2', messages=messages, stream=True)
        for chunk in stream:
            text = chunk['message']['content']
            yield text
            print(text, end='', flush=True)
    
    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    # Ensure your local Ollama server is running and accessible.
    app.run(debug=True, host='0.0.0.0', port=5000)
