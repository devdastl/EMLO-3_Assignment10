from typing import Tuple
import sys
import os
import torch
import torch.nn.functional as F
import logging
import tiktoken
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

#Base class to define input
class GPTInput(BaseModel):
    text: str

# Define a transformation to resize images to 32x32
def generate_text(model, text: str):
    input_enc = torch.tensor(tokenizer.encode(text))
    with torch.no_grad():
        out_gen = model.model.generate(input_enc.unsqueeze(0).long(), max_new_tokens=32)
    decoded = tokenizer.decode(out_gen[0].cpu().numpy().tolist())
    return decoded

# Function to pull model from S3
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

# tokenizer
cl100k_base = tiktoken.get_encoding("cl100k_base")

tokenizer = tiktoken.Encoding(
    name="cl100k_im",
    pat_str=cl100k_base._pat_str,
    mergeable_ranks=cl100k_base._mergeable_ranks,
    special_tokens={
        **cl100k_base._special_tokens,
        "<|im_start|>": 100264,
        "<|im_end|>": 100265,
    }
)

demo_ckpt_path = 'gpt.torchscript.pt'
log.info("Downloading GPT model for inference")
download_model(demo_ckpt_path)

log.info(f"Instantiating scripted model <{demo_ckpt_path}>")
model = torch.jit.load(demo_ckpt_path)
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

@app.post('/gpt_inference')
async def gpt_inference(input_text: GPTInput) -> str:
    output_text = generate_text(model, input_text.text)
    return {"completed_text": output_text}

