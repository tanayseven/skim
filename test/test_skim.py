#!/usr/bin/env python 3

# Test script to test all the skim modules
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

import unittest

from skim.quark import Quark
from skim.model_element import ModelElement, RootElement
from skim.model import Model


class TestQuarkFunctions(unittest.TestCase):

    def setUp(self):
        self.test_quark = Quark()

    def test_Quark_Insertion(self):
        st = "this is a test string".split()
        for i in st:
            self.test_quark.append(i)
        for i, s in enumerate(st):
            self.assertEqual(self.test_quark[s], i, "Quark should return an int for the string that matches")
        for i, s in enumerate(st):
            self.assertEqual(self.test_quark[i], s, "Quark should return an string for the int that matches")

    def test_Quark_Deletion_And_Exceptions(self):
        st = "this is a test string".split()
        for i in st:
            self.test_quark.append(i)  
        del self.test_quark['a']
        self.assertRaises(KeyError, self.test_quark.__getitem__,'a')
        self.assertRaises(KeyError, self.test_quark.__getitem__,2)

    def test_Quark_NotFound_Exceptions(self):
        self.assertRaises(IndexError, self.test_quark.__getitem__,10)

class TestModelElement(unittest.TestCase):

    def setUp(self):
        self.test_element = ModelElement(0)
        self.test_element.add_next(0)
        self.test_element.add_next(1)
        self.test_element.add_next(2)
        self.test_element.add_next(0)
        self.test_element.add_next(2)
        self.test_element.add_next(0)
        
    def test_Initialization(self):
        self.assertEqual(self.test_element.word, 0, "The initialized word should be zero")
        self.assertEqual(self.test_element.count, 1, "The initialized count should be one")
        self.assertEqual(len(self.test_element.next), 3, "The initialized next should be empty")
        
    def test_Add_Next(self):
        self.assertEqual(self.test_element.next[0].word,0,"0 has highest frequency so should be at index 0")
        self.assertEqual(self.test_element.next[1].word,2,"2 has 2nd highest frequency so should be at index 1")
        self.assertEqual(self.test_element.next[2].word,1,"1 has least highest frequency so should be at index 2")

    def test_Get_Next_Index(self):
        self.assertEqual(self.test_element.get_next_index(0),0,"0 should have index 0")
        self.assertEqual(self.test_element.get_next_index(2),1,"2 should have index 1")
        self.assertEqual(self.test_element.get_next_index(1),2,"1 should have index 2")
        self.assertEqual(self.test_element.get_next_index(3),None,"3 should return None")

    def test_Get_Next_Element(self):
        self.assertEqual(self.test_element.get_next_element(0).word,0,"0 should be found")
        self.assertEqual(self.test_element.get_next_element(2).word,2,"2 should be found")
        self.assertEqual(self.test_element.get_next_element(1).word,1,"1 should be found")
        self.assertEqual(self.test_element.get_next_element(3),None,"3 should return None")
        
    def test_Get_Predictions(self):
        test_preds = self.test_element.get_predictions(10)
        actual_preds = [0,2,1]
        result = True
        for test_pred,actual_pred in zip(test_preds,actual_preds):
            if test_pred != actual_pred:
                result = False
                break
        self.assertEqual(result, True, "The two predictions arrays should be the same")
                
class TestRootElement(unittest.TestCase):
    
    def setUp(self):
        self.test_element = RootElement(0)
        
    def test_Initialization(self):
        self.assertEqual(self.test_element.word, 0)
        self.assertEqual(self.test_element.count, 1)
        self.assertEqual(len(self.test_element.next), 0)
        self.assertEqual(self.test_element.age, 0)

class TestModel(unittest.TestCase):

    def setUp(self):
        self.test_model = Model(20,5)

    def test_Initialization(self):
        self.assertEqual(self.test_model.max_roots,20)
        self.assertEqual(self.test_model.num_grams,5)

    #Test both the functions in one test case
    def test_Get_String_Int_Tokens(self):
        string = "Now , fair Hippolyta , our nuptial hour"
        int_tokens = self.test_model.get_int_tokens(string.split())
        str_tokens = self.test_model.get_string_tokens(int_tokens)
        result_str = ' '.join(str_tokens)
        self.assertEqual(string, result_str, "get_string_tokens() and get_int_tokens() should give the same mapped values")

    def test_Split_String_Into_NGrams(self):
        string = "Now , fair Hippolyta , our nuptial hour"
        actual_tokens = ['Now , fair Hippolyta ,', ', fair Hippolyta , our', 'fair Hippolyta , our nuptial', 'Hippolyta , our nuptial hour']
        test_tokens = self.test_model.split_string_into_n_grams(string)
        result = True
        for actual,test in zip(actual_tokens,test_tokens):
            if actual != test:
                result = False
                break
        self.assertTrue(result, "The actual tokens should match the test tokens")

    def test_Get_Root(self):
        self.test_model.roots.append(RootElement(0))
        self.test_model.roots.append(RootElement(1))
        self.test_model.roots.append(RootElement(2))
        root = []
        root.append(self.test_model.get_root(0))
        root.append(self.test_model.get_root(1))
        root.append(self.test_model.get_root(2))
        self.assertNotEqual(root[0], None, "Root 0 should be found")
        self.assertNotEqual(root[1], None, "Root 1 should be found")
        self.assertNotEqual(root[2], None, "Root 2 should be found")
        self.assertEqual(root[0].word, 0, "Root at 0 should be 0")
        self.assertEqual(root[1].word, 1, "Root at 1 should be 1")
        self.assertEqual(root[2].word, 2, "Root at 2 should be 2")

    def test_Insert_String(self):
        string = "What goes around comes around . He knows nothing ."
        self.test_model.insert_string(string)
        self.assertEqual(self.test_model.roots[0].next[0].next[0].next[0].next[0].word, self.test_model.map['around'],"Around should be the word after 'What goes around comes'")
        self.assertEqual(self.test_model.roots[1].next[0].next[0].next[0].next[0].word, self.test_model.map['.'],". should be the word after 'goes around comes around'")

    def test_SearchString(self):
        string = "the cat ate the rat the dog chased the cat this is very fast system that was very good thing this is a very boring place"
        self.test_model.insert_string(string)
        preds = self.test_model.search_string("the", 3)
        self.assertEqual(preds,['cat', 'rat', 'dog'],"The Predicitons should be ['cat', 'rat', 'dog']")
        preds = self.test_model.search_string("the cat", 3)
        self.assertEqual(preds, ['ate', 'this'], "The Predicitons should be ['ate', 'this']")
        preds = self.test_model.search_string("the rat the dog", 3)
        self.assertEqual(preds, ['chased'], "The Predicitons should be ['chased']")
        preds = self.test_model.search_string("this is a stupid", 3)
        self.assertEqual(preds, [], "The Predicitons should be [] (empty)")
        preds = self.test_model.search_string('is a very', 5)
        print(preds)

    def test_Shelve(self):
        pass

if __name__ == "__main__":
    unittest.main()
