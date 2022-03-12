#Real time simulation of 3 CPU planning algorithms

from cgitb import text
from json.encoder import INFINITY
from random import randint
import subprocess
import sys

from art import *


# installation of necesary python libraries

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
    
install('art==5.4')
#CONSTANT DECLARATION =========================================
MAIN = True
OUTPUT = [0,-1,[]]
PSPARAMS = []
FULLOUTPUT = []

#AUXILIARY FUNCTIONS:

def isempty(list):
    if len(list) == 0:
        return True
    return False

def find(elem, list):
    for i,e in enumerate(list):
        if e == elem:
            return i

def findMaxti(ps_list):
    max = 0
    for i in ps_list:
        if i.ti > max:
            max = i.ti
    return max

def createPs(count, min_t, max_t, min_ti_interval, max_ti_interval): #Auxiliary Function to generate Processes from a set of parameters
    output = []
    last_ti = 0
    for i in range(count):
        last_ti += randint(min_ti_interval,max_ti_interval)
        output.append(Process(randint(min_t,max_t),last_ti,"P" + str(i)))

    return output

def setParams(history,n):  # Auxiliary Functions to extract the generation parameters from a given entry in the Execution History

    last_ps = history[n]
    if not isempty(last_ps.params):
        ps_count = last_ps.params[0]
        min_t = last_ps.params[1]
        max_t = last_ps.params[2]
        min_ti_interval = last_ps.params[3]
        max_ti_interval = last_ps.params[4]

        return [ps_count, min_t, max_t, min_ti_interval, max_ti_interval]


def tableFormatter(ps_list): #Formatter for the the first table, displaying Process ID, Process Duration and Process Start Time
    print()

    line = "|ID |t |ti|"
    spacer = "|"
    big_spacer = " |"
    print(line)
    for e in range(len(ps_list)):
        line = "|"
        line += str(ps_list[e].id)
        if e < 10:
            line += big_spacer
        else:
            line += spacer
        line += str(ps_list[e].t)
        if ps_list[e].t > 9 :
            line += spacer
        else:
            line += big_spacer
        line += str(ps_list[e].ti)
        if ps_list[e].ti < 10:
            line += big_spacer
        else:
            line += spacer
        print(line)   
    print()


#INPUT FUNCTIONS ==========================================================================

def check_input(a, list, error): #Error Handling
    b = True
    while b == True:
        if a in list:
            b = False
            return a
           
        else:
            print("ERROR:")
            print(error)
            a = input()

def OriginInput(): # Main menu Input gathering Function
    print()
    print("|1|: Run Algorithm")
    print("|2|: History")
    print("|3|: Rerun Last ")
    print("|4|: Exit")
    b = True
    return check_input(input(),["1","2","3","4"],"porfavor seleccione una opcion valida")



def takeSpecificInputs(): #Input gathering of Specific Process Parameters
    print("Numero de procesos:")
    ps_list = []
    ps_count = check_input(input(),[str(i) for i in range(1,15)],"el numero de procesos debe estar entre 1 y 15")
    for i in range(int(ps_count)):
        id = f"P{i}"
        print(f"P{i} duracion:")
        t = int(input())
        print(f"P{i} momento de inicio:")
        ti = int(input())
        ps_list.append(Process(t,ti,id))
        t = 0
        ti = 0
        id = ""
    return ps_list


def takeInputs():   #Input gathering of Generated Process Parameters
    art = text2art("RUN   ALGORITHM")
    print(art)
    print("Numero de procesos:")
    ps_count = check_input(input(),[str(i) for i in range(1,15)],"el numero de procesos debe estar entre 1 y 15")

    print("duracion minima de cada proceso:")
    min_t = check_input(input(),[str(i) for i in range(1,1000000)],"un proceso debe durar 1 ciclo como minimo")
    print("duracion maxima de cada proceso:")
    max_t = check_input(input(),[str(i) for i in range(int(min_t),1000000)],"la duracion maxima debe ser mayor que la minima")
    print("intervalo minimo entre inicio de procesos:")
    min_ti_interval = check_input(input(),[str(i) for i in range(0,1000000)],"el intervalo minimo debe ser positivo")
    print("intervalo maximo entre inicio de procesos:")
    max_ti_interval = check_input(input(),[str(i) for i in range(int(min_ti_interval),1000000)],"el maximo intervalo debe ser mayor que el minimo")

    
    return  [ps_count, min_t, max_t, min_ti_interval, max_ti_interval]


