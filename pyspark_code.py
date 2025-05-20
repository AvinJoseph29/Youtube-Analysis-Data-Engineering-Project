import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame  # Required for conversion between DataFrame and DynamicFrame

# Parse the job name argument passed by AWS Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------------------------
# STEP 1: Read raw data from AWS Glue Data Catalog
# -----------------------------------------------

# Push-down predicate to load only specific regions for optimization
predicate_pushdown = "region in ('ca','gb','us')"

# Load the 'raw_statistics' table from the 'db_youtube_raw' Glue database
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database="db_youtube_raw",
    table_name="raw_statistics",
    transformation_ctx="datasource0",
    push_down_predicate=predicate_pushdown
)

# -----------------------------------------------
# STEP 2: Apply mapping to enforce schema structure
# -----------------------------------------------

# This ensures the correct data types and column names are maintained
applymapping1 = ApplyMapping.apply(
    frame=datasource0,
    mappings=[
        ("video_id", "string", "video_id", "string"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "long", "category_id", "long"),
        ("publish_time", "string", "publish_time", "string"),
        ("tags", "string", "tags", "string"),
        ("views", "long", "views", "long"),
        ("likes", "long", "likes", "long"),
        ("dislikes", "long", "dislikes", "long"),
        ("comment_count", "long", "comment_count", "long"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "boolean", "comments_disabled", "boolean"),
        ("ratings_disabled", "boolean", "ratings_disabled", "boolean"),
        ("video_error_or_removed", "boolean", "video_error_or_removed", "boolean"),
        ("description", "string", "description", "string"),
        ("region", "string", "region", "string")
    ],
    transformation_ctx="applymapping1"
)

# -----------------------------------------------
# STEP 3: Resolve data type conflicts (if any)
# -----------------------------------------------

# Converts multiple data type choices into struct if conflicting
resolvechoice2 = ResolveChoice.apply(
    frame=applymapping1,
    choice="make_struct",
    transformation_ctx="resolvechoice2"
)

# -----------------------------------------------
# STEP 4: Remove any null fields
# -----------------------------------------------

dropnullfields3 = DropNullFields.apply(
    frame=resolvechoice2,
    transformation_ctx="dropnullfields3"
)

# -----------------------------------------------
# STEP 5: Optimize and Write the output to S3 in Parquet format
# -----------------------------------------------

# Convert DynamicFrame to Spark DataFrame to perform coalesce (single output file)
datasink1 = dropnullfields3.toDF().coalesce(1)

# Convert DataFrame back to DynamicFrame for Glue compatibility
df_final_output = DynamicFrame.fromDF(datasink1, glueContext, "df_final_output")

# Write the cleaned and partitioned data to the target S3 bucket in Parquet format
datasink4 = glueContext.write_dynamic_frame.from_options(
    frame=df_final_output,
    connection_type="s3",
    connection_options={
        "path": "s3://de-on-youtube-cleansed-useast1-dev/youtube/raw_statistics/",
        "partitionKeys": ["region"]
    },
    format="parquet",
    transformation_ctx="datasink4"
)

# Commit the Glue job
job.commit()
