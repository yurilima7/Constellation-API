import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO
import cv2
import base64
import numpy as np

app = FastAPI()
model = YOLO("best.pt")


ConstellationsPtBr = ["Aquário", "Áries", "Câncer", "Capricórnio", "Gêmeos", "Leão",
                      "Libra", "Peixes", "Sargitário", "Escorpião", "Touro", "Virgem"]


class YoloImg(BaseModel):
    image: str


def verify():
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não foi carregado corretamente.")


verify()


@app.post('/detect')
async def detect_objects(image: YoloImg):
    try:
        # Decodifica a imagem em formato base64
        decoded_image = base64.b64decode(image.image)

        # Converte a imagem para um array NumPy
        nparr = np.frombuffer(decoded_image, np.uint8)
        processed_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Faz a classificação
        results = model.predict(source=processed_image, save=False, imgsz=640, conf=0.7)
        class_names = model.names

        # Processa os resultados
        if len(results[0].boxes.data) > 0:
            detections = results[0].boxes.data[0].numpy()
            # Armazenando as coordenadas
            x_min, y_min, x_max, y_max, conf, cls_index = detections

            # Verificado a classe detectada
            class_name = class_names[cls_index]
            class_name_br = ConstellationsPtBr[int(cls_index)]
            print("Classe: {}, Classe BR: {}".format(class_name, class_name_br))
            percentage = f"{conf * 100:.2f}%"
            print(percentage)
            # Retorno
            return {'nameEn': class_name, 'nameBr': class_name_br, 'percentage': percentage}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
