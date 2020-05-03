"""
Job driver for distributed workloads.
Written by Gautam Mittal.
"""
import subprocess

def update():
    import subprocess

def get_ips():
    with open('ips.txt', 'r') as f:
        content = f.readlines()
    return [x.strip() for x in content]

def start_job():
    servers = get_ips()
    