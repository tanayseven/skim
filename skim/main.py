#!/usr/bin/env python3
from skim.model import Model

# Contains the Main methos for the skim to run
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


def main():
    print("""     
    skim  Copyright (C) 2014  Tanay PrabhuDesai
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details. \n\n""")
    mdl = Model(20,5)
    print("Model?(y/n):")
    choice = input()
    if choice != 'n' and choice != 'N':
        mdl.load_map()    
        mdl.load_model_base()
        text = open('./raw_input_1/sherlock.txt','r')
        strings = text.readlines()
        text.close()
        count = 1
        for string in strings:
            mdl.insert_string(string)
            print("Inserted line: "+str(count))
            count += 1
        mdl.save_map()
    print("Start typing: ")
    while True:
        inp = input()
        if inp == "":
            break
        print("Predictions:")
        print(mdl.search_string(inp, 5))


if __name__ == "__main__":
    main()