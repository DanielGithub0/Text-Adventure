import os

__location__ = os.path.realpath( #this creates a call for "__location__" as the real path for [this] file
    os.path.join(os.getcwd(), os.path.dirname(__file__))) #anything called using "__location__" will have the directory of this file searched

test = open("C://Users/darkd/Documents/VS-Code/testing.txt")
print(test.read())

with open(os.path.join(__location__, "testing.txt" )) as test2:  
    print(test2.read(12))
