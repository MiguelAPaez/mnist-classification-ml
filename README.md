# Clasificación de Imagenes con Dígitos Manuscritos basado en Dataset MNIST

El presente repositorio utiliza la metodología y estándar de ciencia de datos y míneria de datos: **CRISP-DM**, para la construcción de un pipeline completo de Machine Learning en un modelo de clasificación de dígitos manuscritos por medio del dataset MNIST: desde el entrenamiento hasta el consumo vía API REST del modelo creado.

---

## Estructura del proyecto

```
mnist-classification-ml/
├── .venv/                       # Ambiente virtual (creado localmente, no cargado en git)
├── .gitignore                   # Excluye .venv y caché del proyecto
├── mnist_classification.ipynb   # Notebook de clasificación completo
├── requirements.txt             # Dependencias del proyecto
├── README.md                    
└── api/
    ├── main.py                  # API creada con FastAPI — endpoint /predict
    └── model/
        └── mnist_cnn.keras      # Modelo exportado (generado por el notebook del proyecto)
```

---

## Requisitos previos

- Python 3.9 o superior
- pip

> Se recomienda usar un **ambiente virtual** para aislar las dependencias del proyecto y no afectar la instalación global de Python en la máquina donde se corra.

### Crear y activar el ambiente virtual

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD)**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Una vez activado, la terminal mostrará el prefijo `(.venv)`.  
Para desactivar el ambiente en cualquier momento escribir el comando: `deactivate` en la terminal

### Instalar dependencias

Con el ambiente virtual **activado**:

```bash
pip install -r requirements.txt
```

---

## 1. Cómo ejecutar el Notebook

> Tener el ambiente virtual **activado** antes de continuar.

### Jupyter Lab / Notebook (navegador - Chrome)

```bash
# Desde la raíz del proyecto
jupyter notebook mnist_classification.ipynb
```

Jupyter se abrirá en el navegador usando directamente el ambiente y las dependencias configuradas en el ambiente virtual (.venv).

### Pasos dentro del notebook

1. Ejecutar todas las celdas en orden (`Run All`)
2. El notebook sigue las 6 fases de CRISP-DM, cada una marcada con un encabezado
3. La primera ejecución descarga automáticamente el dataset MNIST (~11 MB) en la raíz del proyecto

---

## 2. Cómo exportar el modelo

El modelo se exporta **automáticamente** al ejecutar la última sección del notebook ("FASE 6 — Deployment"), generando el archivo `api/model/mnist_cnn.keras` que la API posteriormente cargará al iniciar.

> **Nota:** La carpeta `api/model/` ya existe en la estructura del proyecto. Si no existe, el notebook la creará automáticamente.

---

## 3. Cómo levantar la API

> **Requisitos:**
> - El ambiente virtual debe estar **activado**
> - El modelo debe estar exportado en `api/model/mnist_cnn.keras` (generado por el notebook)

### Desde la raíz del proyecto

Ejecutar el siguiente comando:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8002 --reload
```

### Salida esperada en consola al iniciar

```
INFO | Cargando modelo desde 'api/model/mnist_cnn.keras'...
INFO | Modelo cargado exitosamente.
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

---

## 4. Ejemplo de consumo del endpoint

### cURL de la petición

Para utilizar este curl hacer un import en Postman con el siguiente bloque de código; tener en cuenta que primero deberá estar inicializado el servidor para lanzar una petición

