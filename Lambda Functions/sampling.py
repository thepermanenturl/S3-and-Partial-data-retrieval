import boto3
import random

def sampRet(foldername='',ext='CSV',filename='',compression='NONE',skip=4,est=-1):
    
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
        
        
    scanrange={
        "Start":0,
        "End":est
    }
    
    # if rstate!=None:
    #     rstate*=21958
    #     rstate%=100
    #     rs=random.randrange(0,rstate,3)
    # else:
    
    
    s3 = boto3.client('s3')
    datarec=''
    flag=0
    while flag==0:
        #<scanrange><start>50</start><end>100</end></scanrange> 

        try:
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
        
            
            for event in r['Payload']:
                if 'Records' in event:
                    records = event['Records']['Payload'].decode('utf-8')
                    #datarec.append(list(records.split('\r')))
                    print(records)
            
            datarec+=records
            
            scanrange['Start']+=skip*est
            scanrange['End']+=skip*est
            
        except:
            flag=1
            
    return str(datarec)
