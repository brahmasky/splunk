import re, sys, shutil, os, errno, fnmatch, getpass, codecs, tempfile
from os.path import isdir, join
from datetime import datetime

try:
    from configparser import ConfigParser, RawConfigParser, MissingSectionHeaderError
except ImportError:
    from ConfigParser import ConfigParser, RawConfigParser, MissingSectionHeaderError

def usage():
    print("Param 1: host type = TEST/MDS/MDS_HF/LOCAL_HF")
    print("Param 2: HF zone (IPNET/S3_MQ/CMC/SVDC/NPS/CAAS, required if host type is LOCAL_HF)")
    exit(1)

def replace_file_encoding(filename):
    replaced = False
    temp_file = '{}.tmp'.format(filename)
    with codecs.open(filename, 'r', encoding='utf-8-sig') as infile, codecs.open(temp_file, 'w+', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line)

    infile.close()
    outfile.close()
    if os.path.isfile(temp_file):
        backup(filename)
        os.remove(filename)
        shutil.move(temp_file, filename)
        replaced = True
    
    return True



def read_file(filename):
    try:
        config = ConfigParser(comment_prefixes='#', allow_no_value=True, strict=False, interpolation=None)
    except TypeError:
        config = RawConfigParser()

    config.optionxform = str
    try:
        config.read(filename)
    except MissingSectionHeaderError:
        print('ConfigParser is reading UTF-8-BOM file : {}'.format(filename))
        try:
            config.read(filename, encoding='utf-8-sig')
        except TypeError:
            replace_file_encoding(filename)
            config.read(filename)

    return config

def write_file(config, filename):
    with open(filename, 'w') as configfile:
        config.write(configfile)
    print('{} has been updated'.format(filename))

def backup(filename):
    now = datetime.now()
    new_name = '{}.{}'.format(filename, now.strftime('%Y%m%d%H%M%S'))
    print('Backing up {} to {}'.format(filename, new_name))
    shutil.copy(filename, new_name)
    return new_name

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

def update_local_output(splunk_home, new_output_dir):
    sytem_local_output = '{}/etc/system/local/outputs.conf'.format(splunk_home)
    new_output = '{}/local/outputs.conf'.format(new_output_dir)

    # copy non-tcpout section to new outputs
    copied = copy_outputs(sytem_local_output, new_output)
    # comment out all tcpout sections in system local
    commented = comment_outputs_tcpout(sytem_local_output)

    return copied and commented

def update_mds_serverclass(splunk_home):
    updated = False
    forwarder_list=['S2_FWD01','S3_FWD01','S3_FWD02','S3_FWD03','S3_FWD04','S4_FWD01']
    apps_list = ['00_cba_sx_fwd0x_hf_outputs_to_aws_prod_ssl', '00_cba_sx_fwd0x_hf_outputs_to_aws_prod_indexer_discovery']
    for fowarder in forwarder_list:
        serverclass = '{}/etc/apps/{}-serverclass/local/serverclass.conf'.format(splunk_home, fowarder)
        serverclass_config = read_file(serverclass)
        backup(serverclass)
        for apps in apps_list:
            section = 'serverClass:{}:app:{}'.format(fowarder, apps)
            serverclass_config.add_section(section)
            serverclass_config.set(section, 'restartSplunkWeb', '0')
            serverclass_config.set(section, 'restartSplunkd', '1')
            serverclass_config.set(section, 'stateOnClient', 'enabled')
        write_file(serverclass_config, serverclass)
        updated = True
    return updated


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
    new_output_dir = 'NO_OUTPUT'
    if zone == 'MDS':
        zone_name = 'sx_fwd0x'
    else:
        zone_name = zone.lower()

    apps_list = ['00_cba_zoneName_hf_outputs_to_aws_prod_ssl', '00_cba_zoneName_hf_outputs_to_aws_prod_indexer_discovery']

    for apps in apps_list:
        source_dir = '{}/{}'.format(temp_dir, apps)
        if os.path.isdir(source_dir):
            dst_app = apps.replace('zoneName', zone_name)
            dst_dir = '{}/{}'.format(working_dir, dst_app)
            if dst_dir.endswith('discovery'):
                new_output_dir = dst_dir
            print('souce: {} ==> dst: {}'.format(source_dir, dst_dir))
            copy_dir(source_dir, dst_dir)
            copied = True
    if copied:
        return new_output_dir

def check_apps_in_temp():
    app_copied = False
    apps_list = ['00_cba_zoneName_hf_outputs_to_aws_prod_ssl', '00_cba_zoneName_hf_outputs_to_aws_prod_indexer_discovery']
    for apps in apps_list:
        app_dir = '{}/{}'.format(temp_dir, apps)
        if os.path.isdir(app_dir):
            app_copied = True
        else:
            print('The two output apps {} have not been copied to {}'.format(apps_list, temp_dir))
            exit(1)

    return app_copied

def check_input(param, input):
    pat = re.compile(r"NO_MATCH")
    if param == 'host':
        pat = re.compile(r"(TEST|MDS|MDS_HF|LOCAL_HF)$")
    if param == 'zone':
        pat = re.compile(r"IPNET|S3_MQ|CMC|SVDC|NPS|CAAS")

    matcher = pat.match(input)
    if not matcher:
        usage()

