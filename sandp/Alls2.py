"""
For single electron analysis
"""
import numpy as np
import pandas as pd
from root_numpy import root2array
import os
import matplotlib.pyplot as plt
from multihist import Histdd, Hist1d


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
    Make dataframe with all S2s
    """
    event_id = get_all_scalar(data.EventID, data.S2sPeak)
    event_time = get_all_scalar(data.UnixTime, data.S2sPeak)  # s
    x = get_all_vector(data.S2sPosX)
    y = get_all_vector(data.S2sPosY)
    if not amplifier:
        amp = 1
    else:
        amp = 10

    main_s2 = get_all_vector_as_scalar(data.S2sTot) / amp  # get main s2 in the event which s2 is in
    s2 = get_all_vector(data.S2sTot) / amp  # amplifier
    s1 = get_all_vector_by_other_vector(data.S1sTot, data.S2sPeak) / amp  # amplifier

    s2_width_50 = get_all_vector(data.S2sWidth) / 250  # us
    s2_width_90 = get_all_vector(data.S2sLowWidth) / 250  # us
    s2_rise_time = get_all_vector(data.S2sRiseTime) / 250  # us
    s2_drop_time = get_all_vector(data.S2sDropTime) / 250  # us
    s1_time = get_all_vector_by_other_vector(data.S1sPeak, data.S2sPeak) / 250  # us
    s2_time = get_all_vector(data.S2sPeak) / 250  # us
    main_s2_time = get_all_vector_as_scalar(data.S2sPeak) / 250  # us
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


def get_file(path):
    if isinstance(path, str):
        files = os.listdir(path)
        full_path_s = [os.path.join(path, file) for file in files if '.root' in file]
    elif isinstance(path, list):
        full_path_s_tmp = []
        for path_ in path:
            full_path_s_tmp.append(get_file(path_))

        full_path_s = [element for sub_path in full_path_s_tmp for element in sub_path]

    return full_path_s


def get_path(basic_path, exclude_paths=False):
    paths = os.listdir(basic_path)
    path_s = [os.path.join(basic_path, path) for path in paths if '2019' in path]
    if exclude_paths:
        path_s = [path for path in path_s if path not in exclude_paths]
    return path_s


def load_data(file):
    data = pd.DataFrame(root2array(file, 'T1'))
    return data


def gaus(x, *par):
    a, mu, sig = par
    return a * np.exp(-0.5 * (x - mu) ** 2 / sig ** 2)


def multi_gaus(x, *par):
    a1, a2, a3, a4, mu, sig = par
    gaus1 = gaus(x, a1, mu, sig)
    gaus2 = gaus(x, a2, 2 * mu, np.sqrt(2) * sig)
    gaus3 = gaus(x, a3, 3 * mu, np.sqrt(3) * sig)
    gaus4 = gaus(x, a4, 4 * mu, np.sqrt(4) * sig)
    # gaus5 = gaus(x, a5, 5*mu, np.sqrt(5)*sig)
    return gaus1 + gaus2 + gaus3 + gaus4


def eff(x, *par):
    p0, p1 = par
    return 1 / (np.exp(-(x - p0) / p1) + 1)


def singlefit(x, *par):
    p0, p1, a1, a2, a3, a4, mu, sig = par
    return eff(x, p0, p1) * multi_gaus(x, a1, a2, a3, a4, mu, sig)


def test_single(df, title=False):
    fig = plt.figure(figsize=(9, 4))
    fig.patch.set_color('white')
    plt.subplot(121)
    hist_new = Hist1d(df.s2, bins=np.linspace(0, 25, 100))
    hist_new.plot(label='new processor (update 2)')
    plt.xlabel('S2 [PE]')
    plt.ylabel('Counts / bin')

    plt.subplot(122)
    hist = Hist1d(df.s2_delay_time, bins=np.linspace(0, 80, 100))
    hist.plot()
    plt.yscale('log')
    plt.xlabel('Delay Time from Main S2 [$\mu s$]')
    plt.ylabel('Counts / bin')
    if title:
        plt.suptitle(title)
    plt.show()