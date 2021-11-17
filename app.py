from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Welcome to API"

@app.route('/huella', methods=['GET'])
def huella():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Imagen"
  f.save(os.path.join('./img', filename)) 

  filename = f"./img/{f.filename}"
  img = cv2.imread(filename, 1)
   
  img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
  YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255, 180, 135))
  
  finger = cv2.bitwise_and(img, img, mask=YCrCb_mask)
  finger = cv2.bitwise_not(finger)

  
  finger = cv2.cvtColor(finger, cv2.COLOR_BGR2GRAY)
  
  finger = cv2.adaptiveThreshold(
      finger, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 1
  )

  cv2.imwrite(f"./files/{f.filename}", finger)

  return f"<h1>Finalizado</h1>"
        

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(port=5000,debug= True)
