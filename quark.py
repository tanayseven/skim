#!/usr/bin/env python 3

# Quark is a module that converts unique strings to ints and vice versa
# Copyright (C) 2014  Tanay PrabhuDesai
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pickle

class Quark:
    
    def __init__(self):
        self.__int_strings__ = []
        self.__strings_int__ = {}
        self.filename = "./model/Quark.dict"
    
    def __len__(self):
        return len(self.__int_strings__)
    
    def append(self,string):
        if not isinstance(string,str):
            raise TypeError('Invalid type key \''+str(type(string))+'\'')
        if string not in self.__strings_int__:
            self.__int_strings__.append(string)
            self.__strings_int__[string] = len(self.__int_strings__)-1
        
    def __getitem__(self,key):
        result = None
        if isinstance(key,int):
            if key >= len(self):
                raise IndexError('Index out of range "'+str(key)+'"')
            elif self.__int_strings__[key] not in self.__strings_int__:
                raise KeyError('Invalid int key "'+str(key)+'"')
            else:
                result = self.__int_strings__[key]
        elif isinstance(key,str):
            if key not in self.__strings_int__:
                raise KeyError('Invalid string key "'+key+'"')
            result = self.__strings_int__[key]
        else:
            raise TypeError('Invalid type key "'+str(type(key))+'"')
        return result
    
    def __delitem__(self,key):
        if not isinstance(key,str):
            raise TypeError('Invalid type key "'+str(type(key))+'"')
        if key not in self.__strings_int__:
            raise KeyError('Invalid string key "'+key+'"')
        else:
            self.__int_strings__[self.__strings_int__[key]] = None
            del self.__strings_int__[key]

    def __contains__(self,item):
        if item in self.__strings_int__:
            return True
        else:
            return False

    def write_to_file(self):
        output_file = open(self.filename, 'wb')
        pickle.dump(self,output_file)
        output_file.close()

    def read_from_file(self):
        input_file = open(self.filename, 'rb')
        self = pickle.load(input_file)
        input_file.close()
