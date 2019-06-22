import re, sys, shutil, os, subprocess
from datetime import datetime

try:
    from configparser import ConfigParser
    from configparser import MissingSectionHeaderError
except ImportError:
    from ConfigParser import ConfigParser

def usage():
    print("Param 1: host type = TEST/MDS/MDS_HF/LOCAL_HF")
    exit(1)

def read_file(filename):
    config = ConfigParser(comment_prefixes='#', allow_no_value=True, strict=False, interpolation=None)
    config.optionxform = str
    try:
        config.read(filename)
    except MissingSectionHeaderError:
        config.read(filename, encoding='utf-8-sig')
        print('ConfigParser is reading UTF-8-BOM file : {}'.format(filename))
    return config

def write_file(config, filename):
    with open(filename, 'w') as configfile:
        config.write(configfile)
    print('{} has been updated'.format(filename))

def backup(filename):
    now = datetime.now()
    new_name = '{}.{}'.format(filename, now.strftime('%Y%d%m%H%M%S'))
    print('Backing up {} to {}'.format(filename, new_name))
    shutil.copy(filename, new_name)

def is_splunk_forwarder(path):
    matcher = False
    pat = re.compile(r".*(SplunkForwarder|SplunkLightForwarder).*", re.IGNORECASE)
    matcher = pat.match(path)
    return matcher    

def search_transforms_routing(config, list):
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if (each_key == 'DEST_KEY' and each_val == '_TCP_ROUTING'):
                #print('TRANSFORMS: {} = {}'.format(each_key, each_val))
                list.append(each_section)
    return list

def comment_outputs_tcpout(file):
    updated = False
    config = read_file(file)
    for each_section in config.sections():
        if each_section.startswith('tcpout'):
            for (each_key, each_val) in config.items(each_section):
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
            updated = True
    if updated:
        backup(file)
        write_file(config, file)       
    return updated

def comment_props_by_routing(file, list):
    updated = False
    config = read_file(file)
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if each_val in list:
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                updated = True
    if updated:
        backup(file)
        write_file(config, file)   
    return updated

def comment_inputs_routing(file):
    updated = False
    config = read_file(file)
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if each_key == '_TCP_ROUTING':
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                updated = True
    if updated:
        backup(file)
        write_file(config, file)      
    return updated

def update_hf_files(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        if not is_splunk_forwarder(subdir):
            for file in files:
                if file == "outputs.conf": 
                    outputs_file = os.path.join(subdir, file)
                    comment_outputs_tcpout(outputs_file)
                if file == "transforms.conf":
                    transforms_file = os.path.join(subdir, file)
                    transforms_config = read_file(transforms_file)

                    routing_list = []
                    routing_list = search_transforms_routing(transforms_config, routing_list)

                    if len(routing_list) > 0: 
                        props_file = os.path.join(subdir, "props.conf")
                        comment_props_by_routing(props_file, routing_list)

                if file == "inputs.conf":
                    inputs_file = os.path.join(subdir, file)
                    comment_inputs_routing(inputs_file)
        else:
            print('Ignorning forwarder path: {}'.format(subdir))

def copy_outputs(local_outputs, new_outputs):
    local_outputs_config = read_file(local_outputs)
    new_outputs_config = read_file(new_outputs)
    copied = False
    for each_section in local_outputs_config.sections():
        if each_section != 'tcpout':
            new_outputs_config.add_section(each_section)
            for (each_key, each_val) in local_outputs_config.items(each_section):
                new_outputs_config.set(each_section, each_key, each_val)
            copied = True
    
    if copied:
        backup(new_outputs)
        write_file(new_outputs_config, new_outputs)
    
    return copied

def update_local_output(splunk_home):
    sytem_local_output = '{}/etc/system/local/outputs.conf'.format(splunk_home)
    new_output = '{}/apps/cba_output/local/outputs.conf'.format(splunk_home)

    # copy non-tcpout section to new outputs
    copied = copy_outputs(sytem_local_output, new_output)
    # comment out all tcpout sections in system local
    commented = comment_outputs_tcpout(sytem_local_output)
    
    return copied and commented

def copy_new_apps():

    return True

# === main flow ===

if len(sys.argv) < 2:
    host_type = 'TEST'
elif len(sys.argv) == 2:
    host_type = sys.argv[1]
elif len(sys.argv) > 2:
    usage()

pat = re.compile(r"(TEST|MDS|MDS_HF|LOCAL_HF)$")
matcher = pat.match(host_type)
if not matcher:
    usage()

if host_type == 'TEST':
    #scan a local repo and process all the relevant files
    workingdir = 'C:/GHE/DEA/splunk_mds_copy/deployment-apps'
    update_hf_files(workingdir)
if host_type == 'MDS':
    #scan and process $SPLUNK_HOME/etc/deployment-apps
    splunk_home = os.environ['SPLUNK_HOME']
    workingdir = '{}/etc/deployment-apps'.format(splunk_home)
    update_hf_files(workingdir)
    # rename and copy the 2 new apps for all FWDs (S2/S3/S4)
    ...
if host_type == 'MDS_HF':
    # make sure MDS has been updated and the specific host/forwarder has been reloaded from MDS
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    splunk_home = os.environ['SPLUNK_HOME']
    update_local_output(splunk_home)

if host_type == 'LOCAL_HF':
    #scan and process $SPLUNK_HOME/etc/apps folder
    splunk_home = os.environ['SPLUNK_HOME']
    workingdir = '{}/etc/apps'.format(splunk_home)
    update_hf_files(workingdir)
    # copy the 2 new apps
    ...
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    update_local_output(splunk_home) 

