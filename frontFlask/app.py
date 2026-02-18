from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API = "http://localhost:5000/v1/usarios"

@app.route('/')
def usuarios():
    try:

        response = requests.get("f{API_BASE_URL}usuarios")
    
        if response.status_code == 200:
            usuarios = response.json()

            return render_template('usuarios.html')
    
        else:
            return jsonify({"error":"No se encontraron usuarios"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error":f"Error, no se pudo conectar a la API xddd: {str(e)}"}),500
    
if __name__ == '__main__':
    app.run(debug=True)
