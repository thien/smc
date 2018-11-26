import fern

"""
Submission by:
Thien Nguyen (tn518 / 01565994)
Jinwei Zhang (jz2618 / 01540854)
"""

def xor(value, key):
    # use once to encrypt
    # twice to decrypt
    if value == key:
        return 0
    return 1

def bruteForceDecrypt(keys,token):
    for key in keys:
        try:
            return int(fern.decryptInput(key,token))
        except:
            pass
    return -1
    
def garbledTableHandler(keys,values,store,garbledTable,w):
    """
    Iterates through the garbled table to find the corresponding
    encrypted values related to alice and bob's values.
    """

    dictionaryKey = tuple(values)
    row = garbledTable[dictionaryKey]
    _, rowToken = row
    output = fern.multiDecryptInput(keys, rowToken)
    output = output.decode('utf-8')
    output = output[1:-1].split(",")
    # print("got output:", output)
    wireKey, wireV = output
    wireKey = wireKey[2:-1].encode('utf-8')
    wireV = int(wireV)
    
    return (wireKey, wireV)

def displayTables(table):
    print("----------------")
    print("Received Tables:")
    for table in tables:
        for i in table:
            print((i[0][0],i[0][1][-10:-2]),(i[1][0],i[1][1][-10:-2]),":-", (table[i][0],table[i][1][-10:-2]))

def evaluate(data, pinputs=None):
    # variables redeclared for simplicity  
    aliceW = data['aliceW']  
    tables, w, aliceIn = data['table'], data['w'], data['aliceIn']
    aliceIndex, bobIndex = data['aliceIndex'], data['bobIndex']
    outputDecryption, gateSet = data['outputDecryption'], data['gateSet']
    
    # setup store.
    store = [0 for i in range(data['numberOfIndexes']+1)]

    # store bob's encrypted values.
    if pinputs:
        for i in range(len(pinputs)):
            wireIndex = bobIndex[i]
            # pinputs[1] is a string of a concatenation of the key and the value.
            wireKey, wireV = str(pinputs[i]).replace('"', "").split(" + ")
            wireKey = wireKey[3:-1].encode('utf-8')
            wireV = int(wireV)
            store[wireIndex] = (wireKey, wireV)

    # store alices encrypted inputs.
    for i in range(len(aliceIndex)):
        wireIndex = aliceIndex[i]
        wireKey, wireV = aliceW[i]
        store[wireIndex] = (wireKey, wireV)

    # iterate through the gates
    for i in range(len(gateSet)):
        # get gate value.
        gate = gateSet[i]
        # initialise inputs
        inputs = [store[i][0] for i in gate['in']]
   
        values = [store[i][1] for i in gate['in']]
        # get garbled table for this gate
        table = tables[i]
        # compute value
        value = garbledTableHandler(inputs,values,store,table,w)
        index = gate['id']
        # store the output
        store[index] = value

    # retrieve output and decrypt it.
    decryptedOutputs = []
    for i in range(len(data['out'])):
        index = data['out'][i]
        value = store[index][1]
        print("GOT:",value)
        pVal  = outputDecryption[i]
        decryptedValue = xor(value,pVal)
        decryptedOutputs.append(decryptedValue)
        # kill

    return decryptedOutputs
    
