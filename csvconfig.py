"""
AWS Disclaimer.

(c) 2020 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the AWS Customer
Agreement available at https://aws.amazon.com/agreement/ or other written
agreement between Customer and Amazon Web Services, Inc.

This script is a module called by cwreport.py, it creates the csv file
"""
import yaml
import numpy

# Open the metrics configuration file metrics.yaml and retrive settings
with open("metrics.yaml", 'r') as f:
    metrics = yaml.load(f, Loader=yaml.FullLoader)


# Construct csv headers and return
def make_csv_header(service):
    if service == 'ec2':
        csv_headers = [
                'Name',
                'Instance',
                'Type',
                'Hypervisor',
                'Virtualization Type',
                'Architecture',
                'EBS Optimized',
                'CPUUtilization (Percent)',
                'DiskReadOps (Count)',
                'DiskWriteOps (Count)',
                'DiskReadBytes (Bytes)',
                'DiskWriteBytes (Bytes)',
                'NetworkIn (Bytes)',
                'NetworkOut (Bytes)',
                'NetworkPacketsIn (Count)',
                'NetworkPacketsOut (Count)'
            ]
        return csv_headers
    else:
        csv_headers = ['Resource Identifier']
        for metric in metrics['metrics_to_be_collected'][service]:
            csv_headers.append(metric['name']+" ("+metric['unit']+")")

        return csv_headers


# function to write to csv
def write_to_csv(service, csvwriter, resource, metrics_info):
    if service == 'ec2':
        # get instance name
        if resource.tags:
            name_dict = next(
                (i for i in resource.tags if i['Key'] == 'Name'),
                None)
        else:
            name_dict = None
        csvwriter.writerow([
            '' if name_dict is None else name_dict.get('Value'),
            resource.id,
            resource.instance_type,
            resource.hypervisor,
            resource.virtualization_type,
            resource.architecture,
            resource.ebs_optimized,
            numpy.round(numpy.average(metrics_info['CPUUtilization']), 2),
            numpy.round(numpy.average(metrics_info['DiskReadOps']), 2),
            numpy.round(numpy.average(metrics_info['DiskWriteOps']), 2),
            numpy.round(numpy.average(metrics_info['DiskReadBytes']), 2),
            numpy.round(numpy.average(metrics_info['DiskWriteBytes']), 2),
            numpy.round(numpy.average(metrics_info['NetworkIn']), 2),
            numpy.round(numpy.average(metrics_info['NetworkOut']), 2),
            numpy.round(numpy.average(metrics_info['NetworkPacketsIn']), 2),
            numpy.round(numpy.average(metrics_info['NetworkPacketsOut']), 2)
        ])

    else:
        row_data = [resource]
        for metric in metrics['metrics_to_be_collected'][service]:
            row_data.append(numpy.round(numpy.average(metrics_info[metric['name']]), 2))
        csvwriter.writerow(row_data)
