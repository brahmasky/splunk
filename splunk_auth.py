#!/usr/bin/env python

import re, sys, shutil, os, subprocess, argparse
from datetime import datetime

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

def valid_workspace(s, pat=re.compile(r"cba-a-(cl|np|pr)-(\d{7})-.*")):
    matcher = pat.match(s)
    if not matcher:
        msg = 'unable to parse workspace name'
        raise argparse.ArgumentTypeError(msg)
    ci = matcher.group(2)
    return s, ci

def read_file(filename):
    config = ConfigParser()
    config.optionxform = str
    config.read(filename)
    return config

def write_file(config, filename):
    with open(filename, 'w') as configfile:
        config.write(configfile)

def backup(filename):
    now = datetime.now()
    new_name = '{}.{}'.format(filename, now.strftime('%Y%d%m%H%M%S'))
    print('Backing up {} to {}'.format(filename, new_name))
    shutil.copy(filename, new_name)

def add_authentication(workspace):
    updated = False
    workspace_name = workspace[0]
    ci = workspace[1]

    splunk_group_name = 'slg-curator-{}-user'.format(workspace_name)
    ad_group_name = 'SLG-Curator-{}-User'.format(workspace_name)
    filter = 'source=*{}* OR alias=*{}*'.format(ci,ci)

    authentication_config = read_file(authentication_file_name)

    if not authentication_config.has_option('roleMap_CBA-CNS-AWS-GA-Prod',splunk_group_name):
        backup(authentication_file_name)
        authentication_config.set('roleMap_CBA-CNS-AWS-GA-Prod',splunk_group_name, ad_group_name)
        write_file(authentication_config, authentication_file_name)
        updated = True
        print('Authentication file updated with new workspace {}.'.format(workspace_name))
    else:
        print('Authentication file already has workspace {}, skipping.'.format(workspace_name))

    return updated

def add_authorize(workspace):
    updated = False
    workspace_name = workspace[0]
    ci = workspace[1]

    authorization_config = read_file(authorization_file_name)
    authorization_role = 'role_slg-curator-{}-user'.format(workspace_name)
    ad_group_name = 'SLG-Curator-{}-User'.format(workspace_name)
    filter = 'source=*{}* OR alias=*{}*'.format(ci,ci)
    
    if not authorization_config.has_section(authorization_role):
        backup(authorization_file_name)
        authorization_config.add_section(authorization_role)
        authorization_config.set(authorization_role,'importRoles', 'user')
        authorization_config.set(authorization_role,'srchFilter', filter)
        authorization_config.set(authorization_role,'srchIndexesAllowed', 'cns_ga_prod_aws_cloudtrail;cns_ga_prod_aws_cloudwatch;cns_ga_prod_aws_curator_metrics;cns_ga_prod_aws_infra_curator;cns_ga_prod_aws_server_curator')
        authorization_config.set(authorization_role,'srchIndexesDefault', 'cns_ga_prod_aws_curator_metrics')
        authorization_config.set(authorization_role,'srchMaxTime', '0')
        write_file(authorization_config, authorization_file_name)
        updated = True
        print('Authorization file updated with new workspace - {}.'.format(workspace_name))
    else:
        print('Authorization file already has workspace {}, skipping.'.format(workspace_name))

    return updated

def remove_authentication(workspace):
    updated = False
    workspace_name = workspace[0]
    splunk_group_name = 'slg-curator-{}-user'.format(workspace_name)

    authentication_config = read_file(authentication_file_name)

    if authentication_config.has_option('roleMap_CBA-CNS-AWS-GA-Prod',splunk_group_name):
        backup(authentication_file_name)
        authentication_config.remove_option('roleMap_CBA-CNS-AWS-GA-Prod',splunk_group_name)
        write_file(authentication_config, authentication_file_name)
        updated = True
        print('Authentication file has workspace {} removed.'.format(workspace_name))
    else:
        print('Authentication file does not contain workspace {}, skipping.'.format(workspace_name))

    return updated

def remove_authorize(workspace):
    updated = False
    workspace_name = workspace[0]
    authorization_role = 'role_slg-curator-{}-user'.format(workspace_name)

    authorization_config = read_file(authorization_file_name)

    if authorization_config.has_section(authorization_role):
        backup(authorization_file_name)
        authorization_config.remove_section((authorization_role))
        write_file(authorization_config, authorization_file_name)
        updated = True
        print('Authorization file has workspace {} removed.'.format(workspace_name))
    else:
        print('Authorization file does not contain workspace {}, skipping.'.format(workspace_name))

    return updated


def apply_config(splunk_password):
    splunk_command = '/opt/splunk/bin/splunk apply shcluster-bundle --answer-yes -auth admin:{} -target https://splunk-shead1.cnsga.aws.prod.au.internal.cba:8089 -preserve-lookups true -push-default-apps true'.format(splunk_password)
    # print(splunk_command)
    return_code = subprocess.call(splunk_command, shell=True)
    if return_code != 0:
        print('Splunk command failed')
        exit(1)

parser = argparse.ArgumentParser()  
parser.add_argument('action', choices={"add", "remove"}, help='to ADD a workspace to, or to REMOVE a workspace from, Splunk_TA_auth configurations')
parser.add_argument('workspace', type=valid_workspace, help='AWS workspace name ')
parser.add_argument('-a', '--apply', help='if set, the splunk command would be invoked on Deployer to apply the configuration changes to the three Search Heads', action="store_true")
parser.add_argument('-p', '--password', help='if apply_bundle is set, the password for Splunk user is required to invoke the command')
args = parser.parse_args()  

authentication_file_name = '/opt/splunk/etc/shcluster/apps/Splunk_TA_auth/local/authentication.conf'
authorization_file_name = '/opt/splunk/etc/shcluster/apps/Splunk_TA_auth/local/authorize.conf'

# authentication_file_name = 'C:\\GHE\\myCodes\\authenticate.conf'
# authorization_file_name = 'C:\\GHE\\myCodes\\authorize.conf'

if args.action =="add":
    add_authentication(args.workspace)
    add_authorize(args.workspace)

if args.action == "remove":
    remove_authentication(args.workspace)
    remove_authorize(args.workspace)

if args.apply and (args.password is None):
    parser.error('Splunk user password is required when applying applying splunk configurations changes')

if args.apply:
    apply_config(args.password)