def select_algorithm(ps_list): #input gathering for algorithm selection

    art = text2art("SELECT   AN   ALGORITHM")

    print(art)
    print("1: RoundRobin")
    print("2: FCFS")
    print("3: SJF")
    alg = input()

    if alg == "1":
        print("quantum:")
        q = input()
        return RoundRobin(ps_list,int(q))
    if alg == "2":
        return(FCFS(ps_list))
    if alg == "3":
        return SJF(ps_list)

def input_mode():
    print("select input mode:")
    print("1: Specific")
    print("2: generated")
    return check_input(input(),["1","2"], "porfavor introduce una opcion valida")
#CLASS DEFINITION=================================

class bcolors:          #necesary for coloured output
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SJF:              #SHORTER JOB FIRST ALGORITHM
    def __init__(self, ps_list):
        self.ps_list = ps_list
        self.active_p = None
        self.pending_p = []
        self.t = -1

    def run(self):
        
        for i, ps in enumerate(self.ps_list): #iterate through the ps list, and append the active processes to the pending list
            if ps.ti-1 == self.t:
                self.pending_p.append(ps)

        
        if self.active_p == None: # check for empty active process, if true find shorter pending process and activate
            if not isempty(self.pending_p):
                min_t = 10000
                min_ps_index = 0
                for i,ps in enumerate(self.pending_p):
                    if ps != None:
                        if ps.t < min_t:
                            self.active_p = ps
                            min_ps_index = i
                            min_t = ps.t
                del self.pending_p[min_ps_index]

    
     
        if self.active_p != None:  # step the active process, check if done and activate shorter pending process 
            if(self.active_p.step() == False):
                    self.active_p = None
                    if not isempty(self.pending_p):
                        min_t = 10000
                        min_ps_index = 0
                        for i,ps in enumerate(self.pending_p):
                            if ps != None:
                                if ps.t < min_t:
                                    self.active_p = ps
                                    min_ps_index = i
                                    min_t = ps.t
                        del self.pending_p[min_ps_index]
                        self.active_p.step()
                
        self.t  += 1

        #VOLCADO A CONSTANTE OUTPUT
        OUTPUT[0] = self.t
        OUTPUT[1] = self.active_p
        OUTPUT[2] = self.pending_p

class FCFS:         #FIRST COME FIRST SERVED ALGORITHM
    def __init__(self, ps_list):
        self.ps_list = ps_list
        self.active_p = None
        self.pending_p = []
        self.t = -1

    def run(self):
        
        for i, ps in enumerate(self.ps_list):   #iterate through the ps list, and append the active processes to the pending list
            if ps.ti-1 == self.t:
                self.pending_p.append(ps)

        
        if self.active_p == None:   # check for empty active process, if true activate next pending process
            if not isempty(self.pending_p):
                self.active_p = self.pending_p[0]
                del self.pending_p[0]
    
         
        else:
            if(self.active_p.step() == False): #step the active process, check if done and activate next pending process
                    self.active_p = None
                    if not isempty(self.pending_p):
                        self.active_p = self.pending_p[0]
                        del self.pending_p[0]
                        self.active_p.step()

            
        self.t  += 1

        #VOLCADO A CONSTANTE OUTPUT
        OUTPUT[0] = self.t
        OUTPUT[1] = self.active_p
        OUTPUT[2] = self.pending_p    



