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


@app.post('/some-endpoint-example/deal-update')
async def post_deal_update(data: Order):
    """ The function starts main() with passing the data argument from .json """
    try:
        logging.info(f"REQUEST: {data}")
        result = await main(data)
        return JSONResponse(result, status_code=status.HTTP_202_ACCEPTED)
    except Exception as err:
        send_alert_message(f"RuntimeError: {err}")
        logging.error(err)
        return JSONResponse({'result': False}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    uvicorn.run('server:app', port=5000, host='localhost')
