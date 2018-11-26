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
    
def garbledTableHandler(keys,values,store,garbledTable):
    """
    Iterates through the garbled table to find the corresponding
    encrypted values related to alice and bob's values.
    """
    dictionaryKey = tuple(values)
    row = garbledTable[dictionaryKey]
    _, rowToken = row
    output = fern.multiDecryptInput(keys, rowToken)
    # convert output to a similar fashion.
    # (this is necessary because fernet only takes in
    # bytes from strings and not necessarily anything else.)
    output = output.decode('utf-8')
    output = output[1:-1].split(",")
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
    tables, aliceIn = data['table'], data['aliceIn']
    aliceIndex, bobIndex = data['aliceIndex'], data['bobIndex']
    outputDecryption, gateSet = data['outputDecryption'], data['gateSet']
    
    # setup store.
    store = [0 for i in range(data['numberOfIndexes']+1)]

    # store bob's encrypted values.
    if pinputs:
        for i in range(len(pinputs)):
            wireIndex = bobIndex[i]
            # overcomes disparities between the ZMQ transferred file and the
            # value that's directly transported in local.
            try:
                rawData = pinputs[i].decode('utf-8')
            except:
                rawData = pinputs[i]
            # pinputs[1] is a string of a concatenation of the key and the
            # value, we'll need to conver them to variables that are
            # consistent with the rest of the program.
            wireKey, wireV = rawData.split(" + ")
            wireKey = wireKey.replace("b'", "").replace("'", "")
            wireKey = wireKey.encode("utf-8")
            wireV = int(wireV)
            # store result.
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
        value = garbledTableHandler(inputs, values, store, table)
        index = gate['id']
        # store the output
        store[index] = value

    # retrieve output and decrypt it.
    decryptedOutputs = []
    for i in range(len(data['out'])):
        index = data['out'][i]
        value = store[index][1]
        pVal = outputDecryption[i]
        decryptedValue = xor(value, pVal)
        decryptedOutputs.append(decryptedValue)

    return decryptedOutputs
