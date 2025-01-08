import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def convert_date(date_str: str) -> str:
    date_str = date_str.split('.')
    print(date_str)
    if int(date_str[2]) >=0 and len(date_str[2]) == 2:
        return f"{date_str[0]}.{date_str[1]}.20{date_str[2]}"
    
    return f"{date_str[0]}.{date_str[1]}.19{date_str[2]}"
    
async def create_excel_file(parsed_data : dict , add_info : list[str]) -> None :

    changed_data = []

    for e in parsed_data['details']:
        {
            "AMOUNT" : e['amount'],
            "DETAILS" : e['details'],
            "OPERATION_DATE" : e['operationDate'],
            "TRANSACTION_TYPE" : e['transactionType'],   
        }
        changed_data.append(e)

    details_df = pd.DataFrame(changed_data)
    details_df['FROM_DATE'] = parsed_data['fromDate']
    details_df['TO_DATE'] = parsed_data['toDate']
    details_df['STATEMENT_LANGUAGE'] = parsed_data['metrics']['statement_language']
    details_df['FULL_NAME'] = parsed_data['metrics']['full_name']
    details_df['FINANSIAL_INSTITUTION'] = parsed_data['financialInstitutionName']

    details_df['INSERT_DATE'] = datetime.now()
    details_df['CARD_NUMBER'] = parsed_data['cardNumber']
    details_df['ST_CREATION_DATE'] = parsed_data['toDate']
    details_df['ST_MODIFIED_DATE'] = parsed_data['toDate']
    details_df['ST_SUBJECT'] = f"{add_info[0]} {add_info[1]} клиента {parsed_data['metrics']['full_name']}"
    details_df['ST_AUTHOR'] = "Kasymzhan Dias"
    details_df['ST_TITLE'] = f"{add_info[0]} {add_info[1]}"
    details_df['ST_PRODUCER'] = "АО «Kaspi Bank», БИК CASPKZKA, www.kaspi.kz"
    
    output_path = "statement.xlsx"
    details_df.to_excel(output_path, index=False)

async def calculate_average_topup(transactions: list[dict[str, str | int]]) -> float:
    latest_transaction_date = max(
        datetime.strptime(tx["operationDate"], "%d.%m.%Y") for tx in transactions
    )
    
    start_date = (latest_transaction_date - relativedelta(months=6)).replace(day=1)
    end_date = latest_transaction_date.replace(day=1) + relativedelta(months=1, days=-1)
    
    topups = [
        tx for tx in transactions
        if tx["transactionType"] == "Пополнение" and
        start_date <= datetime.strptime(tx["operationDate"], "%d.%m.%Y") <= end_date
    ]
    
    total_topup = sum(tx["amount"] for tx in topups)
    
    return round(total_topup / 6, 2) if total_topup > 0 else 0.0

async def parse_transactions(transactions: list[str]) -> list[dict[str, str | int]]:
    parsed_details = []
    for transaction in transactions:
        match = re.match(r"(\d{2}\.\d{2}\.\d{2}) ([+-]) ([\d\s,]+) ₸ (.+)", transaction)
        if match:
            operation_date, sign, amount, details = match.groups()
            
            amount = float(amount.replace(" ", "").replace(",", "."))
            
            amount *= 1 if sign == "+" else -1
            
            transaction_type = "Пополнение" if sign == "+" else "Перевод"
            if "Покупка" in details:
                transaction_type = "Покупка"
            
            parsed_details.append({
                "amount": amount,
                "operationDate": convert_date(operation_date),
                "transactionType": transaction_type,
                "details": details.strip()
            })
    
    return parsed_details

async def parsing_data(txt_list : list) -> dict:
    
    cardNumber = txt_list[3][14:]

    fromDate = convert_date(txt_list[1][26:34])
    toDate = convert_date(txt_list[1][38:])

    full_name = txt_list[2]+ ' ' + txt_list[4]
    number_account = txt_list[5][13:]

    details = await parse_transactions(txt_list[16:-1])
    avg_sum = await calculate_average_topup(details)

    parsed_data = {
            "financialInstitutionName": "Kaspi",
            "cardNumber": cardNumber,
            "fromDate": fromDate,
            "toDate": toDate,
            "details": details,
            "metrics": {
                "avg_sum": avg_sum,
                "statement_language": "rus",
                "full_name": full_name,
                "fin_institut": "Kaspi",
                "card_number": cardNumber,
                "number_account": number_account
            }
        }


    return parsed_data