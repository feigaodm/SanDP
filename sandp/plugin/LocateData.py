import os
import datetime as dt
import operator
import pickle
from .. import THISDIR

class base(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def str_to_unix(string):
        """
        Convert string to unix
        """
        raise NotImplementedError

    @property
    def time_str(self):
        """
        Get time string
        :return:
        """
        raise NotImplementedError

    @property
    def time(self):
        """
        Get unix time
        """
        return self.str_to_unix(self.time_str)


class Path(base):
    @staticmethod
    def str_to_unix(string):
        unix = int(dt.datetime.strptime(string, '%Y%m%d%H%M').strftime("%s"))
        return unix

    @property
    def time_str(self):
        ret = self.name[0:12]  # hardcoded for now
        return ret

class File(base):
    @staticmethod
    def str_to_unix(string):
        unix = int(dt.datetime.strptime(string, '%Y%m%d%H%M%S').strftime("%s"))
        return unix

    @property
    def time_str(self):
        ret = self.name[7:15] + self.name[16:22]  # hardcoded for now
        return ret


class DataLocation():
    config = {
        'co57': {'data_location': os.path.join(THISDIR, 'plugin/data_location_info_co57.pkl'),
                 'base_path': '/home/nilab/10T_Two/RawData/Run21/Co57/'}
        #TODO: BKG
    }

    def __init__(self, datatype):
        self.datatype = datatype
        self.data_location = pickle.load(open(self.config[self.datatype]['data_location'], 'rb'))

    def get_location(self, event_time):
        ret_path, ret_file = None, None
        for path_name, path_info in self.data_location.items():
            if event_time > path_info['time']:
                ret_path = path_name
            else:
                path_info = self.data_location[ret_path]
                for file_name, file_time in path_info['file_info'].items():
                    if event_time > file_time:
                        ret_file = file_name
                    else:
                        break

        assert ret_file is not None, "Something wrong with path"
        assert ret_path is not None, "Something wrong with file"

        ret = os.path.join(self.config[self.datatype]['base_path'], os.path.join(ret_path, ret_file))
        return ret