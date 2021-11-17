from flask import Flask, request, jsonify
from secret_service import SecretService
from secrets_model import SecretModel
from flask_cors import cross_origin

app = Flask(__name__)
secretService = SecretService()

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return "Welcome to API"

@app.route('/secretos', methods = ['GET'])
@cross_origin()
def getSecrets():
    response =  jsonify(secretService.getSecrets())
    if response is None:
        return jsonify({"response":"Not found", "status":404})
    return response

@app.route('/secretos', methods = ['POST'])
@cross_origin()
def createUser():
    data  = request.get_json()
    secretsModel = SecretModel()
    secretsModel.__dict__ = data
    response = secretService.createSecrets(secretsModel)
    if response is None:
        return jsonify({"response":"Unprocessable Entity", "status":422})
    return jsonify({"responde":"User creado exitosamente!","status":200})

@app.route('/secretos/<id>', methods = ["GET"])
@cross_origin()
def getById(id):
    if not id:
        return None
    response = secretService.getById(id)
    if response is None:
        return jsonify({"response":"Not found", "status":404})
    return jsonify(response)

@app.route('/secretos', methods = ['DELETE'])
@cross_origin()
def deleteAll():
    response = secretService.deleteAll()
    return jsonify({"responde": "Datos eliminado correctamente", "status":200})

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(port=5000,debug= True)
