import pickle

import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from stock.institutions_chart import InstitutionsOverBoughtChart, InstitutionsOverSoldChart
from stock.trend_chart import PttTrendChart, ReunionTrendChart
from stock.utilities import get_redis_host

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ptt")
def ptt():
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)
    if r.exists('ptt'):
        return pickle.loads(r.get('ptt'))
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/reunion")
def reunion():
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)
    if r.exists('reunion'):
        return pickle.loads(r.get('reunion'))
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/ins-buy")
def ins_buy():
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)
    if r.exists('ins_buy'):
        return pickle.loads(r.get('ins_buy'))
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/ins-sell")
def ins_sell():
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)
    if r.exists('ins_sell'):
        return pickle.loads(r.get('ins_sell'))
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/health_check")
def health_check():
    return {"iam": "healthy"}

# uvicorn fastapi_entry:app --reload