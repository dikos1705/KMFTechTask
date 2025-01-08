from pydantic import BaseModel


class StatementRequest(BaseModel):
    base64_pdf: str