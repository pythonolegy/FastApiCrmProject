import schedule
from main import *

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import logging

from fastapi.middleware.cors import CORSMiddleware

from server_alert import send_alert_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(levelname)s: %(message)s')


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(levelname)s: %(message)s')

