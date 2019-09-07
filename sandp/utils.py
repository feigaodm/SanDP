"""Convert root into pandas dataframe
"""
from root_numpy import root2array
import pandas as pd
import numpy as np
import os
from textwrap import dedent
from pymongo import MongoClient
from tqdm import tqdm


def load_dataframe(filename, amplifier=10):
    """convert ROOT file into dataframe format.

    :param filename: file name including the path
    :return data: data in pandas dataframe format
    """
    data_1 = pd.DataFrame(root2array(filename, 'T1'))

    array_branches = []
    scalar_branches = ['BaseLineChannel', 'BaseLineChannelSigma', 'S2sPMT']  # these two are not scalar
    # columns that we want two peaks from them
    column_two = ['S2sPeak', 'S1sPeak', 'S1sTot', 'S2sTot', 'S2sPosX', 'S2sPosY']
    for name in data_1.columns.values:
        if name in scalar_branches:
            continue
        if hasattr(data_1[name][0], '__len__'):
            if name in column_two:
                continue
            array_branches.append((name, np.nan))
            # TODO add length to different array
        else:
            scalar_branches.append(name)

    data_2 = pd.DataFrame(root2array(filename, branches=array_branches))

    data = pd.concat([data_1[scalar_branches], data_2], axis=1)

    # Add S1 S2 info including second s1 and s2
    info = {
        'S1sTot': {
            'array_branches': ('S1sTot', np.nan, 2),
            'column_name': ['s1', 'largest_other_s1']
        },
        'S2sTot': {
            'array_branches': ('S2sTot', np.nan, 2),
            'column_name': ['s2', 'largest_other_s2']
        },
        'S1sPeak': {
            'array_branches': ('S1sPeak', np.nan, 2),
            'column_name': ['s1_time', 'alt_s1_time']
        },
        'S2sPeak': {
            'array_branches': ('S2sPeak', np.nan, 2),
            'column_name': ['s2_time', 'alt_s2_time']
        },
        'S2sPosX': {
            'array_branches': ('S2sPosX', np.nan, 2),
            'column_name': ['x', 'alt_s2_x']
        },
        'S2sPosY': {
            'array_branches': ('S2sPosY', np.nan, 2),
            'column_name': ['y', 'alt_s2_y']
        }
    }
    for name, content in info.items():
        data_tmp = pd.DataFrame(data=root2array(filename, branches=content['array_branches']),
                                columns=content['column_name'])
        data = pd.concat([data, data_tmp], axis=1)

    # convert time from sample to us
    sample_to_us = 4 / 1e3
    time_columns = ['s1_time', 'alt_s1_time', 's2_time', 'alt_s2_time', 'S1sWidth', 'S1sLowWidth',
                    'S2sLowWidth', 'S2sWidth']
    for column in time_columns:
        data.loc[:, column] *= sample_to_us

    # divide signal by 10
    # TODO: just for temporal purpose. put this in processor in the future and remove these lines
    if amplifier:
        signal_columns = ['s1', 'largest_other_s1', 's2', 'largest_other_s2']
        for column in signal_columns:
            data.loc[:, column] /= amplifier

    # add alias
    data['drift_time'] = data['s2_time'] - data['s1_time']  # us
    data['r'] = np.sqrt(data['x'] ** 2 + data['y'] ** 2)

    return data


def load_path(path, amplifier=10):
    """Load all root files from specific path
    """
    assert isinstance(path, (str, list)), "path should be either string or list type"

    if isinstance(path, str):
        files = os.listdir(path)
        full_file_path_s = [os.path.join(path, file) for file in files if '.root' in file]

        data = load_dataframe(full_file_path_s, amplifier)
    else:
        data = pd.DataFrame()
        for path_ in path:
            data_tmp = load_path(path_)
            data = pd.concat([data, data_tmp], ignore_index=True)
    return data


def get_coll():
    """get data collection info from mongodb"""
    client = MongoClient('mongodb://sandix:%s@132.239.186.12:27017' % os.environ['MONGO_PASSWORD'])
    db = client['run']
    coll = db['data']
    return coll


def get_datasets():
    """get run info as pd dataframe"""
    coll = get_coll()
    doc_s = list(coll.find())
    datasets = pd.DataFrame(doc_s)
    return datasets.drop(['_id', 'processed_data_location'], axis=1)


def load(run_numbers, processor='sandix_v1.1'):
    """load data into pd dataframe by run numbers"""
    if not isinstance(run_numbers, list):
        run_numbers = run_numbers.tolist()
    coll = get_coll()
    doc_s = list(coll.find({'run_number': {'$in': run_numbers}}))

    data = pd.DataFrame()

    if processor == 'sandix_v1.1':
        name = 'sandix_v1p1'
    elif processor == 'sandp_test':
        name = 'sandp_test'
    else:
        raise ValueError("processor is either 'sandix_v1.1' or 'sandp_test', wanna try again?")

    for doc in tqdm(doc_s, desc='load data'):
        if doc['amplifier_on']:
            amplifier = 10
        else:
            amplifier = 1
        data_tmp = load_dataframe(doc['processed_data_location'][name], amplifier=amplifier)
        data_tmp['run_number'] = doc['run_number']
        data = pd.concat([data, data_tmp], ignore_index=True)

    return data


def code_hider():
    """Stolen from hax
    Make a button in the jupyter notebook to hide all code
    """
    # Stolen from stackoverflow... forget which question
    # I would really like these buttons for every individual cell.. but I don't know how
    from IPython.display import HTML  # Please keep here, don't want hax to depend on ipython!
    return HTML(dedent('''
                       <script>
                       code_show=true
                       function code_toggle() {
                        if (code_show){
                        $('div.input').hide();
                          } else {
                        $('div.input').show();
                        }
                        code_show = !code_show
                       }
                       $( document ).ready(code_toggle);
                       </script>
                       <form action="javascript:code_toggle()"><input type="submit"
                       value="Show/hide  all code in this notebook"></form>'''))
