#!/usr/bin/env python3

# Model is the main module that stores the complete n_grams_model
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


from quark import Quark
from model_element import ModelElement, RootElement

import shelve
import pickle
import os

class Model:
    
    MAX_AGE = 10
    
    def __init__(self,max_roots,num_grams):
        self.max_roots = max_roots
        self.roots = []
        self.map = Quark()
        self.map_filename = "./model/mapdict"
        self.num_grams = num_grams
        self.model_base = None
        self.oldest_root = None
        self.model_base_filename = "./model/model"
        
    def load_map(self):
        result = True
        if os.path.exists(self.map_filename):
            input_file = open(self.map_filename, 'rb')
            self.map = pickle.load(input_file)
            input_file.close()
        else:
            result = False
        return result

    def load_model_base(self):
        self.model_base = shelve.open(self.model_base_filename)

    def get_string_tokens(self,int_tokens):
        str_tokens = []
        for int_token in int_tokens:
            str_tokens.append(self.map[int_token])
        return str_tokens
    
    def get_int_tokens(self,str_tokens):
        int_tokens = []
        for str_token in str_tokens:
            if str_token not in self.map:
                self.map.append(str_token)
            int_tokens.append(self.map[str_token])
        return int_tokens
    
    def split_string_into_n_grams(self,string):
        str_tokens = string.split()
        n_gram_strings = []
        for it in range(len(str_tokens)-self.num_grams+1):
            string = ' '.join(str_tokens[it:it+self.num_grams])
            n_gram_strings.append(string)
        return n_gram_strings

    def add_root(self,word,oldest_index):
        oldest_root = self.roots[oldest_index]
        if len(self.roots) >= self.max_roots:
            self.model_base[self.map[oldest_root.word]] = oldest_root
            del self.roots[oldest_index]
        self.roots.append(self.model_base[self.map[word]])

    def load_from_db(self,word):
        try:
            self.model_base[self.map[word]]
        except KeyError:
            pass

    def get_root(self,word,new_node=True):
        root = None
        if len(self.roots) > 0:
            oldest_index, oldest_root = 0, self.roots[0]
            for index, r in enumerate(self.roots):
                r.age += 1
                if r.word == word:
                    root = r
                    r.age = 0
                if r.age > oldest_root.age:
                    oldest_index, oldest_root = index, r
            if root == None:
                try:
                    if self.map[word] != None and self.model_base != None and new_node:
                        self.add_root(word, oldest_index)
                    elif self.model_base != None :
                        self.add_root(self.model_base[self.map[word]],oldest_root)
                        root = self.get_root(word,False)
                except KeyError:
                    return
        return root

    def insert_string(self,string):
        str_tokens_arr = self.split_string_into_n_grams(string)
        int_tokens_arr = []
        for str_token in str_tokens_arr:
            int_tokens_arr.append(self.get_int_tokens(str_token.split()))
        str_tokens_arr = None
        string = None
        for int_tokens in int_tokens_arr:
            temp_element = self.get_root(int_tokens[0])
            if temp_element == None:
                self.roots.append(RootElement(int_tokens[0]))
                temp_element = self.get_root(int_tokens[0])
            for token in int_tokens[1:]:
                temp_element.add_next(token)
                temp_element = temp_element.get_next_element(token)

    def search_string(self,string,num_preds):
        predictions = []
        int_tokens = self.get_int_tokens(string.split())
        temp_token = self.get_root(int_tokens[0], False)
        if temp_token == None:
            return predictions
        for token in int_tokens[1:]: 
            temp_token = temp_token.get_next_element(token)
            if temp_token == None:
                return predictions
        if temp_token != None:
            for element in temp_token.next:
                if num_preds == 0:
                    break
                predictions.append(element.word)
                num_preds -= 1
        predictions = self.get_string_tokens(predictions)
        return predictions

    def save_map(self):
        self.map.write_to_file()