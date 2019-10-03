import boto3
import json

TABLE_NAME = 'CoatStatus'
COLUMN_NAME = 'day'

# DynamoDBから日付のリストを取得する
def readDayList():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    res = table.scan()
    return list(map(lambda x: x[COLUMN_NAME], res['Items']))

# DynamoDBに日付を登録
def insertDayList(list):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    
    with table.batch_writer() as batch:
        for ele in update_list:
            batch.put_item(
                Item={
                    COLUMN_NAME: ele
                })