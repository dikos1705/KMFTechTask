from fastapi import FastAPI, HTTPException

import base64
import pdfplumber
import datetime
import io
from scheme import *
from utils import *
app = FastAPI()



@app.post("/parse_data/")
async def parse_data(data: StatementRequest):
    try:
        pdf_data = base64.b64decode(data.base64_pdf)
        pdf_stream = io.BytesIO(pdf_data)

        with pdfplumber.open(pdf_stream) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
            text = text.replace("АО «Kaspi Bank», БИК CASPKZKA, www.kaspi.kz",'').split('\n')
        
        parsed_data = await parsing_data(text)

        await create_excel_file(parsed_data,text[:16])

        return {
            "success": True,
            "msg": None,
            "data": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
