import torch
import io
from io import BytesIO
import numpy as np

from torch.nn import functional as F
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from torchvision import transforms

import boto3
import logging
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

resize_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

class_labels = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

#Function to run inference on the image
def infer(model, image):
    if image is None:
        return None

    # Apply the resizing transformation
    image = resize_transform(image)
    image = image.unsqueeze(0)

    preds = model.forward(image)
    preds = F.softmax(preds, dim=1)
    preds = preds[0].tolist()
    # Map the class labels to the predictions
    labeled_preds = {class_labels[i]: preds[i] for i in range(10)}
    return labeled_preds

#Function to pull model from S3 if not exist
def download_model(model_name):

    if os.path.isfile(model_name):
        log.info("Scripted model already exists, skipping s3 pull")
    else:
        log.info("Model not found, attempting to download from AWS S3")
        s3 = boto3.client('s3')
        bucket_name = 'testcm1'
        path = ''
        path = os.path.join(path, model_name)
        file_name = model_name

        s3.download_file(bucket_name, path, file_name)

model_name = 'vit.torchscript.pt'
log.info("Downloading VIT model for inference")
download_model(model_name)

log.info(f"Instantiating scripted model <{model_name}>")
model = torch.jit.load(model_name)
log.info(f"Loaded Model: {model}")
model.eval()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/vit_inference')
async def vit_inference(file: UploadFile = File(...)):
    image_byte = await file.read()
    img = Image.open(io.BytesIO(image_byte))
    output_pred = infer(model, np.array(img))
    return output_pred
