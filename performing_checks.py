import os
import socket
import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services import url_intel
from pangea.services import Audit
from pangea.services import file_intel
from pangea.services import redact
import pycurl
from io import BytesIO
import pycurl
import json

#setting up the environment variables
domain = os.getenv("PANGEA_DOMAIN")
token = os.getenv("PANGEA_TOKEN")
config = PangeaConfig(domain=domain)

def audit_log(message_dict):
    """_summary_

    Args:
        message_dict (_type_): a dictionary containing the message, action, actor, target, status, and source
    """
    # Create an audit object
    audit = Audit(token, config=config)
    print(f"Logging...")
    try:
        log_response = audit.log(
            message=message_dict['message'],
            action=message_dict['action'],
            actor=message_dict['actor'],
            target=message_dict['target'],
            status=message_dict['status'],
            source=message_dict['source'],
            verbose=True
        )
        print(f"Response: {log_response.result}")
    except pe.PangeaAPIException as e:
        # Catch exception in case something fails
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    return response


def url_checks(url):
    """_summary_

    Args:
        url (_type_): a string containing the url to be checked
    """
    # Create a URL object
    url_obj = URL(url, config=config)
    print(f"Checking URL...")
    try:
        url_response = url_intel.reputation(
                            url=url,
                            provider="crowdstrike",
                        )
        print(f"Response: {url_response.result}")
    except pe.PangeaAPIException as e:
        # Catch exception in case something fails
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    return response
    
def redact_check(test_info):
    """_summary_

    Args:
        test_info (_type_): a text containing the text to be checked
    """
    # Create a Redact object
    print(f"Checking Redact...")
    try:
        redact_response = redact.redact(text=text_info)
        print(f"Response: {redact_response.result}")
    except pe.PangeaAPIException as e:
        # Catch exception in case something fails
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    return response

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def ip_check():
    ip_address = get_ip()
    #Create an IP object
    print(f"Checking Redact...")
    ip_response = ip_intel.reputation(
            ip=ip_address,
            provider="crowdstrike",
        )
    print(f"Response: {ip_response.result}")
    except pe.PangeaAPIException as e:
        # Catch exception in case something fails
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    return response
        
def file_check(file_path):
    """_summary_

    Args:
        file_path (_type_): a file object to be checked
    """

    print(f"Checking File...")
    try:
        file_response = file_intel.filepathReputation(
            filepath=file_path,
            provider="reversinglabs",
        )
        print(f"Response: {file_response.result}")
    except pe.PangeaAPIException as e:
        # Catch exception in case something fails
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    return response

def check_sts(response, tag = "URL"):
    """_summary_

    Args:
        response (_type_): a response object to be checked
    """
    sts = False
    if response.result['data']['verdict'] == 'malicious':
        print(f"WARNING: This is a malicious {tag}")
    elif response.result['data']['vertict'] == 'suspicious':
        print("WARNING: This is a suspicious URL")
    else:
        print(f"This {tag} is safe")
        sts = True
    return sts

def signin_flow(username, pwd):
    url = 'https://authn.aws.us.pangea.cloud/v1/flow/verify/password'
    headers = [
        'Authorization: Bearer <your_token>',
        'Content-Type: application/json'
    ]
    data = {
        'flow_id': username,
        'password': pwd
    }

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.HTTPHEADER, headers)
    c.setopt(pycurl.POSTFIELDS, json.dumps(data))

    # Suppress the output (useful if you don't want to see the response in the console)
    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)

    c.perform()
    c.close()
    response_body = response_buffer.getvalue()
    response_json = json.loads(response_body.decode('utf-8'))
    return response_json

def signup_flow(username, pwd):
    url = 'https://authn.aws.us.pangea.cloud/v1/flow/signup/password'
    headers = [
        'Authorization: Bearer <your_token>',
        'Content-Type: application/json'
    ]
    data = {
        'flow_id': username,
        'password': pwd
    }

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.HTTPHEADER, headers)
    c.setopt(pycurl.POSTFIELDS, json.dumps(data))

    # Suppress the output (useful if you don't want to see the response in the console)
    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)

    c.perform()
    c.close()
    response_body = response_buffer.getvalue()
    response_json = json.loads(response_body.decode('utf-8'))
    return response_json
