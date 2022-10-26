import pandas as pd
import datetime
from s3fs.core import S3FileSystem
import boto3
import streamlit as st
import os

# get set up
def setup_session(key_id, key):
    return boto3.Session(aws_access_key_id=key_id,
                         aws_secret_access_key=key)


def setup_resource(resource, bucket):
    session = setup_session(key_id, key)
    my_resource = session.resource(resource)
    global target_bucket
    target_bucket = my_resource.Bucket(bucket)
    return session,my_resource,target_bucket

# with open('/Users/william/Desktop/Elastik/awskeys/keys.txt') as keys:
#     lines = keys.readlines()
#     key_id = lines[0].replace('\n','')
#     key = lines[1]
# print(key_id)
# print(key)
# print(lines)

# key_id = st.secrets['key_id']
# key = st.secrets['key']

key_id = os.environ['key_id']
key = os.environ['key']

bucket_dict = {'assigned':'','performance':'','usage':'','logins':''}
setup_session(key_id, key)
setup_resource('s3','elastikdashboard')
files = target_bucket.objects.filter(Prefix='test-run-1/')
files = [obj.key for obj in sorted(files,key=lambda x: x.last_modified, reverse=False)]

for i,i2 in enumerate([k for j,k in enumerate(files) if j % 2 != 0]):
    bucket_dict[list(bucket_dict.keys())[i]] = i2
s3 = S3FileSystem(anon=False,key=key_id,secret=key)


# pandas functions
def avg_logins_transform(file):
    df_logins = pd.read_csv(s3.open('s3://elastikdashboard/'+(bucket_dict.get(file))),parse_dates=True,index_col=0)
    print('index check',df_logins)
    df_logins['weeklyavg'] = df_logins['users'].rolling(window=5).mean()
    df_logins = df_logins.drop(df_logins.head(4).index)
    df_logins = df_logins.drop(df_logins.tail(5).index)
    return df_logins


def time_logins(file):
    df_logins = pd.read_csv(s3.open('s3://elastikdashboard/' + (bucket_dict.get(file))))
    print(df_logins)
    today = datetime.date.today()
    last_month = (today - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    df_average_month1 = int(round(df_logins[df_logins['_col0'] > last_month].mean()))
    df_average_year = round(df_logins['users'].mean())
    return df_average_year

def time_logins_month(file):
    df_logins = pd.read_csv(s3.open('s3://elastikdashboard/' + (bucket_dict.get(file))))
    print(df_logins)
    today = datetime.date.today()
    last_month = (today - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    df_average_month1 = int(round(df_logins[df_logins['_col0'] > last_month].mean()))
    df_average_year = round(df_logins['users'].mean())
    return df_average_month1

def time_logins_df(file):
    df_logins = pd.read_csv(s3.open('s3://elastikdashboard/' + (bucket_dict.get(file))))
    return df_logins


def get_comparisons(file):
    df_comparisons = pd.read_csv(s3.open('s3://elastikdashboard/' + (bucket_dict.get(file))))
    print('test',df_comparisons)
    df_comparisons = df_comparisons.groupby('schoolName').mean(numeric_only=True)
    df_comparisons = df_comparisons.drop(df_comparisons.index[2:6])
    df_comparisons = df_comparisons.drop(df_comparisons.index[2])
    df_comparisons['schoolName'] = df_comparisons.index
    df_comparisons = df_comparisons.sort_values(by=['score'],ascending=False)
    return df_comparisons


def get_tests_assigned(file):
    df_test_usage = pd.read_csv(s3.open('s3://elastikdashboard/' + (bucket_dict.get(file))))
    index_names = df_test_usage[(df_test_usage['schoolName'] == 'Example Secondary School') | (df_test_usage['schoolName'] == 'Example Partner School 1') | (df_test_usage['schoolName'] == 'Example Partner School 2') | (df_test_usage['schoolName'] == 'Example Partner School 3')| (df_test_usage['schoolName'] == 'Example Partner School 4') | (df_test_usage['schoolName'] == 'Best Performance School') | (df_test_usage['schoolName'] == 'Elastik Demonstration School')].index
    df_test_usage = df_test_usage.drop(index_names)
    df_test_usage = df_test_usage.sort_values('startedcomplete')
    print(df_test_usage)
    return df_test_usage

# make a content created tracker
