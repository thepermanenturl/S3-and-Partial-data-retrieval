import boto3

def ret(foldername='',limit=0,ext='CSV',filename='',compression='NONE',header=''):
    
    #default
    bucket='asan-api-try1'
    key='fol/RS_Session_249_AS_174_Annexure_II.csv'
    #ext='CSV'
    exp='select * from s3object'
    headstate='NONE'
    
    if filename=='':
        key=foldername
    else:
        foldername=foldername.replace('-','/')
        key=foldername+'/'+filename
        
    if header!='':
        headstate='USE'
        header='\"'+header.replace('-','\",\"')+'\"'
        exp=exp.replace('*',header)
        
        
    if limit!=0:
        exp+=' limit '+str(limit)
    

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
