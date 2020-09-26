# S3-and-Partial-data-retrieval


### Given a bucket in AWS S3, create an API that can access and display records from files in bucket
<br>

#### Test API endpoints

S3 Bucket structure-
- fol/
  - RS_Session_249_AS_174_Annexure_II.csv
  - samplefile1.csv
  - samplefile2.txt
  - abc.bz2
  - headered.csv
  - anotherfolder/
    - output-onlinerandomtools.txt
- State-wise_and_Sex-wise_registered_practitioners_in_India.csv
- allopathic10-11.csv


To access folder1/folder2/folder3/file.ext


- GET /folder1-folder2-folder3/file.ext


#### First n rows of file

Use following format-

- GET /{foldername}/{filename}/length
  - This endpoint should return the number of rows of the given filename

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/{length}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/5

<br>

#### Open Compressed files

- GET /{foldername}/{filename}/data?limit={}&format={'CSV'|'JSON'}&compression={'NONE'|'GZIP'|'BZIP2'}&header={}
  - This endpoint returns the results from the file as per the limit and offset values

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/data?limit={}&format={}&compression={'NONE'|'GZIP'|'BZIP2'}&header={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/data?limit=10

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/abc.bz2/data?limit=10&compression=BZIP2

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/headered.csv/data?limit=10&header=column1-column2-column3


#### Records in byte Range

- GET /{foldername}/{filename}/data?brs={}&bre={}
  - This endpoint returns the all records which start in the given byte range. bre=byte range end, brs= byte range start

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/data?bre={}&brs={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/data?brs=0&bre=100


#### Average size of first ravg records
- GET /{foldername}/{filename}/data?ravg={}&look={}
  - Returns the average length of ravg records by scanning progressively increasing ranges. Increase in range scanned=look
  
url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/data?ravg={}&look={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/data?ravg=6&look=100



#### Sampling
- GET /{foldername}/{filename}/data?est={}&skip={}
  - est is estimated size of one record, skip is how many records to skip 
  - eg. if est=100, and skip=5, displays records starting in byte ranges 0-100, 600-700, 1200-1700...
  - if est is skipped, value from ravg=5 is used

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/data?est={}&skip={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/data?est=100&skip=5



#### Nth to Mth Records 
- GET /{foldername}/{filename}/data?srange={}&erange={}
  - srange is lower limit of range, erange is upper limit of range
  - eg. if srange=10, and erange=21, displays records 10 to 21
  - Uses ravg=5, look=200, to find byte range of one record but both values can be changed, i.e. GET /{foldername}/{filename}/data?srange={}&erange={}&ravg={}&look={}

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/{file}/data?srange={}&erange={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/RS_Session_249_AS_174_Annexure_II.csv/data?srange=6&erange=16&ravg=7&look=150

<br>

#### List Subdirectories and files
- GET /{foldername}/listContents?path={}
  - This endpoint lists all files in a given folder path

url-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/{folder}/listContents?path={}

eg-
https://0czirk8cwc.execute-api.ap-south-1.amazonaws.com/Full/fol/listContents?path=

<br>
<br>
DEV-Spandan Bhattacharya
