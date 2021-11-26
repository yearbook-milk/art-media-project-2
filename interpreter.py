import sys, random, time
from math import *
#load script
f = open('helloworld.pcs', 'r')
script = f.read()
f.close()

pieces = script.split('\n')
#print(pieces)

def die(msg):
    input('FATAL: '+str(msg)+f' on instruction {ticker}\n<ENTER> to stop execution.')
    exit()

def batchreplace(inp, variablelist):
    for i in variablelist:
        inp = inp.replace(i, str(variablelist[i]))
    return inp

#program ticker and vars
ticker = 0
terminated = False
varlist = {}
toreplace = {
'(': '',
')': '',
    }

while not terminated:
    try:
        command = pieces[ticker].split(' ',1)[0]
        params = pieces[ticker].split(' ',1)[1]
    except:
        command = 'ERROR'
        params = 'ERROR'
    
    moveup1 = True

    #echo
    if command == 'echo': print(batchreplace(params, varlist))

    if command == 'constassign':
        name = params.split('<-')[0]
        try:
            val = int(params.split('<-')[1])
            varlist[name] = val
            print(f'vb: Assigned {val}->{name}')
        except:
            die('Illegal variable value in constassign')

    if command == 'randomassign':
        name = params.split('<-')[0]
        val = batchreplace( batchreplace(params.split('<-')[1], varlist), toreplace)
        try:
            flr = int(val.split(',')[0])
            ceil = int(val.split(',')[1])
        except:
            die('Illegal floor or ceiling value in randomassign')
        final = random.randint(flr, ceil)
        varlist[name] = final
        print(f'vb: Assigned {final} from ({val})->{name}')

    if command == 'mathassign':
        name = params.split('<-')[0]
        val = batchreplace(params.split('<-')[1], varlist)
        
        try: final = eval(val)
        except: die('Invalid mathmatical expression in mathassign')

        print(f'vb: Assigned {final}->{name} from {val}')

    if command == 'jump':
        newticker = pieces.index(f'@ {params}')
        if newticker == -1: die('No such symbolic jump destination in jump')
        print(f'vb: Moving program counter from {ticker} to {newticker}')
        moveup1 = False
        ticker = newticker

        #****empty lines do count as instructions (although the interpreter does not act on them)

    if command == 'litjump':
        try: newticker = int(params)
        except: die('Invalid instruction address in litjump')

        try: instruction = pieces[newticker]
        except: die('Out of bounds address in litjump')

    if command == 'exit':
        print(params)
        terminated = True

    if command == 'delay':
        params = params.split(' ')
        try: deltime = int(params[0])
        except: die('Invalid delay time in delay')
        if params[1] == 's':
            print(f'vb: Delaying {deltime} seconds')
            time.sleep(deltime)
        if params[1] == 'ms':
            print(f'vb: Delaying {deltime} miliseconds')
            time.sleep(deltime/1000)

    if command == 'varcopy':
        name = params.split('<-')[0]
        try: donor = varlist[params.split('<-')[1]]
        except: die('Undefined variable in varcopy')
        varlist[name] = donor
        print(f'vb: Copied {params.split("<-")[1]} ({donor})->{name}')
        


    #advance the program ticker
    if moveup1: ticker = ticker + 1

exit()

    
