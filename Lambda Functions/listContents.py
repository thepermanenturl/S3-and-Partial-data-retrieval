import boto3

def lC(path):
    s3 = boto3.client('s3')
    
    response = s3.list_objects_v2(
    Bucket='asan-api-try1',
    #Delimiter='string',
    #EncodingType='url',
    MaxKeys=123,
    Prefix=path,
    #ContinuationToken='string',
    FetchOwner=True|False
    #StartAfter='string',
    #RequestPayer='requester'
    )
    keys=[]
    if 'Contents' in response:
        n=len(response['Contents'])
        for i in range(n):
            keys.append(response['Contents'][i]['Key'])
    return keys
