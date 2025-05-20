# Youtube Analytics - Data Engineering Project

Dataset Used
This Kaggle dataset contains statistics (CSV files) on daily popular YouTube videos over the course of many months. There are up to 200 trending videos published every day for many locations. The data for each region is in its own file. The video title, channel title, publication time, tags, views, likes and dislikes, description, and comment count are among the items included in the data. A category_id field, which differs by area, is also included in the JSON file linked to the region.

https://www.kaggle.com/datasets/datasnaek/youtube-new

## Data Architecture

![image](https://github.com/user-attachments/assets/8f70aa63-1b53-4858-8325-b3ba00b64108)


![image](https://github.com/user-attachments/assets/66050e19-7714-4785-8480-7e119ddfd1e6)

## AWS IAM Setup

### Create IAM User and Group for Project Access

**Access the AWS Console**

![image](https://github.com/user-attachments/assets/49c77d51-c08b-4c0e-be72-6ceefcadafa4)

**Navigate to IAM**

![image](https://github.com/user-attachments/assets/ef3357ab-592a-4f86-ba2a-1e8b6edcfa29)

**Create a New IAM User**

Let's create another account which has less permission since the root account has the most permissions

![image](https://github.com/user-attachments/assets/9048a516-4dd3-4d29-ba73-ef1466ef88b4)

 - Go to **Users** > **Add Users**

![image](https://github.com/user-attachments/assets/124991a9-bc3a-4b10-95d7-e7ca3ef294c0)

 - Provide a name to the iAM account

![image](https://github.com/user-attachments/assets/af509879-f8ef-440a-9cee-10966e9e29a1)

 - Enable **Programmatic access** and **AWS Management Console access**

![image](https://github.com/user-attachments/assets/5fbe0223-4df8-4bec-8308-e6c5acf6074a)

**Attach Administrator Access Policy**

   Go to **Next → Attach existing policies directly** and check the **AdministratorAccess** policy.

![image](https://github.com/user-attachments/assets/6fb48fc8-0932-4451-94b8-ad51f852b199)

**Create the User**

   Click **Next → Create user**. Once created, download the credentials CSV for safekeeping.


![image](https://github.com/user-attachments/assets/f7a2b10a-1b34-456e-9c41-7ea6613a4de9)
![image](https://github.com/user-attachments/assets/4e6f89f9-7373-4061-84b5-2b6132edef09)

**Login Using the New IAM User**

---

## AWS CLI Setup

### Install and Configure AWS CLI

- Open terminal and check installation with:

  ```bash
  aws

![image](https://github.com/user-attachments/assets/de80ffee-9e75-4e24-970f-be11d164f024)

- Then on the terminal type aws configure and then provide your AWS account's access key and the region

- The give the command aws s3 ls , this will show list of s3 buckets  in your account
![image](https://github.com/user-attachments/assets/549efeb9-bde8-4b11-a1c7-fa1b400442d6)

## Data Preparation and S3 Configuration

### Step 1: Download and Organize the Dataset

Download the dataset from Kaggle and organize it locally before uploading to S3.

### Step 2: Create Amazon S3 Buckets

We will use Hive-style directory naming for optimized analytics performance. A typical path structure looks like:
s3://company-raw-awsregion-awsaccountID-env/source/source_region/tablename/year=yyyy/month=mm/day=dd/table_<yearmonthday>.<file_format>

env = dev, test, prod
source = name or indicator of source
source_region = region of data source

Now, go to the AWS Console and create an S3 bucket. Enable server-side encryption during creation.
![image](https://github.com/user-attachments/assets/1bad8f53-ac2b-45d5-b42c-b12a90c882e1)

![image](https://github.com/user-attachments/assets/f35bb574-1978-4791-a136-cf3b68a9d711)

![image](https://github.com/user-attachments/assets/44e2f7af-788b-4804-afb7-03b75f492950)

### Step 3: Upload Data to S3

Navigate to your local directory containing the dataset and execute the following AWS CLI command:
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

## AWS Glue: Crawler Setup

Go to the AWS Glue Console to begin setting up the crawler.

![image](https://github.com/user-attachments/assets/f54ab782-9e3b-494f-acb8-44ca27d386f8)

### Step 1: Add a New Crawler

Click on crawler in your aws console

![image](https://github.com/user-attachments/assets/d1fc4027-40a8-4f0a-8792-724c620f754c)

Click on add crawler
![image](https://github.com/user-attachments/assets/a61b4eae-1d19-46bf-92aa-576b0b8c6108)

![image](https://github.com/user-attachments/assets/0c5bbde1-ae13-4f1e-b819-29d813e7f83e)

Click next -> Proceed by specifying the data path:
![image](https://github.com/user-attachments/assets/f3b75c30-1e30-4784-b401-f1695a46c773)

![image](https://github.com/user-attachments/assets/5e74bd92-9b57-4384-b75e-2327ff16e866)

![image](https://github.com/user-attachments/assets/67f74834-0a46-4564-aecd-e51ee35bc57b)

---

### Step 2: Create an IAM Role for Glue

Glue requires permission to access S3 buckets. Go to IAM in the AWS Console and create a new role.

Click on create role
![image](https://github.com/user-attachments/assets/ce47ba42-16fd-473f-a286-8dd37f17b008)

![image](https://github.com/user-attachments/assets/a4bccf1d-be8e-45d6-bb6c-4bfaa82f76a7)

Select **Glue**:

![image](https://github.com/user-attachments/assets/651233b9-6c9e-48e1-9e38-d41a4c5a55b6)

Then in add permission search for s3 and choose **AmazonS3FullAccess**

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

---

### Step 3: Finish Crawler Setup

Select the IAM role:

![image](https://github.com/user-attachments/assets/5ad3e211-59f5-47da-8374-0f134830acd0)

Click on next , Create a new Glue database:

![image](https://github.com/user-attachments/assets/0c12db49-e6ff-432f-83a8-b854183c4d0e)

![image](https://github.com/user-attachments/assets/407965f9-f760-4986-809c-094b02a8f587)

Run the crawler:

![image](https://github.com/user-attachments/assets/b9891550-02f2-44d9-aa4d-c1bff264c6df)

Once complete, the Glue Data Catalog will reflect schema info such as:
- Column names and types
- Partition keys

![image](https://github.com/user-attachments/assets/652d6f75-b946-4881-aeb5-25a59ddce579)


![image](https://github.com/user-attachments/assets/0961654a-4bcc-442e-b3a3-9d9cdc4915b2)

## Querying Data Using AWS Athena

Once the crawler completes and the table appears in the Glue Data Catalog, we can start querying the data using Athena — AWS's interactive query service.

### Step 1: Access Athena from Glue Table

Click **View Data** on the Glue table. It redirects to Athena:
![image](https://github.com/user-attachments/assets/de9af658-b48c-403a-b98d-9f1080b13779)

![image](https://github.com/user-attachments/assets/9c8fccd3-a106-4e30-8692-a90547babdb1)

---

### Step 2: Create Athena Query Result Bucket

You must create an S3 bucket to store Athena query results:

![image](https://github.com/user-attachments/assets/1c6fe026-58d1-4e86-9213-ef8b27818a78)

Then in Athena settings:

1. Click **View Settings → Manage**
2. Set the newly created S3 bucket as the output location
![image](https://github.com/user-attachments/assets/6f9a7681-4dd4-485b-85f2-636d2b9a8005)

![image](https://github.com/user-attachments/assets/9fd1d1ac-3b5f-45bf-9a89-71f016fc5c04)

---
![image](https://github.com/user-attachments/assets/5263bcd7-da9d-4b80-84b7-74b319496267)

![image](https://github.com/user-attachments/assets/140a6b9f-9efe-44b3-bd8f-7077a2021b90)

![image](https://github.com/user-attachments/assets/111f3e2b-9c6f-44a9-8e32-b552c7fb9ba8)

![image](https://github.com/user-attachments/assets/a685a812-f37c-409f-ba75-4abd17ee07e2)

![image](https://github.com/user-attachments/assets/417cf5f2-643b-4e15-828c-c5705281c690)

![image](https://github.com/user-attachments/assets/05945d90-4894-4bcd-bc92-bc40dbe667f7)

## Data Transformation with AWS Lambda

### Step 1: Create a Lambda Function

Navigate to **AWS Lambda** and create a new function:
![image](https://github.com/user-attachments/assets/af7c5508-4d3c-4737-a6bf-4a8401f03bfb)

![image](https://github.com/user-attachments/assets/d3147a56-e12c-41f0-bee2-4902463e1096)

### Step 2: Create an Execution Role for Lambda

Before proceeding, set up a role with permissions to access S3 and Glue:

![image](https://github.com/user-attachments/assets/495638c2-bebf-4e56-9c3b-4a8da63ae816)

![image](https://github.com/user-attachments/assets/22e7558d-71a6-45bb-8c7c-82ec5f1ae171)

![image](https://github.com/user-attachments/assets/aa85d486-9cac-4d8d-a1c3-4c3a2dca9153)
![image](https://github.com/user-attachments/assets/6a913e3b-4db9-451d-9954-d79394a4dcfd)

### Step 3: Assign Execution Role & Deploy Function

Back in Lambda, under **Execution Role**, choose:

- **Use an existing role**
- Select the role you just created

![image](https://github.com/user-attachments/assets/e8c7ed3c-ad4d-49ee-8547-bf5db33e5786)
![image](https://github.com/user-attachments/assets/33cf86fe-562e-41e6-a32e-f7397145c7be)

Place your `lambda_function.py` code here.
![image](https://github.com/user-attachments/assets/77ef21e2-c7cd-4a8d-a5e1-f77e0bfefe78)

### Step 4: Configure Cleansed Output Bucket

Create an additional S3 bucket to store cleansed data. Then go to:

**Configuration → Environment Variables → Edit**
![image](https://github.com/user-attachments/assets/21430b3d-6091-4ffa-8f1e-abc4055f9b5b)

![image](https://github.com/user-attachments/assets/e2a14886-5ad3-4603-a75d-e85c5fef4de2)

### Step 5: Test the Lambda Function

Click **Test**, and you might encounter errors initially. Below are common issues and resolutions.

![image](https://github.com/user-attachments/assets/a1e87bbf-834c-4ba5-af79-5a79e3b9fb2a)

![image](https://github.com/user-attachments/assets/857c7366-0eb9-4452-813a-176a052fddd7)

![image](https://github.com/user-attachments/assets/96975b98-e195-4d36-84ad-560ffd84b5e3)

## Resolving Lambda Errors and Adding Required Layers

### Step 6: Add Missing Dependencies via Lambda Layer

If the Lambda function fails due to missing packages (like `pandas` or `pyarrow`):


![image](https://github.com/user-attachments/assets/f3b3bcca-3ce1-485a-a78f-51af014d99a6)

![image](https://github.com/user-attachments/assets/7b3598e0-6576-453d-8ae0-648245b93231)

![image](https://github.com/user-attachments/assets/8b8ce699-1681-4db6-9e6e-6bb05051410e)

**Lambda Console → Add Layer**

![image](https://github.com/user-attachments/assets/4bef6385-ebcd-4f9b-a1e3-6be32d68c629)

![image](https://github.com/user-attachments/assets/2520ecc0-a44b-4e85-ab7f-1e494930411c)

![image](https://github.com/user-attachments/assets/8003584e-b2b5-4def-be90-ed8b3ee370b8)

After adding the layer, test the function again. If another error occurs:

![image](https://github.com/user-attachments/assets/f70d4adb-5cf2-440b-b105-998697675a66)

### Step 7: Update Lambda Resource Limits

Navigate to:

**Configuration → General Configuration → Edit**

![image](https://github.com/user-attachments/assets/85ec2f10-f324-4b6c-bed0-343b82d6d0e7)

![image](https://github.com/user-attachments/assets/c8c9dcd4-d6be-4636-b45c-e88a50eb3165)

Now we get one more error , that is because if ou see in the code we're trying to create a glue catalogue and glue table , but in the lamda role we'd created , we didn't give permission to glue 

### Step 8: Add Glue Permissions to Lambda Role

If your Lambda function writes to the Glue Data Catalog, ensure it has permission:
Go to IAM, edit the Lambda role, and add the **AWSGlueServiceRole** policy.


![image](https://github.com/user-attachments/assets/84def752-7d67-4e64-85fc-ab8748d21a13)

### Step 9: Successful Test and Verifying Output

Once the code is corrected and permissions are in place, retest the Lambda function:

![image](https://github.com/user-attachments/assets/718ab818-e2b6-4f27-84bc-64d6b2602b42)

Now if you go to glue and you can see the table being created and now you can query the data by viewing the data in athena


![image](https://github.com/user-attachments/assets/eca34028-fc36-48ef-9d9a-e1d8c059baab)

## Understanding and Validating the Data

### Step 10: Create New Glue Crawler for Cleaned Data

Navigate to Glue Console → Crawlers → Add Crawler
![image](https://github.com/user-attachments/assets/ee5c9266-d85e-424a-ad33-5170dfab1e2d)
![image](https://github.com/user-attachments/assets/4bdffc11-0661-4871-95b2-246ad5228ae9)
![image](https://github.com/user-attachments/assets/57eec062-9ef5-42a9-845d-cd2b9bfc2ae5)
![image](https://github.com/user-attachments/assets/765b3149-7066-4e71-a8f4-065509666dc9)
![image](https://github.com/user-attachments/assets/79646614-12fd-4cca-8068-1eab36832c68)

Click **Finish** to create the crawler:
![image](https://github.com/user-attachments/assets/c0952f2f-159f-4909-8251-4f34cfab7b49)
![image](https://github.com/user-attachments/assets/512f919c-b1cc-40a8-a2bc-03f450b2e970)

### Step 11: Preview Table in Athena

Go to Athena and preview the newly cataloged table:
![image](https://github.com/user-attachments/assets/a41c37c7-2623-4eb7-a1a5-d9b2e0b3b1d7)

### Step 12: Join Raw and Cleaned Tables in Athena

Use a SQL `JOIN` operation to merge raw and cleansed data. Cast data types as needed:
![image](https://github.com/user-attachments/assets/ae318b67-ea38-4178-ac1f-325c062988b4)
Run mthe query 
![image](https://github.com/user-attachments/assets/8496a9b2-93a5-450d-a0b8-3685d6996470)
![image](https://github.com/user-attachments/assets/c161701e-dd91-4122-b42a-c7be224da3ae)

### Step 13: Optimize by Editing Schema in Glue

Instead of casting in every query, update column types:

1. Go to Glue Console → Tables → Cleaned Table

![image](https://github.com/user-attachments/assets/144e101c-ba5d-4bfe-b022-bfdcf58dba23)
2. Click **Edit Schema**
![image](https://github.com/user-attachments/assets/ce005e91-9a2c-498b-8550-043e815f95f8)

Change string columns to `bigint`:
![image](https://github.com/user-attachments/assets/ef0fc6ab-691b-42ee-a958-c892762f01e7)
![image](https://github.com/user-attachments/assets/ba842b97-6f14-485d-99ab-a1cfe3f177ce)

### Step 14: Re-run Query Without Cast (Fails)

Removing `CAST()` may still cause errors due to Parquet metadata mismatches:
![image](https://github.com/user-attachments/assets/43c0b3af-e0f0-4ee8-8428-5e8e3bb6bc19
Basically our parquet file comes with a meta data , so the data type in the meta data has not been changes even tho we changed in aws glue
![image](https://github.com/user-attachments/assets/bac9979c-3821-4ebf-9e61-44ed699afca7)
![image](https://github.com/user-attachments/assets/a542eeaf-872e-47d0-9e21-6e65e32e3865)

### Step 15: Delete Parquet Files and Re-run Lambda

Go to the s3 bucket where you've the cleaned version
![image](https://github.com/user-attachments/assets/001ba078-8a1d-4ad9-b93c-522abfab7c12)
![image](https://github.com/user-attachments/assets/3f61d9e2-9522-440f-becf-7cb8cb4a40e3)

![image](https://github.com/user-attachments/assets/f803eda1-0a27-4aca-8a93-ab8ce1ee7198)

Once it is deleted , go to the lambda function that we had created and test
![image](https://github.com/user-attachments/assets/8b9729bf-024b-4adf-bcb6-b101add7ac71)

![image](https://github.com/user-attachments/assets/f6b95d45-1034-4bca-b895-a88cf11b9097)
![image](https://github.com/user-attachments/assets/af3a7b95-243d-460e-97a7-9591fa49d19b)

Once the code runs successfully

Now run the query
![image](https://github.com/user-attachments/assets/05e4e1a5-324b-492e-a0ed-14f431a1b475)

Now let's process the raw data which is given below
![image](https://github.com/user-attachments/assets/17050204-5a89-43ae-a142-bca9c3aae7f1)

## Processing Raw Data Using AWS Glue Jobs

### Step 16: Create a Glue Job

Go to AWS Glue Console → Jobs → Add Job
![image](https://github.com/user-attachments/assets/b14c78c2-1f0a-456f-83f4-9b9dbef58ab3)
![image](https://github.com/user-attachments/assets/503e0cc2-be17-4023-9533-6d77ca565720)
![image](https://github.com/user-attachments/assets/f4e5a1e9-af6e-4294-9e94-81654164b343)

![image](https://github.com/user-attachments/assets/2cfb12d4-dde4-4f0b-a7db-862d66b52bd9)
![image](https://github.com/user-attachments/assets/25403e05-e92a-4ff8-937a-82cd1e708589)

### Step 17: Set Target Location

Specify the target as the cleansed S3 bucket

![image](https://github.com/user-attachments/assets/c6d5bbe2-182e-4e0a-b802-17123da8b92c)
Update the datatypes wherever it is long into big integer
![image](https://github.com/user-attachments/assets/a8e12de3-8c99-4c1d-a5e5-81a92ef79066)
![image](https://github.com/user-attachments/assets/4b2d5af9-ede8-48ff-8b16-0fcc54e4a4af)
![image](https://github.com/user-attachments/assets/f67820fb-6c9a-43f9-8755-47a391277759)
Click save job and edit script

### Step 18: Review and Optimize PySpark Script

Glue generates a default PySpark script. Open it for manual optimization:
![image](https://github.com/user-attachments/assets/43e5b68d-9cbf-4e4b-b0e1-38d2f21584d4)

  We can easily save and run the above , instead we're going to optimization on this particular job (Refer pyspark code)

  Go to the job that we just created , ere we can track if the job is running or not , We can see an error has occured
  ![image](https://github.com/user-attachments/assets/dab69cb9-7cd9-45c7-b0e0-235c2bb8f3af)

  ### Step 19: Handle Encoding Issues

  If your dataset contains special characters (e.g., Korean, Japanese, etc.), UTF encoding might be required. However, you 
   can also filter by region:
  ![image](https://github.com/user-attachments/assets/42b6b91c-1f50-451c-ac6b-db85d07eaa4f)


  But instead of converting into utf standard , let's just filter out few regions that only we require where machine can 
  understand the language . So for that enter this line of code in our pyspark
  
  ![image](https://github.com/user-attachments/assets/6124cb5b-ac2f-4b34-ab21-e9f563d4d34a)
  ![image](https://github.com/user-attachments/assets/67888b3e-6a44-49fb-8ab5-1056cdf94603)

  Save and run the job again:
  ![image](https://github.com/user-attachments/assets/4137bb16-7fe1-4d24-830c-8c787e098bee)
  And now after successful run we can see the output here
  ![image](https://github.com/user-attachments/assets/dcef2a10-fa82-456f-9fa1-9dcb9902085b)

  Let's create a new crawler
  ![image](https://github.com/user-attachments/assets/9cf4626a-9569-4147-8a90-83eb726111dc)
  ![image](https://github.com/user-attachments/assets/76f8081b-1148-4d3d-8557-eabc74092661)
  ![image](https://github.com/user-attachments/assets/441b1b95-3ab1-4654-aa0a-5da47009e798)
  ![image](https://github.com/user-attachments/assets/272cf1ba-5ee4-41bd-b809-b505da218121)
  Let's run it

## Automating Lambda Execution via S3 Trigger
### Step 20: Add S3 Trigger for Lambda

So now if a new json file is being uploaded in our s3 bucket , it should be automatically run the lambda code and the data should be added to cleansed s3 bucket 

Go to Lambda → Add Trigger → S3
![image](https://github.com/user-attachments/assets/acb81a4a-4001-4a88-bfc3-e83486e3fb8d)
![image](https://github.com/user-attachments/assets/b39f028a-4f53-4395-89f2-f4ac881fa60c)
![image](https://github.com/user-attachments/assets/ec83fa95-3e5b-40a2-af50-606cac092a3e)

### Step 21: Validate Trigger Execution

We can test this by deleting all  our json files in our s3 bucket and adding them again just like we did it before from our cmd, we can see the parquet files being added in our cleaned version of s3 bucket.

## Reporting Layer Setup Using AWS Glue Studio

### Step 22: Open Glue Studio

Now we have got into the step of creating a Reporting layer where we'll perform ETL and preprocessing operations
For this we'll be using glue, go to glue studio in glue console

![image](https://github.com/user-attachments/assets/c6bb4b43-ad64-42d0-8812-aa7cad3b1e53)
Click on view jobs
![image](https://github.com/user-attachments/assets/2d04460b-b6c3-49f2-b8d6-e26f32e2f7b0)
Visual with a source and target->crreate
![image](https://github.com/user-attachments/assets/4b09c70e-bf6b-4558-8496-ba1b035acf6f)
![image](https://github.com/user-attachments/assets/2830c388-ffa8-4516-a441-b2db6f7197e6)
![image](https://github.com/user-attachments/assets/567ced37-4ac9-4e35-b9e3-32dbd928a78f)

### Step 23: Add a Transform - Join

Go to transform and click on  Join 
![image](https://github.com/user-attachments/assets/e753bf9b-f9e8-4f5e-8ce5-cd4ad7d8e461)
![image](https://github.com/user-attachments/assets/9ba35c74-a3a3-4618-8ed6-05a0cc168883)

---

### Step 24: Configure Final Target

- Create a new S3 bucket for storing the final analytics/reporting output.
(We need to store the above data that is obtained using the join operation , for that we've to  create a new s3 bucket for it)
![image](https://github.com/user-attachments/assets/9e8f0f4c-bfdb-4193-8d97-239f32caced1)

Go to your glue studio and add target
![image](https://github.com/user-attachments/assets/6ef71a28-092d-4fbd-9449-8fcd715699dc)
![image](https://github.com/user-attachments/assets/9fc4c3e4-aef4-4e9d-a80d-1765f48de493)

---

### Step 25: Create Athena Database for Reporting

Go to Athena → Databases → Create New Database
![image](https://github.com/user-attachments/assets/e0d27cf8-4ba5-4c91-bc8a-e0dc492feb8f)

![image](https://github.com/user-attachments/assets/ee547337-23d4-44c9-8166-dca21a3cb680)
![image](https://github.com/user-attachments/assets/1b287030-9870-46e6-a3ce-816de82e9405)

---

### Step 26: Final Job Setup

Fill out the job details and click on save 
![image](https://github.com/user-attachments/assets/ef2049c9-e511-4b3c-805b-822bf8689698)

By clicking on run you can execute the job
![image](https://github.com/user-attachments/assets/260054fd-afcb-4a12-ada3-b094a0e8684d)

---

### Step 27: Monitor Job Execution

Monitor via Glue Studio and AWS Console:
You can monitor it in multiple ways
1.
![image](https://github.com/user-attachments/assets/56deb74d-90b5-476d-9741-d5f494d52d3d)
2. Go to glue studio -> View monitoring
![image](https://github.com/user-attachments/assets/ad624a78-b72a-4520-a293-ea61db91ea42)

---

### Step 28: Output Verification

The final output can be viewed in our s3 bucket we created for analytics
(Since region was selected as partition we can see different files being created for different regions and further for different categories)
![image](https://github.com/user-attachments/assets/286ae704-1e76-465f-bd8a-8c88c61a9c7b)

![image](https://github.com/user-attachments/assets/db1da9f9-d6b1-4191-9604-0156624636cd)

## Building Dashboards with Amazon Quicksight

### Step 29: Launch Quicksight Console

Go to the AWS Console → Quicksight
![image](https://github.com/user-attachments/assets/306b38f2-b131-4c02-af3b-eb5c139210bf)

Once you register to quicksight -> go to **Manage Quicksight**:
![image](https://github.com/user-attachments/assets/7776f06f-8ef7-47e0-9660-924818e00df9)
![image](https://github.com/user-attachments/assets/fc4d5c35-6107-4c23-867d-6710c9ccbd18)

---
### Step 30: Connect Athena as a Data Source

We’ll import the processed data from Athena into Quicksight for visual analytics.

![image](https://github.com/user-attachments/assets/5d9fad85-d80a-46d2-97d2-21842c4bad4b)
Create datasource
![image](https://github.com/user-attachments/assets/3f85040c-04e7-47ca-a4a4-3d27e9405cd1)
![image](https://github.com/user-attachments/assets/e26571d9-f506-4a6e-a779-ef9f3a3f3d56)
![image](https://github.com/user-attachments/assets/d4bc4d7c-00ec-4587-ab53-66013ea47f66)
Click on the final analytics dataset
![image](https://github.com/user-attachments/assets/0a10fcde-faa5-4e18-a9ae-98d64ef5b143)

### Step 31: Begin Analysis and Visual Design

1. Click on create analysis
![image](https://github.com/user-attachments/assets/bb99f90c-eb76-47ee-b8c9-b24941df4995)
2. Then create the dashboard for various kpis
   Using the fields from your dataset, design a dashboard that reflects key metrics like:

- Top trending videos
- Regional engagement
- Category-wise viewership
- Likes vs dislikes trends
- Total comments per video/channel
![image](https://github.com/user-attachments/assets/767ccafd-1ac2-4c5d-9eb9-cf897e3d6df1)







































  








































































































