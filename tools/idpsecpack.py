#!/usr/bin/env python

import argparse
import time
import xml.etree.ElementTree as ET

from jnpr.junos import Device

parser = argparse.ArgumentParser(description='Process user input')
parser.add_argument("--host", dest="host", default="",metavar="HOST",help="Specify host to connect to")
parser.add_argument("--username", dest="username", metavar="USERNAME",help="Specify the username")
parser.add_argument("--password", dest="password", metavar="PASSWORD",help="Specify the password")
args = parser.parse_args()

host = args.host
username = args.username
password = args.password

#now lets connect to the device, load the template, and commit the changes
#first we instantiate an instance of the device
junos_dev = Device(host=host, user=username, password=password)
#now we can connect to the device
junos_dev.open()
#run the RPC to get the support information
download_result = junos_dev.rpc.request_idp_security_package_download()
#output to a sting
print ET.tostring(download_result,encoding="utf8", method="text")

#loop through status until OK is seen
while True:
    download_status = junos_dev.rpc.request_idp_security_package_download(status=True)
    print ET.tostring(download_status,encoding="utf8", method="text")
    #look for done
    info = download_status.findtext('secpack-download-status-detail')
    print info
    time.sleep(2)

install_result = junos_dev.rpc.request_idp_security_package_install()
#output to a sting
print install_result

#loop through status until OK is seen
while True:
    install_status = junos_dev.rpc.request_idp_security_package_install(status=True)
    print ET.tostring(install_status,encoding="utf8", method="text")
    info = download_status.findtext('secpack-status-detail')
    print info
    time.sleep(2)
