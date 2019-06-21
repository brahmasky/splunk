import re, sys, shutil, os, subprocess
from datetime import datetime

try:
    from configparser import ConfigParser
    from configparser import MissingSectionHeaderError
except ImportError:
    from ConfigParser import ConfigParser

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

def search_routing_in_transforms(config, list):
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if (each_key == 'DEST_KEY' and each_val == '_TCP_ROUTING'):
                #print('TRANSFORMS: {} = {}'.format(each_key, each_val))
                list.append(each_section)
    return list

def config_comment_by_section_preix(config, section_prefix):
    updated = False
    for each_section in config.sections():
        if each_section.startswith(section_prefix):
            for (each_key, each_val) in config.items(each_section):
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
            updated = True
    return config, updated

def config_comment_by_option(config, option):
    updated = False
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            #print('INPUTS: {} = {}'.format(each_key, each_val))
            if each_key == option:
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                updated = True
    return config, updated

def config_comment_by_section_option(config, section, option):
    updated = False
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            #print('INPUTS: {} = {}'.format(each_key, each_val))
            if each_section == section and each_key == option:
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                updated = True
    return config, updated

def config_comment_by_keyvalue(config, list):
    updated = False
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            #print('PROPS: {} = {}'.format(each_key, each_val))
            if each_val in list:
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                updated = True
    return config, updated

# looping through configuration files under the rootdir
rootdir = 'C:/GHE/DEA/splunk_mds_copy'
workingdir = '{}/deployment-apps'.format(rootdir)
sytem_local_output = '{}/system/local/outputs.conf'.format(rootdir)

for subdir, dirs, files in os.walk(workingdir):
    if not is_splunk_forwarder(subdir):
        for file in files:
            if file == "outputs.conf": 
                outputs_file = os.path.join(subdir, file)
                outputs_config = read_file(outputs_file)
                if outputs_file == sytem_local_output: #copy 'defaultGroup' in [tcpout] stanza
                    new_output = '{}/apps/cba_output/local/outputs.conf'.format(rootdir)
                    system_local_outputs_config_updated = copy_local_to_new_output(sytem_local_output, new_output)

                #comment out all the options in outputs.conf under the apps
                outputs_config_updated = config_comment_by_section_preix(outputs_config, 'tcpout')

                if outputs_config_updated[1]:
                    # To comment out 'tcpout' stanza/section in outputs.conf
                    backup(outputs_file)
                    write_file(outputs_config_updated[0], outputs_file)
                    print('{} has been updated'.format(outputs_file))

            
            if file == "transforms.conf":
                transforms_file = os.path.join(subdir, file)
                # print('TRANSFORM file : {}'.format(transforms_file))
                transforms_config = read_file(transforms_file)

                routing_list = []
                routing_list = search_routing_in_transforms(transforms_config, routing_list)

                if len(routing_list) > 0: 
                    props_file = os.path.join(subdir, "props.conf")
                    # print('props file is {}'.format(props_file))
                    props_config = read_file(props_file)

                    props_config_updated = config_comment_by_keyvalue(props_config, routing_list)
                    if props_config_updated[1]:
                        backup(props_file)
                        write_file(props_config_updated[0], props_file)
                        print('{} has been updated'.format(props_file))
            
            if file == "inputs.conf":
                inputs_file = os.path.join(subdir, file)
                inputs_config = read_file(inputs_file)
                inputs_config_updated = config_comment_by_option(inputs_config, '_TCP_ROUTING')

                if inputs_config_updated[1]:
                    # To comment out '_TCP_ROUTING' option in inputs.conf
                    backup(inputs_file)
                    write_file(inputs_config_updated[0], inputs_file)
                    print('{} has been updated'.format(inputs_file))

    else:
        print('Ignorning forwarder path: {}'.format(subdir))


                



