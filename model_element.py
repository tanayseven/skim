#!/usr/bin/env python 3

# ModelElement is an element from the model that represents a word
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

class ModelElement:
    
    MAX_NEXT = 20
    
    def __init__(self,word):
        self.word = word
        self.count = 1
        self.next = []
    
    def add_next(self,word):
        it = self.get_next_index(word)
        if it != None:
            self.next[it].count += 1
        else:
            if len(self.next) >= ModelElement.MAX_NEXT:
                self.next.pop()
            self.next.append(ModelElement(word))
            it = len(self.next)-1
        while it > 0:
            if self.next[it].count > self.next[it-1].count:
                self.next[it], self.next[it-1] = self.next[it-1], self.next[it]
            it -= 1
    
    def get_next_index(self,word):
        result = None
        for it in range(len(self.next)):
            if self.next[it].word == word:
                result = it
                break
        return result
    
    def get_next_element(self,word):
        result = None
        for element in self.next:
            if element.word == word:
                result = element
                break
        return result
    
    def get_predictions(self,num):
        predictions = []
        for element in self.next:
            predictions.append(element.word)
            num -= 1
            if num == 0:
                break
        return predictions
    
class RootElement(ModelElement):

    def __init__(self,word):
        ModelElement.__init__(self,word)
        self.age = 0