```bash
curl --location 'http://localhost:8002/predict' \
--header 'Content-Type: application/json' \
--data '{
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABIElEQVR4nLWSvUoDQRSFz53ZxLAo+Aum0EIU20CIhQ8QBTsfIY3gC/gMPkMwhS9gk1psBQkKQoIiu4VFIFELoxh15sguMX87goV+zZ2ZbwbOzB3gX5CxCX/YpzQArdwOSM2k4+pwK+VG8+Zo1WEV8i1GtDcSViRTp61VQjKYkpGUgMY27fkEFuqGJXiDGBGCHKXanWyVFXf691G9ijRgFfQDZF0ZGZOhsGg7ZguY8zGKINsxrO4f0/JpFolEe/FN+MHHhIRG6c7Yy4NX3vsJGZHLe5tkra+870FmbentFCiC1/Q+MYzCcpfPi8gGhruDE+hZOeN7oxJYXqQSL69ReInT3rraIiichM2rw3lnVAX40+JuNqCiZW/43G8/2F/yBTiQaDCaLoihAAAAAElFTkSuQmCC"
}'
```

### Body de la petición

```json
{
  "image_base64": "<cadena base64 de la imagen>"
}
```

### Respuesta exitosa

```json
{
  "prediction": "7"
}
```

---

### Ejemplo de imágenes en base64 para hacer pruebas con la API


