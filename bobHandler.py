import fern

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
    
def garbledTableHandler(inputs,store,garbledTable,w):
    """
    Iterates through the garbled table to find the corresponding
    encrypted values related to alice and bob's values.
    """
    output = -1


    for row in garbledTable:
        rawValues = []
        for keypair in row:
            index, token = keypair
            # try and decrypt the token with w.
            value = bruteForceDecrypt(w[index], token)
            entry = (index,value)
            rawValues.append(entry)

        # if they're the same retrieve the output and decrypt it.
        if set(rawValues) == set(inputs):
            # print("garbled table:",garbledTable[row])
            index, token = garbledTable[row]
            output = bruteForceDecrypt(w[index],token)
            # print("brute force output for index:",index, output)
            if output > -1:
                break

    return output

def displayTables(table):
    print("----------------")
    print("Received Tables:")
    for table in tables:
        for i in table:
            print((i[0][0],i[0][1][-10:-2]),(i[1][0],i[1][1][-10:-2]),":-", (table[i][0],table[i][1][-10:-2]))


def bobHandler(data,inputs=[1]):
    # variables redeclared for simplicity    
    tables, w, aliceIn = data['table'], data['w'], data['aliceIn']
    aliceIndex, bobIndex = data['aliceIndex'], data['bobIndex'], 
    outputP, gateSet = data['outputP'], data['gateSet'],
    bobColouring = data['bobColouring']
    
    # setup store.
    store = [0 for i in range(data['numberOfIndexes']+1)]
   
    # store alices input in the store array.
    for i in range(len(aliceIndex)):
        index = aliceIndex[i]
        encryptedValue = aliceIn[i]
        store[index] = bruteForceDecrypt(w[index], encryptedValue)

    # encrypt bob's input with the P's and store these values into our store.
    for i in range(len(inputs)):
        index = bobIndex[i]
        encryptedValue = inputs[i]
        store[index] = bruteForceDecrypt(w[index], encryptedValue)

    # # iterate through the gates
    for i in range(len(gateSet)):
        # get gate value.
        gate = gateSet[i]
        # initialise inputs
        inputs = [(i,store[i]) for i in gate['in']]
        print("gate in:", gate['in'])
        print("so the input is:",inputs)
        # print("inputs:",inputs)
        # get garbled table for this gate
        table = tables[i]
        # compute value
        value = garbledTableHandler(inputs,store,table,w)
        index = gate['id']
        # store the output
        store[index] = value

    # retrieve output and decrypt it.
    decryptedOutputs = []
    for i in range(len(data['outIndex'])):
        index = data['outIndex'][i]
        value = store[index]
        pVal  = outputP[i]
        print("OUTPUT i",index,"v:",value,"p",pVal)
        decryptedValue = xor(value,pVal)
        decryptedOutputs.append(decryptedValue)

    return decryptedOutputs
    