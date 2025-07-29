from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from main import Payer

payer = Payer()
app = FastAPI()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.get("/period_to_number")
async def get_period_to_number(period: str = Query(...)):
    return payer.period_to_number(period)


@app.post("/add_job")
async def get_add_job(
    desc: str = Query(...),
    salary: float = Query(...),
    amount: float = Query(...),
    periods: int = Query(...),
    hours: int = Query(...)
):
    return payer.add_job(desc, salary, amount, periods, hours)


@app.post("/remove_job")
async def get_remove_job(index: int = Query(...),):
    return payer.remove_job(index)


@app.post("/set_status")
async def get_set_status(status: str = Query(...),):
    return payer.set_status(status)


@app.post("/add_deduct")
async def get_add_deduct(desc: str = Query(...), amount: float = Query(...)):
    return payer.add_deduct(desc, amount)


@app.post("/remove_deduct")
async def get_remove_deduct(index: int = Query(...),):
    return payer.remove_deduct(index)


@app.post("/add_rcredit")
async def get_add_rcredit(desc: str = Query(...), amount: float = Query(...)):
    return payer.add_rcredit(desc, amount)

@app.post("/remove_rcredit")
async def get_remove_rcredit(index: int = Query(...),):
    return payer.remove_rcredit(index)


@app.post("/add_nrcredit")
async def get_add_nrcredit(desc: str = Query(...), amount: float = Query(...)):
    return payer.add_nrcredit(desc, amount)


@app.post("/remove_nrcredit")
async def get_remove_nrcredit(index: int = Query(...),):
    return payer.remove_nrcredit(index)


@app.get("/calculate_fica")
async def get_calculate_fica(gross_income: float = Query(...)):
    return payer.calculate_fica(gross_income)


@app.get("/calculate_tax")
async def get_calculate_tax(gross_income: float = Query(...)):
    return payer.calculate_tax(gross_income)


@app.get("/calculate")
async def get_calculate():
    return payer.calculate()
