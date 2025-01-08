from pydantic import BaseModel,Field


class StatementRequest(BaseModel):
    base64_pdf: str = Field(... , title = "pdf in base 64 format")

class DetailResponse(BaseModel):
    amount: int = Field(... , title = "amount")
    operationDate: int = Field(... , title = "operation date")
    transactionType: str = Field(... , title = "transaction type")
    details: str = Field(... , title = "details")\

class MetricResponse(BaseModel):
    statement_language: str = Field(... , title = "statement language")
    full_name: str = Field(... , title = "full name")
    financialInstitutionName: str = Field(... , title = "bank name")
    cardNumber: str = Field(... , title = "card number")
    number_account: str = Field(... , title = "account number")
    avg_sum: float = Field(... , title = "average topup sum")
    
class StatementResponse(BaseModel):
    financialInstitutionName: str = Field(... , title = "bank name")
    cardNumber: str = Field(... , title = "card number")
    fromDate: str = Field(... , title = "start date")
    toDate: str = Field(... , title = "end date")
    details: list[DetailResponse] = Field(... , title = "transactions details")
    metrics: MetricResponse = Field(... , title = "metrics")
class ParseResponseModel(BaseModel):
    success: bool = Field(... , title = "success or failure")
    msg: str = Field(... , title = "message")
    data: StatementResponse = Field(... , title = "parsed data")
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "msg": None,
                "data": {
                    "financialInstitutionName": "Kaspi",
                    "cardNumber": "1358",
                    "fromDate": "18.09.2023",
                    "toDate": "18.09.2024",
                    "details": [
                    {
                        "amount": -2000,
                        "operationDate": "18.09.2024",
                        "transactionType": "Перевод",
                        "details": "Перевод Инесса М."
                    },
                    {
                        "amount": 9000,
                        "operationDate": "18.09.2024",
                        "transactionType": "Пополнение",
                        "details": "Пополнение С карты другого банка"
                    }]
                    ,
                "metrics": {
                    "avg_sum": 2351037.5,
                    "statement_language": "rus",
                    "full_name": "Бисенбай Алмас Манасұлы",
                    "fin_institut": "Kaspi",
                    "card_number": "1358",
                    "number_account": "KZ48722C000023417033"
                    }
                }
            }
        }
        orm_mode = True
