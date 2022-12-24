import requests
import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    notion_api_url = os.environ.get("NOTION_BASE_URL") or "https://api.notion.com"
    notion_api_version = os.environ.get("NOTION_VERSION") or "v1"
    notion_api_version_date = os.environ.get("NOTION_VERSION_DATE") or "2022-06-28"
    notion_api_database_id = os.environ.get("NOTION_DATABASE_ID") or "0590158c-cca7-43fe-b87f-e62a671abca0"
    notion_api_secret_key = os.environ.get("NOTION_SECRET_KEY") or "secret_m3nIm4aOkqrEBnCp1iA5EBegp6cBbUHK3ZkGCj2dEHa"
    
    service_name = os.environ.get("AWS_SERVICE_NAME") or "dynamodb"
    region_name = os.environ.get("AWS_REGION_NAME") or "us-east-1"
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID") or "AKIA54UO4IUZXVG2BONU"
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY") or "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"
    table_name = os.environ.get("AWS_DYNAMO_TABLE_NAME") or "notion_activities_devfazer"

    print(service_name)
    print(region_name)
    print(aws_access_key_id)
    print(aws_secret_access_key)

    dynamo_client = boto3.resource(
        service_name=f"{service_name}",
        region_name=f"{region_name}",
        aws_access_key_id=f"{aws_access_key_id}",
        aws_secret_access_key=f"{aws_secret_access_key}"
    )

    table = dynamo_client.Table(f'{table_name}')

    payload = {}
    
    headers = {
        "Notion-Version": notion_api_version_date,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {notion_api_secret_key}"
    }

    URL = f"{notion_api_url}/{notion_api_version}/databases/{notion_api_database_id}/query"
    log_info = f"""
        REQUISITANDO NOTION
        URL: {URL}
        METHOD: POST
        PAYLOAD: {payload}
        HEADERS: {headers}
    
    """
    print(log_info)

    # Buscar Atividades no Notion
    r = requests.post(f"{URL}", data=json.dumps(payload), headers=headers)
    registros = []
    if r.status_code == 200:
        registros = r.json().get("results") or []
        # Gravar ou Atualizar Registros
        for registro in registros:
            try:
                print("GRAVANDO REGISTRO: " + registro.get("id"))
                table.put_item(
                    Item=registro,
                )
            except ClientError as err:
                print(
                    f"Couldn't add record {registro.get('id')} to table {table_name}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
                raise
        
        print(f"{len(registros)} Itens Inseridos com Sucesso!!")
        return {
            'statusCode': 200,
            'body': json.dumps(registros, default=str),
            'headers': {
                "Content-Type": "application/json"
            }
        }

        

    log_error = f"""
            FALHA NA COMUNICAÇÃO COM API DO NOTION
            URL: {r.url}
            METHOD: {r.request.method}
            STATUS REQUEST: {r.status_code}
            RETORNO: {r.text}
    """
    print(log_error)
    return {
        'statusCode': 400,
        'body': json.dumps(registros, default=str),
        'headers': {
            "Content-Type": "application/json"
        }
    }

