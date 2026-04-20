import base64
import io
import logging
import os

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel, field_validator
from tensorflow import keras

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Carga del modelo, se realiza solo al iniciar la aplicación y optimiza la inferencia posterior

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "mnist_cnn.keras")

def load_model() -> keras.Model:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo no encontrado en '{MODEL_PATH}'. "
            "Ejecute primero el notebook para entrenar y exportar el modelo."
        )
    logger.info("Cargando modelo desde '%s'...", MODEL_PATH)
    model = keras.models.load_model(MODEL_PATH)
    logger.info("Modelo cargado exitosamente.")
    return model

model: keras.Model = load_model()


# FastAPI Initialization

app = FastAPI(
    title="Clasificación de Imagenes con Dígitos Manuscritos basado en Dataset MNIST",
    description=(
        "Clasifica dígitos manuscritos (0-9) a partir de una imagen "
        "codificada en base64. Modelo CNN entrenado con el dataset MNIST."
    ),
    version="1.0.0",
)

class PredictRequest(BaseModel):
    image_base64: str

    @field_validator("image_base64")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo 'image_base64' no puede estar vacío.")
        return v.strip()


class PredictResponse(BaseModel):
    prediction: str


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("L")                        # escala de grises
    image = image.resize((28, 28), Image.LANCZOS)     # resize a 28×28 (Formato utilizado por el dataset MNIST)
    arr   = np.array(image, dtype="float32") / 255.0  # normalización [0,1]
    arr   = arr.reshape(1, 28, 28, 1)                 # reshape para modelo CNN (batch_size, height, width, channels)
    return arr


# Predict endpoint

@app.post(
    "/predict",
    response_model=PredictResponse,
    summary="Clasificar un dígito manuscrito",
    responses={
        200: {"description": "Predicción exitosa"},
        400: {"description": "Entrada inválida (base64, imagen vacía o formato no válido)"},
        500: {"description": "Error interno del servidor"},
    },
)
async def predict(request: PredictRequest) -> PredictResponse:
    # 1. Decodificar base64
    try:
        image_bytes = base64.b64decode(request.image_base64, validate=True)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="El valor de 'image_base64' no es una cadena base64 válida.",
        )

    # 2. Verificar que no esté vacío después de decodificar
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="La imagen decodificada está vacía.",
        )

    # 3. Abrir imagen con PIL y verificar formato
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))  # reabrir tras verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo abrir la imagen. "
                "Formatos válidos: PNG, JPEG, BMP, TIFF, WEBP."
            ),
        )

    # 4. Preprocesamiento
    try:
        tensor = preprocess_image(image)
    except Exception as exc:
        logger.exception("Error en preprocesamiento: %s", exc)
        raise HTTPException(
            status_code=400,
            detail=f"Error al preprocesar la imagen: {str(exc)}",
        )

    # 5. Inferencia
    try:
        probabilities = model.predict(tensor, verbose=0)
        digit         = int(np.argmax(probabilities, axis=1)[0])
        confidence    = float(np.max(probabilities))
        logger.info("Predicción: %d  |  Confianza: %.2f%%", digit, confidence * 100)
    except Exception as exc:
        logger.exception("Error en inferencia: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Error interno durante la inferencia del modelo.",
        )

    return PredictResponse(prediction=str(digit))


# Health check endpoint

@app.get("/health", summary="Estado de la API")
async def health_check() -> dict:
    return {"status": "ok", "model_loaded": model is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=False)
