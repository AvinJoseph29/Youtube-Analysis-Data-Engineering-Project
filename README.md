# Youtube-Data-Engineering-Project

Dataset Used
This Kaggle dataset contains statistics (CSV files) on daily popular YouTube videos over the course of many months. There are up to 200 trending videos published every day for many locations. The data for each region is in its own file. The video title, channel title, publication time, tags, views, likes and dislikes, description, and comment count are among the items included in the data. A category_id field, which differs by area, is also included in the JSON file linked to the region.

https://www.kaggle.com/datasets/datasnaek/youtube-new

Data Architecture

![image](https://github.com/user-attachments/assets/8f70aa63-1b53-4858-8325-b3ba00b64108)


![image](https://github.com/user-attachments/assets/66050e19-7714-4785-8480-7e119ddfd1e6)

Create an IAM user and IAM group for this Project

Aws console -

![image](https://github.com/user-attachments/assets/49c77d51-c08b-4c0e-be72-6ceefcadafa4)

Go to IAM

![image](https://github.com/user-attachments/assets/ef3357ab-592a-4f86-ba2a-1e8b6edcfa29)

Let's create another account which has less permission since the root account has the most permissions

![image](https://github.com/user-attachments/assets/9048a516-4dd3-4d29-ba73-ef1466ef88b4)

Go to users and click on the add users

![image](https://github.com/user-attachments/assets/124991a9-bc3a-4b10-95d7-e7ca3ef294c0)

Provide a name to the iAM account

![image](https://github.com/user-attachments/assets/af509879-f8ef-440a-9cee-10966e9e29a1)

Enable the below configurations

![image](https://github.com/user-attachments/assets/5fbe0223-4df8-4bec-8308-e6c5acf6074a)

Then go to next -> Attach existing policies directly -> check on Administrator acess under Policy name (You can perform all the actions but cannot see some of he thing like costs etc.

![image](https://github.com/user-attachments/assets/6fb48fc8-0932-4451-94b8-ad51f852b199)

Click next-> create user . You can view your credentials , also you can download your credentials file by clicking on download csv

![image](https://github.com/user-attachments/assets/f7a2b10a-1b34-456e-9c41-7ea6613a4de9)
![image](https://github.com/user-attachments/assets/4e6f89f9-7373-4061-84b5-2b6132edef09)

Then login in with new created account 
Install AWS cli

Go to your terminal and type aws to check if aws has been configured in the system

![image](https://github.com/user-attachments/assets/de80ffee-9e75-4e24-970f-be11d164f024)

Then on the terminal type aws configure and then provide your AWS account's access key and the region

The give the command aws s3 ls , this will show list of s3 buckets  in your account
![image](https://github.com/user-attachments/assets/549efeb9-bde8-4b11-a1c7-fa1b400442d6)

Steps to get our data
- Download the dataset
- Create an Amazon s3 bucket, for our landing bucket
eg :
s3://company-raw-awsregion-awsaccountID-env/source/source_region/tablename/year=yyyy/month=mm/day=dd/table_<yearmonthday>.<file_format>

env = dev, test, prod
source = name or indicator of source
source_region = region of data source

Now go to AWS and create the S3 Bucket , enable your server side encryption
![image](https://github.com/user-attachments/assets/1bad8f53-ac2b-45d5-b42c-b12a90c882e1)

![image](https://github.com/user-attachments/assets/f35bb574-1978-4791-a136-cf3b68a9d711)

![image](https://github.com/user-attachments/assets/44e2f7af-788b-4804-afb7-03b75f492950)

Execute the below command, it is to copy data from your local system to the s3 bucket 
Go to the directory where yoiur data is stored and then execute the below command
aws s3 cp . s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"

Similarly execute the following command ie basically creating different folder for deifferent region's data files
# To copy all data files to its own location, following Hive-style patterns:
aws s3 cp CAvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=ca/
aws s3 cp DEvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=de/
aws s3 cp FRvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=fr/
aws s3 cp GBvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=gb/
aws s3 cp INvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=in/
aws s3 cp JPvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=jp/
aws s3 cp KRvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=kr/
aws s3 cp MXvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=mx/
aws s3 cp RUvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=ru/
aws s3 cp USvideos.csv s3://de-on-youtube-raw-useast1-dev/youtube/raw_statistics/region=us/

Go to aws glue on your aws
![image](https://github.com/user-attachments/assets/f54ab782-9e3b-494f-acb8-44ca27d386f8)

Click on crawler in your aws console

![image](https://github.com/user-attachments/assets/d1fc4027-40a8-4f0a-8792-724c620f754c)

Click on add crawler
![image](https://github.com/user-attachments/assets/a61b4eae-1d19-46bf-92aa-576b0b8c6108)

![image](https://github.com/user-attachments/assets/0c5bbde1-ae13-4f1e-b819-29d813e7f83e)

Click next -> Provide the data path
![image](https://github.com/user-attachments/assets/f3b75c30-1e30-4784-b401-f1695a46c773)

![image](https://github.com/user-attachments/assets/5e74bd92-9b57-4384-b75e-2327ff16e866)

![image](https://github.com/user-attachments/assets/67f74834-0a46-4564-aecd-e51ee35bc57b)

Now we've to create the IAM role . let's got to the IAM in our aws

In aws , when a service wants to acess a service for example glue wants to acess the data in s3, we need to create a role for that

Click on create role
![image](https://github.com/user-attachments/assets/ce47ba42-16fd-473f-a286-8dd37f17b008)

![image](https://github.com/user-attachments/assets/a4bccf1d-be8e-45d6-bb6c-4bfaa82f76a7)

Click on glue

![image](https://github.com/user-attachments/assets/651233b9-6c9e-48e1-9e38-d41a4c5a55b6)

Then in add permission search for s3 and choose amazons3fullaccess

![image](https://github.com/user-attachments/assets/b24f0e6b-4458-44df-8b96-e5d6a4d49049)

Provide name to the role and click on create role
![image](https://github.com/user-attachments/assets/1a1d89f2-1716-4060-a828-f06fca3ac9a1)

Find the role created from the below list of roles
![image](https://github.com/user-attachments/assets/e6259619-1767-44cf-b523-aa1d1a4771d2)

Click on the role created and click on add permission
![image](https://github.com/user-attachments/assets/e5d6d5bd-a8cf-43cf-bc3f-ac8ce57e92b2)

Search for glue and choose awsglueservicerole

![image](https://github.com/user-attachments/assets/c2d363c1-7f8d-4650-bb8d-6657aacfeedf)

![image](https://github.com/user-attachments/assets/086d3c7c-3923-4cce-9116-dbfeddf4d10f)

Now go back to the IAM console and click on @choose an existing IAM role@ and find the role that we had created

![image](https://github.com/user-attachments/assets/5ad3e211-59f5-47da-8374-0f134830acd0)

Click on next , then we've to create our new database

![image](https://github.com/user-attachments/assets/0c12db49-e6ff-432f-83a8-b854183c4d0e)

![image](https://github.com/user-attachments/assets/407965f9-f760-4986-809c-094b02a8f587)

Click on run crawler

![image](https://github.com/user-attachments/assets/b9891550-02f2-44d9-aa4d-c1bff264c6df)

You can see the glue creating the catalogue (it will contails information regarding the data  eg - no. of cols /rows , data type etc)

![image](https://github.com/user-attachments/assets/652d6f75-b946-4881-aeb5-25a59ddce579)


![image](https://github.com/user-attachments/assets/0961654a-4bcc-442e-b3a3-9d9cdc4915b2)

Now let's query this data, click on view data it will redirect you to aws athena which aws's query tool to understand what's happending int the data
![image](https://github.com/user-attachments/assets/de9af658-b48c-403a-b98d-9f1080b13779)

![image](https://github.com/user-attachments/assets/9c8fccd3-a106-4e30-8692-a90547babdb1)

Note - create a new s3 bucket for athena job


![image](https://github.com/user-attachments/assets/1c6fe026-58d1-4e86-9213-ef8b27818a78)


Click on view settings -> manage -> provide the s3 bucket created for athena

![image](https://github.com/user-attachments/assets/6f9a7681-4dd4-485b-85f2-636d2b9a8005)

![image](https://github.com/user-attachments/assets/9fd1d1ac-3b5f-45bf-9a89-71f016fc5c04)


![image](https://github.com/user-attachments/assets/5263bcd7-da9d-4b80-84b7-74b319496267)



![image](https://github.com/user-attachments/assets/140a6b9f-9efe-44b3-bd8f-7077a2021b90)

![image](https://github.com/user-attachments/assets/111f3e2b-9c6f-44a9-8e32-b552c7fb9ba8)

![image](https://github.com/user-attachments/assets/a685a812-f37c-409f-ba75-4abd17ee07e2)

![image](https://github.com/user-attachments/assets/417cf5f2-643b-4e15-828c-c5705281c690)

![image](https://github.com/user-attachments/assets/05945d90-4894-4bcd-bc92-bc40dbe667f7)

Go to AWS Lambda to perform the transformation using python code










