| Dígito | Base64 |
|--------|--------|
| 0 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA/0lEQVR4nL2SvUoDURCFv5m7JqKBiEYrG7HwNbSzUrCwsEhtIfgAvojY2dhbaGVhGaxsbYQgGAujEETDxr0jq9kId38q8RTDhQ/m3Dkz8A8SKUUO0LQUa24WtKijcnDT616sF1Hl2FL5re/2gd+mxcOza29Pzdy3HOfejqDjrU0UONJ4tNGq49D86QRqBpeXeHlO5B5ZIwlhy/H2ITaAhcjGppo1noFRIsQwXfudoEKaPd4hckYNhnEAjVdPo27ShP6nWAAf+swvOlvB7iYR6Rjq4NZP7SXsmlzlvCN2yuNDOfkJfjsffLqy/U6ve7lRPJ2ULzvdjFSeScWB/aG+AICqVv139L7YAAAAAElFTkSuQmCC |
| 1 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAAsklEQVR4nGNgoAlgxOD+J14pAjD+52f6/oMBK2BhMH/9LpeBBUkABhhZfnNNF2HgggswMDDBWf9/y+8w/Pn/LxZJRkbBvFO2DMyMjFgkmf8nThT7cx9hEKqxbAxvApdhl/zP8HGh6RZeFDm4a/8yzJrOwPwPVZIJzvrLzIbsUmSdDAwMf9ECD1knFsBEtiQLCu//X5ToRJXkYGZgwyH5n+HWKYZHuJMCKkD1G4hHpEZaAQB+/SgQTdfLLgAAAABJRU5ErkJggg== |
| 2 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABA0lEQVR4nGNgoANgZMQpwwIiWbDKMzEwMPDzgRRh0ccg1nH++dNTVRyYskyMSnf/g8FBHgybmRg2/P/5duH6Xz/+tzCwoMsp/f//w5CBIe//36tMaDqZGAyO3trEwMas8Of/fTYsbmLhYGRhtP/37zgWOSYGBkZmhp3//hej2wkGTMwMU///v8WDbicIMDIxzPz/74sxODjQACMT09L//z46MjBjkWNmWvX//ysLBjYsGpkZ5vz/fVUGRYwFJvc3Pfk300QR+d8Mvy79QzOUUeDl799//oEC9yk86KE6mf9EiMEUsqIb+59B4ORfFob/DAz/GV+imYoDIAIDwfpPlE4aAQBpwFQlokBQiQAAAABJRU5ErkJggg== |
| 3 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABDklEQVR4nGNgoAlgROP8x6WOmYGBgYkZlxmMAlwMDExY5UR7Lr+4v8EOiywjo9TN/yDwL5wBw2Rmhtn/fz2Zd/rfv4/ijIzohgp++/9ZnoH93L//4QwsUFEWCPWf4aeP3oeHHD9uG2CaCgGMDI7v/3+TxuIkZjZmnfO//z/zx+oZFobY////rhFGDTUoYGEMXbDx//+X+owYWhkhIqX//h/GlGRgYGJlYmUS/vzvqxTMViYYZbHr6uR/zAwsTIyMLOi6GPT///+sx8DQ/P/vLVb0IGJiWPv/97uFO///+p+JEQxMjJKXwAH/fxq2aGHgb7nw4tGeCAYmLP4ECQnwoCUchCzIlSjJhNgERk0AAPKmVzsMSLdmAAAAAElFTkSuQmCC |
| 4 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA9klEQVR4nL2Su2oCQRiFz1wkJGKhBAKCTUiZylcQTeMLhFjbB2vbENJul5AqD2IloqU2eQFTaBRMYUR358iGjLO7TCCVXzH89/8wM8DxEWlXguD/SlNIVPvDDhQ8CHUyIZ+hXbFDRY/X6+g7EXEo1LnbMfB1ShZfIVNSpbNMUFkGXjHQuCXbDSbHWqSoLNjHHRmI3CGIX/hSWrRgAMMok1Tm/sY8zIt54DQ+UgiMtpvp52xFfs26dqu26bMcyj9GoXBhY9oab5dGSHNVw3jQi1d7aIbhk/MOnUoAOjxXKGm5zSZj/Yw+RngP/beUJfv2An9+k+OwB+y0S/RCIykxAAAAAElFTkSuQmCC |
| 5	|iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABD0lEQVR4nMWRIU8DQRCF3ewuJCUcCSgEJBDSEH4ACgnBY9AYUofsX6gBgcOA5AeAQ6JQIAppqhuaQnJ1Selxt4+0Zfd6exgE4TMzmbezM28X+BPkh5y/7TTRJCaD0imDo/57HMdv8RW0r3m2FydxyVeMSyy2mA4sUtMviWIrG9LZSRSyBFkocnUZTz0UUE7E5iwXLh5ujnXB+xiDejbkiLtIharGLcnHFw556a04BGfPrT2oE5t+rvlhBQRokgduTeXr8yvrGlp3we9n9ChUOx/dUUOb3A2Gisy9kqczUrdZL5JgXY0aE7aaTFkrbQuF87FNNnItv0C4f1i17et7ZcPGfPEpj9OjNQhF9yX/xBebtWDXnOTKIwAAAABJRU5ErkJggg== |
| 6 | iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABH0lEQVR4nLWSPy9EQRTFz50ZsskLsYRKQciWim02dEiUGl+CUqWk1dleQih8gO21S4FIFFYlm2DjXyIsm/XeHJl9eSuZt6/jNpOZ35x7z70zwL+E+DtmXFQagJbeDOjPGz9ZHAozB7VGbSffgyosf9LF2YD4VMlkk6zuv3xxE8aDBmVGFY0l8lJ5SoG5sZwHsLJQSGXFRItvuZFSIWUG0CiR1xv3bFVnXU8eXKT97rj9KHap+q1qTXN7/coGZb+mxhzbXAVGH204nUhUvBDPYR+PTe7pXPR4MiOVwPoDZTAUd95O2z2kPRJMvUbvY/50lRRtxJO9u5C7cE/nSdc6nfB02B9f3GrltnGxFWQ8KIKh1M/pap1105s5USb5y/gBX1FlOxbVZvMAAAAASUVORK5CYII= |
| 7 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA0ElEQVR4nGNgoD9gxML6T4pOpn/mE/9D2Izfw14x/QMzWWBqhMzhGjhhDBYYA6KW4RcT05svjP9RjGX8z6/OwMDI9GuC1X/f7cx/sToh4Pf/RgZmTJcxM7OwSLz9f4mVGeEpJMDMMPH/f08sGhkYGJgY5L78PYxdjoGFoeX//1CE+5EBIwPH3X9PuBlw2Oj4//98FFOZkHS6MzDsZsSqkYGJ4cD/XxpIqlGs5Hzw55ILu5VMDAr//1/DlUNyOONx5gsMsDAnjAUCATFKKTOYy90a7AAAAABJRU5ErkJggg== |
| 8 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABG0lEQVR4nGNgoAlgROP8x6WOGUZgNYNJgBfNLChgZJCacuXFo8OpDEwY0oyMMnf/g8F0BiZ0SWaG2f9/Xyto/fT7vx0Dmr2MDEzX/35VZ2Ao//+3iYEFKsqEMJfh4x0WxktIQkjGzvj/L5mBe91/TGMZGBkl9v75f+b2/88NWLW6f/j///+f8xLYXBv29//7hZv+/X+hzogmy8jI++z/FxMGhoJ//zejazVmcPj/bzsDOxPPm39vBGBByASTFvjP+JuBken/X0ZWdjQrmRj0/v99J8vA4Pfv721WRrTQZWI68v/PzaKGN7/+18FDCKFV9Q4k4LdzYIkWBtG2s8+fHi9iwRajIKfx86GnHLhekFWMLFjlIGGBS4aaAAAcYWL54o708QAAAABJRU5ErkJggg== |
| 9 |	iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABIElEQVR4nLWSvUoDQRSFz53ZxLAo+Aum0EIU20CIhQ8QBTsfIY3gC/gMPkMwhS9gk1psBQkKQoIiu4VFIFELoxh15sguMX87goV+zZ2ZbwbOzB3gX5CxCX/YpzQArdwOSM2k4+pwK+VG8+Zo1WEV8i1GtDcSViRTp61VQjKYkpGUgMY27fkEFuqGJXiDGBGCHKXanWyVFXf691G9ijRgFfQDZF0ZGZOhsGg7ZguY8zGKINsxrO4f0/JpFolEe/FN+MHHhIRG6c7Yy4NX3vsJGZHLe5tkra+870FmbentFCiC1/Q+MYzCcpfPi8gGhruDE+hZOeN7oxJYXqQSL69ReInT3rraIiichM2rw3lnVAX40+JuNqCiZW/43G8/2F/yBTiQaDCaLoihAAAAAElFTkSuQmCC |

