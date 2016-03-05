from __future__ import division
import sys

"""
Written by Leo Selker

A script which takes an input representing a honeycomb of letters and an 
input representing a "dictionary" of words, and return the words from that 
dictionary which are found in the honeycomb

Usage: python main.py <honeycombFileName> <dictionaryFileName>"""

"""Import data and set it up"""
files=sys.argv
(honeycombFile,dictionaryFile)=(open(files[1]),open(files[2]))
# transfer the dictionary and honeycomb to lists
dictionary=[]
for line in dictionaryFile:
    # remove newline characters
    if line[-1]=='\n': line=line[:-1]
    dictionary.append(list(line))
    
#read the first line
nLayers=int(honeycombFile.readline())
honeycomb=[]

for line in honeycombFile:
    # remove newline characters
    if line[-1]=='\n': line=line[:-1]
    honeycomb.append(list(line))



# The stack which will keep track of states to check. A queue would have worked
# just as well but I felt like going depth-first today. Either is much more 
# efficient space-wise and time-wise than a recursive algorithm.
theStack=[]
#Words actually found
foundList=[]

def connected((e,r)):
    """returns the spots a square connects to"""
   
    # Deal with the middle case so we don't divide by zero
    if r==0: return [(1,1),(2,1),(3,1),(4,1),(5,1),(0,1)]
    # If the input is impossible, return nothing to prune the branch (shouldn't
    # happen)
    if e>=6*r: return []
    connected=[]
    mult=e//r
    rem=e % r
    #Going sideways
    toAdd=((6*r-1,r) if e==0 else (e-1,r))
    connected.append(toAdd)
    toAdd=((0,r) if e==6*r-1 else (e+1,r))
    connected.append(toAdd)
    #Going inward
    toAdd=( (0,r-1)if mult==5 and rem==r-1 else (mult*(r-1)+rem,r-1) )
    connected.append(toAdd)
    if rem!=0:
        connected.append((mult*(r-1)+rem-1,r-1))

    #Going outward
    if r<nLayers-1:
        connected.append((mult*(r+1)+rem,r+1))
        connected.append((mult*(r+1)+rem+1,r+1))
        if rem==0: # only case where negatives could result
            if mult>0: connected.append( (mult*(r+1)-1,r+1))
            else: connected.append( (6*(r+1)-1,r+1))
            
    return connected
    
def compare(theInput,dictionary):
    """compares an input string to the dictionary. Returns 0 if it doesn't 
    match the first letters of any word, 1 if it does, 2 if it matches a word 
    exactly"""
    n=len(theInput)
    ret=0
    for word in dictionary:
        if theInput==word: return 2
        if theInput==word[:n]: ret=1
    return ret

def step((e,r),soFar,used):
    """A step in the process. Note that 'used' is a set object """
    
    # If it's a word in the dictionary, add it unless it's already in the list
    if compare(soFar, dictionary)==2:
        if soFar not in foundList:
            foundList.append(soFar)
    # If it's part of a word, keep going
    if compare(soFar, dictionary)>0:
        toPush=connected((e,r))
        
        for (eNew,rNew) in toPush:
            if (eNew,rNew) not in used:
                newUsed=used.copy()
                newUsed.add((eNew,rNew))
                theStack.append( ((eNew,rNew),soFar+[honeycomb[rNew][eNew]],newUsed) )
    
    # If it's not part of a word, to keep going would waste time.
    if compare(soFar, dictionary)==0:
        pass
    
def iterate():
    """runs the algorithm's main loop"""
    # States are of the form (coordinates, word so far, used spots)
    # Load the initial states into the stack
    global theStack
    for r,layer in enumerate(honeycomb):
        for e,el in enumerate(layer):
            theStack.append( ((e,r), [el],set([(e,r)])) )
    
    while (len(theStack) != 0):
        #pop the next run
        (e,r),soFar,used=theStack[-1]
        theStack=theStack[:-1]
        #run it!
        step((e,r),soFar,used)


# Run the algorithm 
iterate()
foundList=sorted(foundList)
print foundList