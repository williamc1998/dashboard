# dashboard
## automated live dashboard with data stream to be deployed on ec2
this repo will be cloned on an ec2 instance and glue.py will be scheduled to run x times per day while elastikdashboard.py will run once and be left running as a constant process on the vm that keeps the app up

the next big task is to clean up the code, add more dynamic reading and solve final error

* query.txt files are SQL queries
* this should all run fine on 1gb memory until more data is used
* access key should not be made public