---

## 5. Manejo de errores

| Caso | Status HTTP | Mensaje |
|------|-------------|---------|
| base64 inválido | 400 | "El valor de 'image_base64' no es una cadena base64 válida." |
| Imagen vacía | 400 | "La imagen decodificada está vacía." |
| Formato no soportado | 400 | "No se pudo abrir la imagen. Formatos válidos: PNG, JPEG, BMP, TIFF, WEBP." |
| Error de preprocesamiento | 400 | "Error al preprocesar la imagen: ..." |
| Error interno | 500 | "Error interno durante la inferencia del modelo." |

---

## 6. Detalles técnicos del modelo

| Aspecto | Detalle |
|---------|---------|
| Arquitectura | CNN con 2 bloques Conv2D + BatchNorm + MaxPool + Dropout |
| Dataset | MNIST (60k train / 10k test) |
| Accuracy esperada | ≥ 99% en test |
| Framework | TensorFlow / Keras |
| Formato exportado | `.keras` (TF2 nativo) |
| Anti-overfitting | BatchNormalization + Dropout(0.25/0.5) + EarlyStopping |

---

## 7. Flujo completo de la solución

```
Notebook ML
    │
    ├─ 1. Carga MNIST
    ├─ 2. Exploración de datos
    ├─ 3. Preprocesamiento (normalización + reshape)
    ├─ 4. Entrenamiento CNN
    ├─ 5. Evaluación (curvas, matriz confusión, métricas)
    ├─ 6. Validación visual (32 imágenes)
    └─ 7. Exportación → api/model/mnist_cnn.keras
                              │
                        API FastAPI
                              │
                    POST /predict
                    ┌─────────────────┐
                    │ image_base64    │ ← cliente
                    └────────┬────────┘
                             │
                    Decode base64
                    Abrir con PIL
                    Preprocesar (28×28, /255, reshape)
                    model.predict()
                             │
                    ┌─────────────────┐
                    │ prediction: "7" │ → cliente
                    └─────────────────┘
```