class RoundRobin:   #ROUND ROBIN ALGORITHM
    def __init__(self, ps_list, q):
        self.ps_list = ps_list
        self.q = q
        self.active_p = None
        self.pending_p = []
        self.t = -1
        self.rq = q

    def run(self):
        
        for i, ps in enumerate(self.ps_list):   #iterate through the ps list, and append the active processes to the pending list
            if ps.ti-1 == self.t:
                self.pending_p.append(ps)

        
        if self.active_p == None:   # check for empty active process, if true activate next pending process
            if not isempty(self.pending_p):
                self.active_p = self.pending_p[0]
                del self.pending_p[0]
    
        if self.active_p != None:

            if self.rq == 0:            #check if quantum has run out, if so, stop active process apeend it to the pending list, and start the next pending process
                if not isempty(self.pending_p):
                    if self.active_p.t != 0:
                        self.pending_p.append(self.active_p)     
                    self.active_p = self.pending_p[0]
                    del self.pending_p[0]
                    self.rq = self.q

            if(self.active_p.step() == False):  #step the active process, check if done and activate next pending process, and reset quantum
                    self.active_p = None
                    if not isempty(self.pending_p):
                        self.active_p = self.pending_p[0]
                        del self.pending_p[0]
                        self.active_p.step()
                    self.rq = self.q

            
                        
            self.rq -= 1 
        self.t  += 1

        #VOLCADO A CONSTANTE OUTPUT
        OUTPUT[0] = self.t
        OUTPUT[1] = self.active_p
        OUTPUT[2] = self.pending_p    


class OutputFormatter:  #FORMATTER TO DISPLAY EACH LINE OF THE OUTPUT TABLE

    def __init__(self, ps_list):            
        self.ps_list = ps_list
        self.ID_list = [ps.id for ps in ps_list]
        self.ID_list_line = "|"
        self.pending_ID_list = []

        #definition strings representing table cells for active, inactive and pending status.
        
        self.active   = f"{bcolors.PINK}XXXXX{bcolors.ENDC}"
        self.inactive = "_____"
        self.pending  = f"{bcolors.YELLOW}/////{bcolors.ENDC}"
        self.line = "|"


    def run(self):   

        #OUTPUT[0] == algorithm.t
        #OUTPUT[1] == algorithm.active_p
        #OUTPUT[2] == algorithm.pending_p
        
                
        if not isempty(OUTPUT[2]):                          #fill the list of pending Processes
            self.pending_ID_list = [ps.id for ps in OUTPUT[2]]


        if OUTPUT[0] == 0:                                  #if the time is 0, write the first line of the table displaying PS IDs and field descriptions
            block = ""
            for i in self.ID_list:
                block = ""
                if len(i) == 2:
                    block += " "
                    block += i
                    block += "  |"
                    self.ID_list_line += block
                elif len(i) == 3:
                    block += " "
                    block += i
                    block += " |"
                    self.ID_list_line += block
                
            self.ID_list_line += "t |"
            self.ID_list_line += "Pending PS"
            print(self.ID_list_line)
        self.line = "|"

        for id in self.ID_list:                            #iterate through the process list, determine process status and add the corresponding text block to the output string
            if OUTPUT[1] != None and OUTPUT[1] != -1:
                if id == OUTPUT[1].id:
                    self.line += self.active
                    self.line += "|"
                    continue
            if id in self.pending_ID_list:
                self.line += self.pending
            else:
                self.line += self.inactive
            self.line += "|"
        self.line += str(OUTPUT[0])

        if len(str(OUTPUT[0])) == 1:        
            self.line += " |"
        else:
            self.line += "|"

        ids = [str(ps.id) for ps in OUTPUT[2]]
        ts = [str(ps.t) for ps in OUTPUT[2]]
        idstr = ""
        for i,e in enumerate(ids):
            idstr += e
            idstr += " "
            idstr += ts[i]
            idstr += ","
        self.line += " "
        self.line += idstr


        print(self.line)                    #print the final string representing the next line of the table
        FULLOUTPUT.append([self.line])      #save the line into the FULLOUTPUT constant


#PROCESS CLASS

class Process:
    def __init__(self, t, ti, id):
        self.t = t
        self.ti = ti
        self.id = id

    def step(self):
        self.t -=1
        if self.t < 0:
            return False
        else:
            return True

        

    
