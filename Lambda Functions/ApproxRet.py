import boto3

def ApRet(foldername='',ext='CSV',filename='',compression='NONE',ravg=5,look=200):
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
         

    s3 = boto3.client('s3')

    s=0
    look=200
    size_in_bytes=0
        
    scanrange={
        "Start":0,
        "End":look
    }

    while s<ravg:
        
        size_in_bytes+=look
        
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
    
        datarec=''
        for event in r['Payload']:
            #print(event)
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8')
                #datarec.append(list(records.split('\r')))
                print(records)
        
        datarec+=str(records)
        
        s= datarec.count('\n')
        #s+=1 #to avoid inf
        #scanrange['Start']+=look
        scanrange['End']+=look

        
        
    size_in_bytes/=s
    return int(size_in_bytes)
    #return str(s) + " records "+" begin in "+" the first "+str(scanrange['End']-look) + " bytes, averaging at "+ str(int(size_in_bytes)) + " bytes per record."