def include_patterns(*patterns):
    """
    https://stackoverflow.com/questions/35155382/copying-specific-files-to-a-new-folder-while-maintaining-the-original-subdirect
    Function that can be used as shutil.copytree() ignore parameter that
    determines which files *not* to ignore, the inverse of "normal" usage.
    This is a factory function that creates a function which can be used as a
    callable for copytree()'s ignore argument, *not* ignoring files that match
    any of the glob-style patterns provided.
    'patterns' are a sequence of pattern strings used to identify the files to
    include when copying the directory tree.
    Example usage:
        copytree(src_directory, dst_directory,
                 ignore=include_patterns('*.sldasm', '*.sldprt'))
    """
    def _ignore_patterns(path, all_names):
        # Determine names which match one or more patterns (that shouldn't be
        # ignored).
        keep = (name for pattern in patterns
                        for name in fnmatch.filter(all_names, pattern))
        # Ignore file names which *didn't* match any of the patterns given that
        # aren't directory names.
        dir_names = (name for name in all_names if isdir(join(path, name)))
        return set(all_names) - set(keep) - set(dir_names)

    return _ignore_patterns

def backup_conf(src_dir, dst_dir):
    # Make sure the destination folder does not exist.
    if os.path.exists(dst_dir) and os.path.isdir(src_dir):
        print('removing existing directory "{}"'.format(dst_dir))
        shutil.rmtree(dst_dir, ignore_errors=False)

    shutil.copytree(src_dir, dst_dir, ignore=include_patterns('*.conf'))

def backup_splunk(splunk_home, backup_dir):
    backuped = False
    relevant_dirs=['deployment-apps', 'apps', 'system/local']
    for dir in relevant_dirs:
        #LOCAL src_dir = '{}/etc/{}'.format(splunk_home, dir)
        src_dir = '{}/{}'.format(splunk_home, dir)
        if os.path.isdir(src_dir):
            dst_dir = '{}/etc/{}'.format(backup_dir, dir)
            backup_conf(src_dir, dst_dir)
            backuped = True

    return backuped

# === main flow ===
if len(sys.argv) < 2:
    host_type = 'TEST'
elif len(sys.argv) >= 2:
    host_type = sys.argv[1]
    check_input('host', host_type)
    if host_type == 'LOCAL_HF':
        if len(sys.argv) < 3:
            usage()
        hf_zone = sys.argv[2]
        check_input('zone', hf_zone)
elif len(sys.argv) > 3:
    usage()


user = getpass.getuser()
if os.name == 'posix':
    temp_dir = '/tmp/hf_routing'
    if user != 'splunk':
        temp_dir = '/tmp/{}/hf_routing'.format(user)
if os.name == 'nt':
    temp_dir = 'C:/Temp/hf_routing'

testing = True

if host_type == 'TEST':
    #scan a local repo and process all the relevant files
    splunk_home = 'C:/GHE/DEA/splunk_svdc02_manual'
    backup_dir = '{}/{}'.format(temp_dir, host_type.lower())
    check_apps_in_temp()

    print('backup_dir = {}'.format(backup_dir))
    backup_splunk(splunk_home, backup_dir)
    #test is going to be worked on backuped files
    working_dir = '{}/etc/apps'.format(backup_dir)
    update_hf_files(working_dir)

    new_output_dir = copy_new_apps(working_dir, 'SVDC')
        #if copy is successful, update serverclass for all forwarders
    #update_mds_serverclass(backup_dir)
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    update_local_output(backup_dir, new_output_dir)

if host_type == 'MDS':
    check_apps_in_temp()
    #scan and process $SPLUNK_HOME/etc/deployment-apps
    splunk_home = os.environ['SPLUNK_HOME']
    backup_dir = '{}/{}'.format(temp_dir, host_type.lower())
    backup_splunk(splunk_home, backup_dir)
    if testing:
        splunk_home = backup_dir

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
    backup_dir = '{}/{}'.format(temp_dir, host_type.lower())
    backup_splunk(splunk_home, backup_dir)
    if testing:
        splunk_home = backup_dir

    new_output_dir = '{}/etc/apps/00_cba_sx_fwd0x_hf_outputs_to_aws_prod_indexer_discovery'.format(splunk_home)
    if os.path.isdir(new_output_dir):
        update_local_output(splunk_home, new_output_dir)
    else:
        print('The new outputs app has not been downloaded to this HF. Make sure this fowarder has been reloaded from MDS')
        exit(1)

if host_type == 'LOCAL_HF':
    #scan and process $SPLUNK_HOME/etc/apps folder
    check_apps_in_temp()
    splunk_home = os.environ['SPLUNK_HOME']
    backup_dir = '{}/{}'.format(temp_dir, host_type.lower())
    backup_splunk(splunk_home, backup_dir)
    if testing:
        splunk_home = backup_dir

    working_dir = '{}/etc/apps'.format(splunk_home)
    update_hf_files(working_dir)
    # manually copy the 2 new apps
    new_output_dir = copy_new_apps(working_dir, hf_zone)
    # process $SPLUNK_HOME/etc/system/local/outputs.conf file
    update_local_output(splunk_home, new_output_dir)
