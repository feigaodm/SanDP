"""
For single electron analysis
"""
import numpy as np
import pandas as pd
from root_numpy import root2array
import os
import matplotlib.pyplot as plt
from multihist import Histdd, Hist1d
from .utils import run_number_to_file_s, folders_to_file_s, judge_str
from tqdm import tqdm


def get_all_vector(ndarr):
    all_arr = []
    for arr in ndarr:
        [all_arr.append(e) for e in arr]

    return np.array(all_arr)


def get_all_vector_as_scalar(ndarr):
    """
    only select the first entry of a vector if it's non-empty
    """
    all_arr = []
    for arr in ndarr:
        if len(arr) > 0:
            [all_arr.append(arr[0]) for _ in arr]

    return np.array(all_arr)


def get_all_scalar(arr1, ndarr2):
    """
    vectorize a scalar based on another vector
    """
    all_arr = []
    for arr1_, arr in zip(arr1, ndarr2):
        if len(arr) > 0:
            [all_arr.append(arr1_) for _ in arr]

    return np.array(all_arr)


def get_all_vector_by_other_vector(ndarr1, ndarr2):
    """
    get vector as scalar based on another vector, and assign nan if that vector is empty
    """
    all_arr = []
    for arr1, arr2 in zip(ndarr1, ndarr2):
        if len(arr2) > 0:
            if len(arr1) == 0:
                arr1 = [np.nan]
            [all_arr.append(arr1[0]) for _ in arr2]

    return np.array(all_arr)


def get_max(ndarr):
    all_arr = []
    for arr in ndarr:
        if len(arr) > 0:
            all_arr.append(max(arr))

    return np.array(all_arr)


def to_new_df(data, amplifier=True):
    """
    Make dataframe for all S2s. It provides:

    - run_number: number of the run
    - event_id: event number in the run
    - event_time: when event happened in unix time in seconds
    - x: x position of event in arbitrary unit (a.u.)
    - y: y position of event in a.u.
    - s2: s2 size, PE
    - main_s2: size of main s2 for the event where the s2 is, PE
    - s2_width_50: s2 width of 50 percent area in us
    - s2_width_90: s2 width of 90 percent area in us
    - s2_rise_time: s2 rise time in us
    - s2_drop_time: s2 drop time in us
    - s1: s1 size in PE
    - s1_time: center time of main s1 in us
    - s2_time: center time of s2 in us
    - main_s2_time: center time of main s2 in us
    - s2_delay_time: how long s2 is delayed after main s2, us
    """
    event_id = get_all_scalar(data.EventID, data.S2sPeak)
    event_time = get_all_scalar(data.UnixTime, data.S2sPeak)  # s
    x = get_all_vector(data.S2sPosX)
    y = get_all_vector(data.S2sPosY)
    if not amplifier:
        amp = 1
    else:
        amp = 10

    sample_to_mu = 1 / 250

    main_s2 = get_all_vector_as_scalar(data.S2sTot) / amp  # get main s2 in the event which s2 is in
    s2 = get_all_vector(data.S2sTot) / amp  # amplifier
    s1 = get_all_vector_by_other_vector(data.S1sTot, data.S2sPeak) / amp  # amplifier

    s2_width_50 = get_all_vector(data.S2sWidth) * sample_to_mu  # us
    s2_width_90 = get_all_vector(data.S2sLowWidth) * sample_to_mu  # us
    s2_rise_time = get_all_vector(data.S2sRiseTime) * sample_to_mu  # us
    s2_drop_time = get_all_vector(data.S2sDropTime) * sample_to_mu  # us
    s1_time = get_all_vector_by_other_vector(data.S1sPeak, data.S2sPeak) * sample_to_mu # us
    s2_time = get_all_vector(data.S2sPeak) * sample_to_mu  # us
    main_s2_time = get_all_vector_as_scalar(data.S2sPeak) * sample_to_mu  # us
    s2_delay_time = s2_time - main_s2_time  # us

    df = pd.DataFrame({'event_id': event_id,
                       'event_time': event_time,
                       'x': x,
                       'y': y,
                       's2': s2,
                       'main_s2': main_s2,
                       's2_width_50': s2_width_50,
                       's2_width_90': s2_width_90,
                       's2_rise_time': s2_rise_time,
                       's2_drop_time': s2_drop_time,
                       's1': s1,
                       's1_time': s1_time,
                       's2_time': s2_time,
                       'main_s2_time': main_s2_time,
                       's2_delay_time': s2_delay_time})
    return df


def load_data(file):
    data = pd.DataFrame(root2array(file, 'T1'))
    return data

def load(input, processor='sandp_test'):
    """load data into all s2 format. Input can be either folder name or run number"""
    is_string = judge_str(input)

    if is_string:
        run_info = folders_to_file_s(input, processor)

    else:
        run_info = run_number_to_file_s(input, processor)

    data = pd.DataFrame()
    for run in tqdm(run_info, desc='load single e data'):
        data_tmp = to_new_df(load_data(run['file_location']), amplifier=run['amplifier_on'])
        data_tmp['run_number'] = run['run_number']
        data = pd.concat([data, data_tmp], ignore_index=True)

    return data