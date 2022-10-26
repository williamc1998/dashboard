import boto3
import time
import pathlib
import streamlit as st
import os

# keep this private please
with open('/home/ubuntu/keys.txt') as keys:
    lines = keys.readlines()
    key_id = lines[0].replace('\n','')
    key = lines[1]
print(key_id)
print(key)
print(lines)

# key_id = st.secrets['key_id']
# key = st.secrets['key']

# key_id = os.environ['key_id']
# key = os.environ['key']

# WILLIAMS TO DO LIST
#       1-
#       2- rewrite streamlit app + process data accordingly w pandas
#       3- get ec2 up and running and schedule transfer to run automatically + have the app running (at all times?) on vm
#       4- recode THE RESOURCE ACCESS KEY pleasE + encrypt api
#       5- start to get more and better data

def setup_session(key_id, key): # provides the credentials to boto3
    return boto3.Session(aws_access_key_id=key_id,
                         aws_secret_access_key=key)


def setup_resource(resource, bucket): # tells the api where to look
    session = setup_session(key_id, key)
    my_resource = session.resource(resource)
    target_bucket = my_resource.Bucket(bucket)
    return session, my_resource, target_bucket


def show_files(target_bucket): # this will be used in the data processing code to skip over metadata
    files = list(target_bucket.objects.all())


# def delete_files(target_bucket,object_key):  --- WIP

def fetch_query_string(file): # reads the query
    with open(file, 'r') as f:
        lines = str(f.read())
        return lines


def query(query_text, output): # this function takes read query and executes it towards a specified bucket
    client = boto3.client('athena', region_name='eu-west-2', aws_access_key_id=key_id,
                          aws_secret_access_key=key)
    response = client.start_query_execution(
        QueryString=query_text,
        QueryExecutionContext={
            'Database': 'default',
            'Catalog': 'dynamodb'
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )


def data_updater(*args):
    # if exists, delete objects
    try:
        objects_to_delete = boto3.resource('s3',
                                           aws_access_key_id=key_id,
                                           aws_secret_access_key=key).meta.client.list_objects(Bucket="elastikdashboard",
                                                                                               Prefix="test-run-1/hi/")
        delete_keys = {'Objects': []}

        delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]

        boto3.resource('s3',
                       aws_access_key_id=key_id,
                       aws_secret_access_key=key).meta.client.delete_objects(Bucket='elastikdashboard',
                                                                             Delete=delete_keys)
        print('deleted first')
        # transfer each query's data to bucket
        for arg in args:
            print(arg)
            time.sleep(15)
            query(fetch_query_string(arg), 's3://elastikdashboard/test-run-1/hi/')
        print('and added the new data')

    # if doesnt exist, simply skip deletion step
    except:
        print('key didnt exist')
        for arg in args:
            print(arg)
            time.sleep(15)
            query(fetch_query_string(arg), 's3://elastikdashboard/test-run-1/hi/')
        print('now it does')


def main():
    # set up resource
    setup_resource('s3', 'elastikdashboard')
    # provide credentials
    setup_session(key_id, key)
    # run the updater, enter any number of .txts containing the athena queries
    data_updater('query_assigned.txt', 'query_performances.txt', 'query_test_usage.txt','logins.txt')


if __name__ == '__main__':
    main()