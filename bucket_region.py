import boto3

# Replace with your bucket name and the desired region location
bucket_name = 'my-bucket'
new_region = 'us-west-2'

# Create an S3 client
s3 = boto3.client('s3')

# Get the current location of the bucket
response = s3.get_bucket_location(Bucket=bucket_name)

# If the bucket is already in the desired region, exit the script
current_region = response['LocationConstraint']
if current_region == new_region:
    print(f"{bucket_name} is already in {new_region}")
    exit()

# If the bucket is in the 'us-east-1' region, set the location constraint to None
# This is because 'us-east-1' is the default region, and must be handled differently
if current_region == 'us-east-1':
    current_region = None

# Update the bucket location
s3.put_bucket_location(Bucket=bucket_name, LocationConstraint=new_region)

# Confirm the new bucket location
response = s3.get_bucket_location(Bucket=bucket_name)
new_location = response['LocationConstraint']
print(f"{bucket_name} has been moved to {new_location}")
