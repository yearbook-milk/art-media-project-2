import sys, random, time, serial
from math import *
#load script
f = open(sys.argv[1], 'r')
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
serialhandles = {}
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

    if command == 'exprassign':
        name = params.split('<-')[0]
        varlist[name] = str(params.split('<-')[1])
        print(f'vb: ExprAssigned "{params.split("<-")[1]}"->{name}')

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
        #print(val)
        #val = params
        #print(vals)
        
        try: final = eval(val)
        except: die('Invalid mathmatical expression in mathassign')


        print(f'vb: Assigned {final}->{name} from {val}')
        varlist[name] = final

    if command == 'jump':
        params = batchreplace(params, varlist)
        newticker = pieces.index(f'@ {params}')
        if newticker == -1: die('No such symbolic jump destination in jump')
        print(f'vb: Moving program counter from {ticker} to {newticker}')
        moveup1 = False
        ticker = newticker

        #****empty lines do count as instructions (although the interpreter does not act on them)

    if command == 'litjump':
        params = batchreplace(params, varlist)
        try: newticker = int(params)
        except: die('Invalid instruction address in litjump')

        try: instruction = pieces[newticker]
        except: die('Out of bounds address in litjump')

    if command == 'exit':
        print(params)
        terminated = True

    if command == 'delay':
        params = batchreplace(params, varlist)
        params = params.split(' ')
        try: deltime = int(params[0])
        except: die('Invalid delay time in delay')
        try:
            if params[1] == 's':
                print(f'vb: Delaying {deltime} seconds')
                time.sleep(deltime)
            if params[1] == 'ms':
                print(f'vb: Delaying {deltime} miliseconds')
                time.sleep(deltime/1000)
        except:
            print(f'vb: Delaying {deltime} seconds (fallback)')
            time.sleep(deltime)
                

    if command == 'varcopy':
        name = params.split('<-')[0]
        try: donor = varlist[params.split('<-')[1]]
        except: die('Undefined variable in varcopy')
        varlist[name] = donor
        print(f'vb: Copied {params.split("<-")[1]} ({donor})->{name}')

    if command == 'debug':
        print('db Varpool: ' + str(varlist).replace(',', '\n'))
        print('db Instructionpool: ' + str(pieces).replace(',', '\n'))


    if command == 'if':
        params = batchreplace(params, varlist)
        statement_bool = eval(batchreplace(params, toreplace))
        #print(statement_bool)

        splicedarray = pieces[ticker-1:]
        endpoint = None
        for i in splicedarray:
            if 'endif' in i: endpoint = pieces.index(i, ticker-1)

        if endpoint == None:
            die('No End of If (EOI) in if')


        if statement_bool: print(f'vb: Statement evaluated to {statement_bool}, NO JUMP MADE (supposed jump address = {endpoint})')
        if not statement_bool:
            print(f'vb: Statement evaluated to {statement_bool}, JUMP MADE,jump address = {endpoint}')
            ticker = endpoint
            moveup1 = False

    if command == 'inpassign' or command == 'inputassign':
        x = input('int-> ')
        try: x = int(x)
        except: die('Noninteger user input in inpassign')

        varlist[params] = x

    if command == 'str.inpassign' or command == 'str.inputassign':
        x = input('str-> ')
        varlist[params] = x

    if command == 'import':
        try:
            f = open(params)
            c = f.read()
            f.close()
        except:
            die(f'FileIO error in reading file {params} in import')

        tobeinserted = c.split('\n')
        tobeinserted.reverse()
        for i in tobeinserted:
            pieces.insert(ticker+1, str(i))

    if command == 'openserial':
        params = batchreplace(batchreplace(params,varlist), toreplace).split(';')
        sethandle = False
        serialhandle = None
        timeout = None
        for i in params:
            iss = i.split('=')
            if iss[0] == 'handlename' or iss[0] == 'hn':
                serialhandles[iss[1]] = serial.Serial()
                serialhandles[iss[1]].timeout = timeout
                sethandle = True
                serialhandle = iss[1]

        if not sethandle: die('No name attached to Serial handle in openserial') # establish handle name first

        for i in params:
            iss = i.split('=')
            if iss[0] == 'baud':
                try:
                    serialhandles[serialhandle].baudrate = int(iss[1])
                    print(f'vb: Assigned {serialhandle} baudrate to {iss[1]}')
                except: die('Non-integer baud rate in openserial')
                
            if iss[0] == 'timeout':
                try:
                    serialhandles[serialhandle].timeout = int(iss[1])
                    print(f'vb: Assigned {serialhandle} timeout to {iss[1]}')
                except: die('Non-integer timeout in openserial')
             
            if iss[0] == 'port':
                serialhandles[serialhandle].port = str(iss[1])
                print(f'vb: Assigned {serialhandle} port to {iss[1]}')

        try: serialhandles[serialhandle].open()
        except Exception as e: die('Could not open serial port in serialopen, ul_error: ' + str(e))
        print(f'vb: Opened {serialhandle} as serial port.')

    if command == 'comcmd':
        params = batchreplace(params, toreplace)
        params = params.split('<-')
        try:
            serialhandles[params[0]].write(bytes(batchreplace(params[1], varlist), 'ascii'))
            print(f'Wrote {batchreplace(params[1], varlist)} to {params[0]}')
        except Exception as e: die('Could not write to serial port in comcmd, ul_error: '+str(e))

    if command == 'terminateserial':
        try: serialhandles[params].close()
        except: die(f'Unknown error in closing serial port {params}')

        print(f'vb: Serial object closed: serialhandles[{params}].')
        
            

        #print(str(pieces).replace(',','\n'))
        #input('Any key to continue')

        


    #advance the program ticker
    if moveup1: ticker = ticker + 1


input('vb: Program terminated.')
