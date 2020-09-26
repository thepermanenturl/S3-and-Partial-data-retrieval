import json
import RetFile
import listContents
import scanRange
import sampling
import ApproxRet
import rangeReturn

def lambda_handler(event, context):
    # TODO implement
    #default
    ans='Invalid Query'
    compression='NONE'
    ext='CSV' #default
    limit=0   #all records
    header=''
    bre=-1
    brs=-1
    sr=0
    est=64
    skip=4
    ravg=5
    look=200
    
    try:
        if 'file' in event['pathParameters']:  #GET /{foldername}/{filename}
            
            foldername=event['pathParameters']['folder']
            filename=event['pathParameters']['file']
            
            if event['queryStringParameters']!=None:    #GET /{foldername}/{filename}/data?limit={}&format={}
            
                if 'limit' in event['queryStringParameters']:
                    limit=int(event['queryStringParameters']['limit'])
                    
                if 'format' in event['queryStringParameters']:
                    ext=event['queryStringParameters']['format'].upper()
                    
                if 'compression' in event['queryStringParameters']:
                    compression=event['queryStringParameters']['compression'].upper()
                    
                if 'header' in event['queryStringParameters']:
                    header=event['queryStringParameters']['header']
                
                #ans+="rpoint1"
                
                if 'ravg' in event['queryStringParameters'] or 'look' in event['queryStringParameters']:
                    #ans+="rpoint2"

                    if 'ravg' in event['queryStringParameters']:
                        ravg=int(event['queryStringParameters']['ravg'])
                    if 'look' in event['queryStringParameters']:
                        look=int(event['queryStringParameters']['look'])
                    if sr==0:
                        t=ApproxRet.ApRet(foldername,ext,filename,compression,ravg,look)
                        ans= "Average size of one record is "+str(t) +" bytes"
                    sr=1
                    
                if 'brs' in event['queryStringParameters']:
                    brs=int(event['queryStringParameters']['brs'])
                    bre=int(event['queryStringParameters']['bre'])
                    if sr==0:
                        ans=scanRange.ret2(foldername,ext,filename,compression,header,brs,bre)
                    sr=1
                    
                if 'est' in event['queryStringParameters'] or 'skip' in event['queryStringParameters']:
                    if 'est' not in event['queryStringParameters']:
                        est=ApproxRet.ApRet(foldername,ext,filename,compression,ravg,look)
                    else:
                        est=int(event['queryStringParameters']['est'])
                    if 'skip' not in event['queryStringParameters']:
                        skip=4
                    else:
                        skip=int(event['queryStringParameters']['skip'])
                    ans=sampling.sampRet(foldername,ext,filename,compression,skip,est)
                    sr=1
                    
                if 'srange' in event['queryStringParameters'] and 'erange' in event['queryStringParameters']:
                    srange=int(event['queryStringParameters']['srange'])
                    erange=int(event['queryStringParameters']['erange'])
                    avg=ApproxRet.ApRet(foldername,ext,filename,compression,ravg,look)
                    ans=rangeReturn.raRe(foldername,ext,filename,compression,avg,srange,erange)
                    sr=1
                
                
                
            if 'length' in event['pathParameters']:    #GET /{foldername}/{filename}/length
                limit=event['pathParameters']['length']
        
            if sr==0:
                ans=RetFile.ret(foldername,limit,ext,filename,compression,header)
            
        elif 'path' in event['queryStringParameters']:    #GET /{foldername}/listContents?path={}
            ans=listContents.lC(event['pathParameters']['folder']+'/'+event['queryStringParameters']['path'])
                
    except TypeError:  #When no folder or file specified. To make work in lambda, change to KeyError - GET /
        ans+="API works, add file and folder name in address."
            
            
    return {
        "isBase64Encoded": True|False,
        "statusCode": 200,
        #"headers": { "headerName": "headerValue"},
        "body": str(ans) 
        #"body": str(RetFile.ret(ans))
    }
