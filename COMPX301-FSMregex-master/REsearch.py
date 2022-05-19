import fileinput
import string
import sys
# COMPX301-20A Taukoriri Nooti 1322671

class Deque:

    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        return self.items == []
        
    def addFirst(self, item):
        
        self.items.insert(0, item)
        
    def addLast(self, item):
        length = len(self.items)
        self.items.insert(length, item)
     
    def dequePop(self):
        return self.items.pop(0)
   
    def removeLast(self):
        return self.items.pop()
    
    def displayDeque(self):
        print(self.items)
            
    def dequeFirst(self):
        i = self.items[0]
        return i
        
    def dequeClear(self):
        self.items = []
        
    def dequeSize(self):
        return len(self.items)
def main():
    
    matchfound = False
    loop = 1
    line = ""
    chr = []
    n1 = []
    n2 = []
    #deque object
    deque = Deque()
    #where we began our search
    m = ""
    #where to see 
    p = ""


    while loop >= 1:
        a = sys.stdin.readline().split()

        alength = len(a)
        chr.append(a[0])
        n1.append(int(a[1]))
        n2.append(int(a[2]))
        loop = int(a[1])
        
    try:
        nextstate1 = n1[0]
        nextstate2 = n2[0]    
       

        for line in fileinput.input():
            #length takes the length of the line
            #for each character in "line"
            #scan
            deque.addLast("x")
            for word in line.split():
                #set our pointer and m to the start of the pattern
                if matchfound:
                    matchfound = False
                    break
                wordlen = len(word)
                
                for h in range(wordlen):
                    if matchfound:
                        print("word", word)
                        break
                    counter = h
                    counter += 1
                    if counter == wordlen:
                        print("No match found: out of input")
                        deque.dequeClear()
                        break
                    #advance m
                    m = word[h]
                    p = m
                    #push start state
                    currentstate = 0
                    deque.addFirst(n1[currentstate])
                    
                    j = h
                    for i in range(wordlen):
                        
                        p = word[j]


                        currentstate = deque.dequeFirst()
                        #match is not found
                        if currentstate == "x":
                            print("no match found:only SCAN is left in Deque")
                            break
                        currentstate = deque.dequeFirst()
                        #match is found
                        if n1[currentstate] < 0:
                            print("match found")
                            matchfound = True
                            deque.dequeClear()
                            break
                        index = int(currentstate)
                        b1 = n1[index]
                        b2 = n2[index]                   
                        if (b1 == b2):

                            if p == chr[currentstate]:
                                #pop current state
                                deque.dequePop()
                                #add nextstate
                                deque.addLast(n1[currentstate])
                                #pop scan
                                deque.dequePop()
                                j += 1

                                if not (deque.isEmpty()):
                                    #pop scan and add to the bottom
                                    #deque.dequePop()
                                    deque.addLast("x")
                                    #advance the pointer
                                    #currentstate = deque.dequeFirst()
                                else:
                                    print("failure")
                            else:

                                deque.dequePop()
                        #Branching Machine
                        else: 

                            deque.dequePop()

                            #add branching machine to stack
                            deque.addFirst(n1[currentstate])
                            deque.addFirst(n2[currentstate])
                            
                            currentstate = deque.dequeFirst()
                            if p == chr[currentstate]: 
                                #add nextstate
                                deque.addLast(n1[currentstate])
                                #pop current state
                                deque.dequePop()
                                deque.dequePop()
                                #pop scan
                                deque.dequePop()
                                j += 1
                                if not (deque.isEmpty()):
                                    #pop scan and add to the bottom
                                    #deque.dequePop()
                                    deque.addLast("x")
                                    #advance the pointer
                                    #currentstate = deque.dequeFirst()                                
                                else:
                                    print("failure")
                            else:
                                deque.dequePop()
                                currentstate = deque.dequeFirst()
                                if p == chr[currentstate]:
                                    #add nextstate
                                    deque.addLast(n2[currentstate])
                                    #pop current state
                                    deque.dequePop()
                                    #pop scan and add to the bottom
                                    deque.dequePop()
                                    j += 1

                                    if not (deque.isEmpty()):

                                        deque.addLast("x")
                                        #advance the pointer
                                        currentstate = deque.dequeFirst()                                
                                    else:
                                        print("failure")      
                                else:

                                    
                                    deque.dequePop()
            print("\n")
                

    except Exception as e:
        print(e)

    
main()
