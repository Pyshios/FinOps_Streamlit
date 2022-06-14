### Pre-requisites Installation

1. Install packages:

pip3 install -r requirements.txt

2. Configure the AWS CLI:

aws configure

### Script Configuration:

Script configuration can be found in metrics.yaml.

1. period - This is the period of the metrics to fetch. The default period is 5 minutes (300 seconds). This can be modified but note the below API limitations when modifying this value

- If hours specified below is between 3 hours and 15 days ago - Use a multiple of 60 seconds for the period (1 minute) else no datapoint will be returned by the API.
- If hours specified below is between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes) else no datapoint will be returned by the API.
- If hours specified below is greater than 63 days ago - Use a multiple of 3600 seconds (1 hour) else no datapoint will be returned by the API

2. hours - This is the amount of hours prior worth of metrics you want to fetch. The default is 1hour, you can modify this to signify days but it must be specified in hours. For example 48 signifies 2 days

3. statistics - This is the global statistics that will be used when fetching metrics that do not have specific statistics assigned. For any metric that has statistics configured, this configuration will not be used.

### Script Usage

Run Python cwreport.py -h

Example syntax: python cwreport.py <service> <--region=Optional Region> <--profile=<Optional credential profile>

Parameters:
1. service (required) - This is the service you want to run the script against. The services currently supported are AWS Lambda, Amazon EC2, Amazon RDS, Application Load Balancer, Network Load Balancer and Amazon API Gateway
2. region (optional) - This is the region to fetch metrics from. Default region is ap-southeast-1
3. profile (optional) - This is the AWS CLI named profile to use. If specified, the default configured credential is not used

Examples:
1) Using default region "ap-southeast-1" and default configured credentials to fetch Amazon EC2 metrics: python cwreport.py ec2
1) With Region Specified and fetching Amazon API Gateway metrics: python cwreport.py apigateway --region us-east-1
3) With AWS profile specified: python cwreport.py ec2 --profile testprofile
4) With both region and profile specified: python cwreport.py ec2 --region us-east-1 --profile testprofile
