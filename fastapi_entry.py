from typing import Optional

from fastapi import FastAPI

from stock.trend_chart import PttTrendChart, ReunionTrendChart

app = FastAPI()


@app.get("/ptt")
def ptt():
    ptt_trend_chart = PttTrendChart()
    print(ptt_trend_chart.trends)
    return ptt_trend_chart.trends


@app.get("/reunion")
def reunion():
    reunion_trend_chart = ReunionTrendChart()
    print(reunion_trend_chart.trends)
    return reunion_trend_chart.trends

# uvicorn fastapi_entry:app --reload