class Main:
    def __init__(self):

        #STATES:
        # 0: Origin
        # 1: run
        # 2: history
        # 3: Rerun
        # 4: Exit

        self.state = "0"
        self.History = []
        self.save_ps_list = []

    art = text2art("Welcome   to   PSorter_SO")
    print (art)
    

    def display_history(self):   #MAIN LOOP FOR THE HISTORY MENU

        art = text2art("HISTORY")
        print(art)


        for i,Input in enumerate(self.History):
            ps_data_list = ""
            ids = [x.id for x in Input.ps_list]
            ts = [x.t for x in Input.ps_list]
            tis = [x.ti for x in Input.ps_list]

            for e in range(len(Input.ps_list)):
                data_block = "{}(T:{}, TI:{}) ".format(ids[e],ts[e],tis[e])
                ps_data_list += data_block
                      
            line = "|{}|PS List: {} ".format(i,ps_data_list)
            print(line)


        print("")
        print("indique el indice de de la entrada que desea ejecutar o -1 para salir")
        n = check_input(input(),[str(x) for x in range(-1,len(self.History))],"Porfavor indique una entrada existente")


        if n != "-1":
            self.state = "1"
            self.execute_algorithm(True, int(n))
     
        self.state = "0"



    def execute_algorithm(self, rerun,n): #MAIN LOOP FOR THE ALGORITHM EXECUTION MENU
        inputmode = "0"

        if rerun == True:                           #check for rerun, if true copy ps_list and inputmode and bypass input gathering
            if not isempty(self.History[n].params):
                PSPARAMS = setParams(self.History, n)
            ps_list = self.History[n].ps_list
            inputmode = self.History[n].inputmode
       
        else:                                      #input gathering for the upcoming execution
            inputmode = input_mode()

            if inputmode == "1":
                ps_list = takeSpecificInputs()  
            else:
                PSPARAMS = takeInputs()
                ps_list = createPs(int(PSPARAMS[0]),int(PSPARAMS[1]),int(PSPARAMS[2]), int(PSPARAMS[3]),int( PSPARAMS[4]))

        self.save_ps_list = [Process(ps.t, ps.ti,ps.id) for ps in ps_list]  #backup of process list for execution history
        algorithm = select_algorithm(ps_list)                               #declare selected algorithm
        OUTPUTFORMATTER = OutputFormatter(ps_list)                          #declare outputformatter for the algorithm
        tableFormatter(ps_list)                                             #display first table

        while self.state == "1":                                            #execute algorithm and output formatter until end conditions are met
            algorithm.run()
            OUTPUTFORMATTER.run()
            if algorithm.t > findMaxti(ps_list) and isempty(algorithm.pending_p) and algorithm.active_p == None:
                self.state  = 0

        if rerun == True:                                                               #check for rerun, if true bypass execution History update and reset ps_list in the execution history
            self.History[n].ps_list = self.save_ps_list

        if rerun == False:                                                              #execution history update
            if inputmode != "1":
                self.History.append(Input_log(FULLOUTPUT, self.save_ps_list ,PSPARAMS, inputmode))
            else:
                self.History.append(Input_log(FULLOUTPUT, self.save_ps_list ,[], inputmode))


        self.state = "0"

    def run(self):          #MAIN PROGRAM LOOP
        while self.state == "0":            #main state machine for the program
            self.state = OriginInput()

            if self.state == "1":
                self.execute_algorithm(False,0)
                

            if self.state == "2":
                self.display_history()

            if self.state == "3":
                self.state =  "1"
                self.execute_algorithm(True, -1)


class Input_log:    #EXECUTION HISTORY ENTRY CLASS
    def __init__(self, OUTPUT, PS_list, params, inputmode):
        self.OUTPUT  = OUTPUT
        self.ps_list = PS_list
        self.params = params
        self.inputmode = inputmode


MAIN = Main()

MAIN.run()
    
    
   


#   Marco Ferrero Garcia (gitHub: M4RK0V160)
        