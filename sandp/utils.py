from root_numpy import root2array
import pandas as pd
import numpy as np

def get_dataframe(filename):
    '''
    convert ROOT file into dataframe format.
    :param filename: file name including the path
    :return data: data in pandas dataframe format
    '''
    data_1 = pd.DataFrame(root2array(filename, 'T1'))

    array_branches = []
    scalar_branches = ['BaseLineChannel', 'BaseLineChannelSigma']  # these two are not scalar
    for name in data_1.columns.values:
        if name in scalar_branches:
            continue
        if hasattr(data_1[name][0], '__len__'):
            array_branches.append((name, np.nan))
            #TODO add length to different array
        else:
            scalar_branches.append(name)

    data_2 = pd.DataFrame(root2array(filename, branches=array_branches))

    data = pd.concat([data_1[scalar_branches], data_2], axis=1)
    return data