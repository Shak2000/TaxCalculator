from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Payer

payer = Payer()
app = FastAPI()


# Request models for POST endpoints
class JobRequest(BaseModel):
    desc: str
    salary: int
    amount: float
    periods: int
    hours: int

class RemoveRequest(BaseModel):
    index: int

class StatusRequest(BaseModel):
    status: str

class DeductionRequest(BaseModel):
    desc: str
    amount: float

class CreditRequest(BaseModel):
    desc: str
    amount: float


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
async def get_add_job(request: JobRequest):
    # Convert periods back to period string for the main.py method
    period_map = {1: 'A', 12: 'M', 24: 'S', 26: 'B', 52: 'W'}
    period = period_map.get(request.periods, 'A')  # Default to 'A' if not found
    
    result = payer.add_job(request.desc, bool(request.salary), request.amount, period, request.hours)
    return {"success": result}


@app.post("/remove_job")
async def get_remove_job(request: RemoveRequest):
    result = payer.remove_job(request.index)
    return {"success": result}


@app.post("/set_status")
async def get_set_status(request: StatusRequest):
    result = payer.set_status(request.status)
    return {"success": result}


@app.post("/add_deduct")
async def get_add_deduct(request: DeductionRequest):
    payer.add_deduct(request.desc, request.amount)
    return {"success": True}


@app.post("/remove_deduct")
async def get_remove_deduct(request: RemoveRequest):
    result = payer.remove_deduct(request.index)
    return {"success": result}


@app.post("/add_rcredit")
async def get_add_rcredit(request: CreditRequest):
    payer.add_rcredit(request.desc, request.amount)
    return {"success": True}


@app.post("/remove_rcredit")
async def get_remove_rcredit(request: RemoveRequest):
    result = payer.remove_rcredit(request.index)
    return {"success": result}


@app.post("/add_nrcredit")
async def get_add_nrcredit(request: CreditRequest):
    payer.add_nrcredit(request.desc, request.amount)
    return {"success": True}


@app.post("/remove_nrcredit")
async def get_remove_nrcredit(request: RemoveRequest):
    result = payer.remove_nrcredit(request.index)
    return {"success": result}


@app.get("/calculate_fica")
async def get_calculate_fica(gross_income: float = Query(...)):
    return payer.calculate_fica(gross_income)


@app.get("/calculate_tax")
async def get_calculate_tax(gross_income: float = Query(...)):
    return payer.calculate_tax(gross_income)


@app.get("/calculate")
async def get_calculate():
    result = payer.calculate()
    return result


@app.get("/get_filing_status")
async def get_filing_status():
    return {"status": payer.status}


@app.get("/get_jobs")
async def get_jobs():
    return {"jobs": payer.jobs}


@app.get("/get_deductions")
async def get_deductions():
    return {"deductions": payer.deduct}


@app.get("/get_refundable_credits")
async def get_refundable_credits():
    return {"refundable_credits": payer.rcredit}


@app.get("/get_non_refundable_credits")
async def get_non_refundable_credits():
    return {"non_refundable_credits": payer.nrcredit}


@app.get("/get_standard_deduction_added")
async def get_standard_deduction_added():
    return {"standard_deduction_added": payer.standard_deduction_added}


@app.get("/get_standard_deduction_amount")
async def get_standard_deduction_amount():
    if payer.status == 'J':
        amount = 30000
    elif payer.status == 'H':
        amount = 22500
    elif payer.status == 'S':
        amount = 15000
    else:  # Single
        amount = 15000
    return {"amount": amount}


@app.get("/get_period_multiplier")
async def get_period_multiplier(period: str = Query(...)):
    multiplier = payer.period_to_number(period)
    return {"multiplier": multiplier}


@app.get("/get_status_names")
async def get_status_names():
    return {
        "status_names": {
            'U': 'Single',
            'J': 'Married Filing Jointly',
            'S': 'Married Filing Separately',
            'H': 'Head of Household'
        }
    }
