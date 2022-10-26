import datetime
import pickle
from pathlib import Path
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import random
import pandas as pd
import datetime
import altair as alt
from github import Github
import boto3
import time
from data_helpers import *
from s3fs.core import S3FileSystem
import os

# get set up
# with open('/Users/william/Desktop/Elastik/awskeys/keys.txt') as keys:
#     lines = keys.readlines()§
#     key_id = lines[0].replace('\n','')
#     key = lines[1]
# print(key_id)
# print(key)
# print(lines)

# key_id = st.secrets['key_id']
# key = st.secrets['key']

key_id = os.environ['key_id']
key = os.environ['key']

def setup_session(key_id, key):
    return boto3.Session(aws_access_key_id=key_id,
                         aws_secret_access_key=key)


def setup_resource(resource, bucket):
    session = setup_session(key_id, key)
    my_resource = session.resource(resource)
    global target_bucket
    target_bucket = my_resource.Bucket(bucket)
    return session, my_resource, target_bucket


setup_session(key_id, key)

setup_resource('s3', 'elastikdashboard')

# load in the data
print('--- reading bucket ---')
for object_summary in target_bucket.objects.filter(Prefix='test-run-1/'):
    print(object_summary.key)
print(' --- finished bucket read --- ')

bucket_dict = {'assigned': '', 'performance': '', 'usage': '', 'logins': ''}
files = target_bucket.objects.filter(Prefix='test-run-1/')
files = [obj.key for obj in sorted(files, key=lambda x: x.last_modified, reverse=False)]

for i, i2 in enumerate([k for j, k in enumerate(files) if j % 2 != 0]):
    bucket_dict[list(bucket_dict.keys())[i]] = i2
print('\nhere are the csvs which will be read: \n', bucket_dict)

# s3 = S3FileSystem(anon=False,key=key_id,secret=key)

school_performance = get_comparisons('performance')
print(school_performance.columns)
school_tests = get_tests_assigned('usage')
df_average_year = time_logins('logins')
avg = avg_logins_transform('logins')
df_average_month1 = time_logins_month('logins')
df = time_logins_df('logins')

print('here are all dfs')
print('\n', school_performance)
print('\n', school_tests)
print('\n', df)
print('\n', avg)

dict_school_keys = {'English Martyrs': 0, 'Kings Ely': 1, 'Wetherby Prep': 2, 'Parkside': 3, 'St Pauls': 4,
                    'St Francis': 5, 'Sacret Heart': 6,
                    'Danes Hill': 7, 'Hatfield Wick': 8, 'Mayville': 9, 'St Marks': 10, 'Parkgate': 11,
                    'St Monicas': 12, 'Our Lady': 13, 'St Andrew': 14,
                    'All': 15}

st.set_page_config(page_title='Elastik Dashboard', page_icon=':rocket:')


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl('https://assets9.lottiefiles.com/private_files/lf30_TBKozE.json')

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader('Elastik Dashboard')
        st.title('Potential. Unleashed.')
        st.write('The Elastik data team has built and compiled new insights into school performance and usage.')
    with right_column:
        st_lottie(lottie_coding, height=300, key='coding')


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] in st.secrets["passwords"] and st.secrets["passwords"][
            st.session_state["username"]] == st.session_state["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


st.write("---")

if check_password():
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader('Platform Engagement')
            st.metric("Today's Logins", df['users'].iloc[0], str(df['users'].iloc[0] - df['users'].iloc[1]))
            st.metric("Average Daily Logins in Last 30 Days", df_average_month1,
                      str(df_average_month1 - df_average_year))
            st.metric("Schools on Platform", "22", "0")
        with right_column:
            st_lottie(load_lottieurl('https://assets9.lottiefiles.com/packages/lf20_l3qxn9jy.json'), height=300,
                      key='metrics')
        st.write("---")

        st.subheader('Total User Activity')

        st.line_chart(data=avg, y='users', width=0, height=0, use_container_width=True)
        st.write('---')

        st.subheader('Best Performance')

        left_column, left_column2, right_column, right_column2 = st.columns(4)
        school_tests_no_nan_perf = school_performance.dropna(axis=0)
        best_performing = school_tests_no_nan_perf['schoolName'].head(3)
        best_scores = school_tests_no_nan_perf['score'].head(3)
        with left_column:
            st.metric(best_performing.iloc[0], round(best_scores.iloc[0]))
        with left_column2:
            st_lottie(load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_rZQs81.json'), height=100,
                      key='performance')

        with right_column:
            st.metric(best_performing.iloc[1], round(best_scores.iloc[1]))
        with right_column2:
            st_lottie(load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_3u6uxdsw.json'), height=100,
                      key='performance2')

        st.write('---')

        st.subheader('Assessment Completion Rate')

        left_column, right_column = st.columns(2)

        with left_column:
            school_tests_no_nan = school_tests.dropna(axis=0)
            worst_performing = school_tests_no_nan['schoolName'].head(3)
            worst_scores = school_tests_no_nan['startedcomplete'].head(3)
            st.metric(worst_performing.iloc[0], str(round(worst_scores.iloc[0] * 100)) + '%')
            st.metric(worst_performing.iloc[1], str(round(worst_scores.iloc[1] * 100)) + '%')
            st.metric(worst_performing.iloc[2], str(round(worst_scores.iloc[2] * 100)) + '%')

        with right_column:
            st_lottie(load_lottieurl('https://assets4.lottiefiles.com/private_files/lf30_VuL9i1.json'), height=300,
                      key='hazard')

        st.write('---')

        st.subheader('School assessment completion rate')
        # left_column, right_column, = st.columns(2)
        # with left_column:
        option = st.selectbox('Select a School.',
                                ['All', 'English Martyrs', 'Kings Ely', 'Wetherby Prep', 'Parkside', 'St Pauls',
                                'St Francis', 'Sacret Heart', 'Danes Hill', 'Hatfield Wick', 'Mayville', 'St Marks',
                                'Parkgate', 'St Monicas', 'Our Lady', 'St Andrew'])
        # with left_column:
    from matplotlib import pyplot as plt
    import seaborn as sns
    chart1 = alt.Chart(school_tests_no_nan).mark_bar().encode(x='schoolName',y='assignedcomplete')
            # fig = plt.figure()
            # fig.facecolor('none')
            # sns.barplot(data=school_tests,x='schoolName',y='assignedcomplete')
            # st.pyplot(fig)
    st.altair_chart(chart1)
    st.write(school_tests)
        # with left_column:
        #     st.bar_chart(x=school_tests['schoolName'].all(),y=school_tests['assignedcomplete'].all(), use_container_width=True)
