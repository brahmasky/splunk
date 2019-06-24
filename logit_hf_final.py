import re, sys, shutil, os, errno
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

def search_transforms_routing(file):
    list = []
    config = read_file(file)
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if (each_key == 'DEST_KEY' and each_val == '_TCP_ROUTING'):
                #print('TRANSFORMS: {} = {}'.format(each_key, each_val))
                list.append(each_section)
    return list

def comment_outputs_tcpout(file):
    commented = False
    config = read_file(file)
    for each_section in config.sections():
        if each_section.startswith('tcpout'):
            for (each_key, each_val) in config.items(each_section):
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
            commented = True
    if commented:
        backup(file)
        write_file(config, file)       
    return commented

def comment_props_by_routing(file, list):
    commented = False
    config = read_file(file)
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if each_val in list:
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                commented = True
    if commented:
        backup(file)
        write_file(config, file)   
    return commented

def comment_inputs_routing(file):
    commented = False
    config = read_file(file)
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            if each_key == '_TCP_ROUTING':
                commented_line = '# {} = {}'.format(each_key,each_val)
                config.remove_option(each_section, each_key)
                config.set(each_section, commented_line)
                commented = True
    if commented:
        backup(file)
        write_file(config, file)      
    return commented

def update_hf_files(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        if not is_splunk_forwarder(subdir):
            for file in files:
                if file == "outputs.conf": 
                    outputs_file = os.path.join(subdir, file)
                    comment_outputs_tcpout(outputs_file)
                if file == "transforms.conf":
                    transforms_file = os.path.join(subdir, file)
                    routing_list = []
                    routing_list = search_transforms_routing(transforms_file)

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

def update_mds_serverclass(splunk_home):
    updated = False
    forwarder_list=['S2_FWD01','S3_FWD01','S3_FWD02','S3_FWD03','S3_FWD04','S4_FWD01']
    apps_list = ['00_cba_sx_fwd0x_hf_outputs_to_aws_prod_ssl', '00_cba_sx_fwd0x_hf_outputs_to_aws_prod_indexer_discovery']
    for fowarder in fowarder_list:
        # C:\GHE\DEA\splunk_mds\apps\S2_FWD01-serverclass\local\serverclass.conf
        serverclass = '{}/apps/{}-serverclass/local/serverclass.conf'.format(splunk_home, fowarder)
        serverclass_config = read_file(serverclass)
        backup(serverclass)
        for apps in apps_list:
            section = 'serverClass:{}:app:{}'.format(fowarder, apps)
            serverclass_config.set(section, 'restartSplunkWeb', '0')
            serverclass_config.set(section, 'restartSplunkd', '1')
            serverclass_config.set(section, 'stateOnClient', 'enabled')
        write_file(serverclass_config, serverclass)


def copy_dir(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def copy_new_apps(working_dir, zone='MDS'):
    copied = False
    if zone == 'MDS':
        zone_name = 'sx_fwd0x'
    else:
        zone_name == zone.lower()
    
    print('zone_name == {}'.format(zone_name))
    apps_list = ['00_cba_zoneName_hf_outputs_to_aws_prod_ssl', '00_cba_zoneName_hf_outputs_to_aws_prod_indexer_discovery']

    for apps in apps_list:
        source_dir = '/tmp/hf_routing/{}'.format(apps)
        if os.path.isdir(source_dir):
            dst_app = apps.replace('zoneName', zone_name)
            dst_dir = '{}/{}'.format(working_dir, dst_app)
            print('souce: {} ==> dst: {}'.format(source_dir, dst_dir))
            copy_dir(source_dir, dst_dir)
            copied = True
    return copied

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
    working_dir = 'C:/GHE/DEA/splunk_mds_copy/deployment-apps'
    update_hf_files(working_dir)
if host_type == 'MDS':
    #scan and process $SPLUNK_HOME/etc/deployment-apps
    splunk_home = os.environ['SPLUNK_HOME']
    working_dir = '{}/etc/deployment-apps'.format(splunk_home)
    update_hf_files(working_dir)
    # rename and copy the 2 new apps to $SPLUNK_HOME/etc/deployment-apps
    if copy_new_apps(working_dir):
        #if copy is successful, update serverclass for all forwarders
        update_mds_serverclass(splunk_home)
if host_type == 'MDS_HF':
    # make sure MDS has been updated and the specific host/forwarder has been reloaded from MDS
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    splunk_home = os.environ['SPLUNK_HOME']
    update_local_output(splunk_home)

if host_type == 'LOCAL_HF':
    #scan and process $SPLUNK_HOME/etc/apps folder
    splunk_home = os.environ['SPLUNK_HOME']
    working_dir = '{}/etc/apps'.format(splunk_home)
    update_hf_files(working_dir)
    # manually copy the 2 new apps
    copy_new_apps(working_dir, zone)
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    update_local_output(splunk_home) 
