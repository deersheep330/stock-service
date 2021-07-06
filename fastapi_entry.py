from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stock.trend_chart import PttTrendChart, ReunionTrendChart

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ptt")
def ptt():
    ptt_trend_chart = PttTrendChart()
    print(ptt_trend_chart.trends)
    return ptt_trend_chart.trends[:8]


@app.get("/reunion")
def reunion():
    reunion_trend_chart = ReunionTrendChart()
    print(reunion_trend_chart.trends)
    return reunion_trend_chart.trends[:8]


@app.get("/ins-buy")
def ins_buy():
    return []


@app.get("/ins-sell")
def ins_sell():
    return []


@app.get("/health_check")
def health_check():
    return {"iam": "healthy"}

# uvicorn fastapi_entry:app --reload