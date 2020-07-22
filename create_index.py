import csv, sys
from configparser import ConfigParser

def read_file(filename):
    config = ConfigParser()
    config.optionxform = str
    config.read(filename)
    return config

def write_file(config, filename):
    with open(filename, 'w') as configfile:
        config.write(configfile)

def add_index(idx_name, is_metric, is_custom):
  updated = False
  idx_file = './std_indexes.conf'

  if is_custom:
    idx_file = './custom_indexes.conf'

  home_path = f'volume:hot_warm/{idx_name}/db'
  cold_path = f'volume:cold/{idx_name}/colddb'
  thawed_path = f'volume:cold/{idx_name}/thaweddb'
  
  idx_config = read_file(idx_file)

  if not idx_config.has_section(idx_name):
    idx_config.add_section(idx_name)
    idx_config.set(idx_name,'homePath',home_path)
    idx_config.set(idx_name,'coldPath',cold_path)
    idx_config.set(idx_name,'thawedPath',thawed_path)
    if is_metric:
      idx_config.set(idx_name,'datatype', 'metric')
    if is_custom:
      idx_config.set(idx_name,'frozenTimePeriodInSecs', '34190000')
    write_file(idx_config, idx_file)
    updated = True
  else:
    print(f'{idx_file} already has index {idx_name}')

  return updated


# sample stg_indexes_test.csv
# "stg_idx","stg_metric","stg_path"
# "index01",FALSE,"indexes_standard_retention"
# "index02",TRUE,"indexes_standard_retention"
# "index03",FALSE,"indexes_custom_retention"


with open('./stg_indexes_test.csv') as csv_file:
  csv_reader = csv.DictReader(csv_file, delimiter=',')
  headers = csv_reader.fieldnames
  idx_name = ''

  for line in csv_reader:
    idx_name = line["stg_idx"]
    is_metric = False
    is_custom = False 
    
    if line["stg_metric"] == 'TRUE':
      is_metric = True

    if line["stg_path"].endswith('custom_retention'):
      is_custom = True

    # print(f'{line["stg_idx"]}, {is_metric}, {is_custom}')
    add_index(idx_name, is_metric, is_custom)
