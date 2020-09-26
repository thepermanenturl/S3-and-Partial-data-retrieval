import boto3

def raRe(foldername='',ext='CSV',filename='',compression='NONE',avg=100,srange=0,erange=10):
    
    bucket='asan-api-try1'
    key='fol/RS_Session_249_AS_174_Annexure_II.csv'
    exp='select * from s3object'
    headstate='NONE'
    mod=0
    
    #<scanrange><start>50</start><end>100</end></scanrange> 
    scanrange={
        "Start":srange*avg,
        "End":erange*avg
    }
    
    
    if filename=='':
        key=foldername
    else:
        foldername=foldername.replace('-','/')
        key=foldername+'/'+filename
        
    # if header!='':
    #     headstate='USE'
    #     header='\"'+header.replace('-','\",\"')+'\"'
    #     exp=exp.replace('*',header)
        
        


    s3 = boto3.client('s3')

    r = s3.select_object_content(
            Bucket=bucket,
            Key=key,
            ExpressionType='SQL',
            Expression=exp,
            InputSerialization = 
            {
                'CSV': {"FileHeaderInfo": headstate},
                'CompressionType':compression
            },
            ScanRange=scanrange,
            OutputSerialization = {ext: {}},

    )

    #datarec=''
    for event in r['Payload']:
        #print(event)
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            #datarec.append(list(records.split('\r')))
            print(records)
    return str(records)
