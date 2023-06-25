import sys
import os

import logging, logging.config
import json
from datetime import datetime

class Logger():

    def __init__(self, configfile=None, loggername=None, logpath=None, logfile=None, **kwargs):
        self.__logger = None
        self.__logger_config = None
        self.__loggername = "__main__"
        self.config(configfile=configfile, loggername=loggername, logpath=logpath, logfile=logfile, **kwargs)
    
    def config(self, configfile=None, loggername=None, logpath=None, logfile=None, **kwargs):
        self.__configfile = configfile
        self.__current_file_path = None
        self.__logfile = logfile

        if configfile is not None:
            self.__logger_config = self.__read_configfile(configfile=configfile)

            if logpath is not None:
                if logfile is None:
                    self.__logfile = self.__get_dict_value_by_key(key="['handlers']['file']['filename']")
                self.__current_file_path = self.__create_log_dir(logpath)
                self.__set_logfile(logpath=self.__current_file_path, logfile=self.__logfile)

            self.__set_config(loggerdictconfig=self.__logger_config)

        if loggername is not None:
            self.set_logger(loggername=loggername)
                
        return self
    
    def get_logger(self):
        return self.__logger
    
    def set_logger(self, loggername=None):
        if loggername is not None:
            self.__loggername = loggername
        self.__logger = logging.getLogger(self.__loggername)
        self.__logger.debug("Logger created with following params: [configfile: '%s' | logpath: '%s' | logfile: '%s']", self.__configfile, self.__current_file_path, self.__logfile)
        return self
    
    ##################################################################################################################################
    
    def __find_path_of_occurrence(self, nested_dict: dict, search_path: str):
        def __convert_dictkeys_to_list(dict_keys: str):
            key_list = dict_keys.strip("[]").split("][")
            key_list = [int(item) if item.isdecimal() else float(item) if item.replace('.', '', 1).isdecimal() else item.replace('"', '').replace("'", "") for item in key_list]
            return key_list

        def __convert_keylist_to_dictstr(list_keys: list):
            key_dictstr = ""
            for item in list_keys:
                key = int(item) if isinstance(item, int) else float(item) if isinstance(item, float) else "'" + item + "'"
                key_dictstr = key_dictstr + "[" + str(key) + "]"
            return key_dictstr
        
        def __recursive_tree_search(nested_dict: dict, pattern: list, result_list=[], current_path=[]):
            for [key, value] in nested_dict.items(): 
                if key == pattern[0]:
                    current_result = __check_occurrence(nested_dict=value, pattern=pattern, index=1, result_path=current_path + [key])
                    if current_result != None:
                        result_list.append(current_result)
                
                if isinstance(value, dict):
                    __recursive_tree_search(nested_dict=value, pattern=pattern, result_list=result_list, current_path=current_path + [key])
            return result_list
        
        def __check_occurrence(nested_dict: dict, pattern: list, index=0, result_path=[]):
            if index > len(pattern) - 1:
                return result_path

            if isinstance(nested_dict, dict) and pattern[index] in nested_dict:
                result_path.append(list(nested_dict.keys())[0])
                return __check_occurrence(nested_dict=nested_dict[pattern[index]], pattern=pattern, index=index+1, result_path=result_path)
            else:
                return None

        search_path_list = __convert_dictkeys_to_list(search_path)
        result_list_list = __recursive_tree_search(nested_dict, search_path_list)
        result_str_list = []
        for path in result_list_list:
            result_str_list.append(__convert_keylist_to_dictstr(path))
        return result_str_list

    def __get_dict_value_by_key(self, key):
        #TODO: search for key='filename' in nested dict and get the value
        #path_list = self.__find_path_of_occurrence(self.__logger_config, key)
        #exec("result = self._Logger__logger_config%s" % path_list[0])

        #Workaround:
        if key == "['handlers']['file']['filename']":
            result = self.__logger_config['handlers']['file']['filename']
        else:
            raise Exception("Not implemented ('key') yet for '__get_dict_value_by_key()'")
        
        return result
    
    def __set_dict_value_by_key(self, key, new_value):
        #TODO: search for key='filename' in nested dict and replace the value
        #path_list = self.__find_path_of_occurrence(self.__logger_config, key)
        #exec("result = self._Logger__logger_config%s = %s" % (path_list[0], new_value))

        #Workaround:
        if key == "['handlers']['file']['filename']":
            self.__logger_config['handlers']['file']['filename'] = new_value
        else:
            raise Exception("Not implemented ('key') yet for '__set_dict_value_by_key()'")

    def __read_configfile(self, configfile):
        with open(configfile) as json_file:
            logger_config = json.load(json_file)
        return logger_config

    def __set_logfile(self, logpath, logfile):
        if logfile is not None and logfile != "":
            if logpath is None or logpath == "":
                logpath = self.__current_file_path
            value = logpath + logfile
            self.__set_dict_value_by_key(key="['handlers']['file']['filename']", new_value=value)

    def __set_config(self, loggerdictconfig):
        logging.config.dictConfig(loggerdictconfig)

    def __create_log_dir(self, path):
        if (self.__current_file_path is None) and (path is not None):
            current_datetimestamp = self.__get_current_datetimestamp()
            if not os.path.exists(path + current_datetimestamp):
                os.makedirs(path + current_datetimestamp)
            self.__current_file_path = path + current_datetimestamp + "/"

            value = self.__current_file_path + self.__get_dict_value_by_key(key="['handlers']['file']['filename']")
            self.__set_dict_value_by_key(key="['handlers']['file']['filename']", new_value=value)
        return self.__current_file_path
    
    def __get_current_datetimestamp(self):
        current_datetimestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return current_datetimestamp