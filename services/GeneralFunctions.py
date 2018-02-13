from services import settings
from services import root_dir

def create_json_object_from_dict(in_dict):
    load = {}
    rankings_json = []
    carrier = {'Violations': None, 'CarrierName': None, 'Difference in ' + settings.INPUT.upper(): None, 'Percentage': None}

    for key, values in in_dict.items():
        load['LOAD'] = key
        rankings_json.append(load)
        for value in values:
            carrier['Violations'] = str(value[0])
            carrier['CarrierName'] = str(value[1])
            carrier['Difference in ' + settings.INPUT.upper()] = str(value[2])
            carrier['Percentage'] = str(value[3])
            rankings_json.append(carrier)
            carrier = {}
        load = {}
    return rankings_json

def get_sorted_dict_from_data(loads):

    load_keys = dict()
    keys = loads.groups.keys()

    for name, g in loads:
        sf = name
        load_keys.setdefault(sf, [])

    for i in keys:
        lf = loads.get_group(i)
        load_carriers = lf.groupby(settings.CARRIER)
        carrier_keys = load_carriers.groups.keys()
        tmp_list = []
        for j in carrier_keys:
            lf_carrier = load_carriers.get_group(j)
            total_cnt = len(lf_carrier)
            lf_1 = lf_carrier[lf_carrier[settings.PLANINPUTVALUE] != lf_carrier[settings.EXECINPUTVALUE]]
            after_mismatch_eta = len(lf_1[lf_1 == True])
            tmp_list.append(after_mismatch_eta)
            tmp_list.append(lf_carrier.iloc[0][settings.CARRIER])
            tmp_list.append(lf_carrier[settings.DIFF].sum())
            tmp_list.append(((total_cnt - after_mismatch_eta) / total_cnt) * 100)
            load_keys.setdefault(i, []).append(tmp_list)
            tmp_list = []

    sorted_loads = {}
    for key, value in load_keys.items():
        sorted_loads[key] = sorted(value, key=lambda x: (x[0], x[2]))

    return sorted_loads

def get_sorted_dict_from_specific_load_data(specific_load):

    load_keys = dict()
    load_keys.setdefault(settings.LOADID, [])

    load_carriers = specific_load.groupby(settings.CARRIER)
    carrier_keys = load_carriers.groups.keys()
    tmp_list = []
    for j in carrier_keys:
        lf_carrier = load_carriers.get_group(j)
        total_cnt = len(lf_carrier)
        lf_1 = lf_carrier[lf_carrier[settings.PLANINPUTVALUE] != lf_carrier[settings.EXECINPUTVALUE]]
        after_mismatch_eta = len(lf_1[lf_1 == True])
        tmp_list.append(after_mismatch_eta)
        tmp_list.append(lf_carrier.iloc[0][settings.CARRIER])
        tmp_list.append(lf_carrier[settings.DIFF].sum())
        tmp_list.append(((total_cnt - after_mismatch_eta) / total_cnt) * 100)
        load_keys.setdefault(settings.LOADID, []).append(tmp_list)
        tmp_list = []

    sorted_loads = {}
    for key, value in load_keys.items():
        sorted_loads[key] = sorted(value, key=lambda x: (x[0], x[2]))

    return sorted_loads

def get_json_file():
    parent_root_dir_ = root_dir()
    json_file = parent_root_dir_ + "/database/" + settings.JSONFILE
    return json_file