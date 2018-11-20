import fern

def xor(value, key):
        # use once to encrypt
        # twice to decrypt
        if value == key:
            return 0
        return 1
    
def bobHandler(data,inputs=[1]):
    
    # 'table'  : garbled,
    # 'w'      : w,
    # 'aliceIn': encryptedBits,
    # 'aliceIndex' : self.alice,
    # 'bobIndex' : self.bob,
    # 'numberOfIndexes' : number of indexes..
    # 'outputDecryption': outputDecryptionBit
    
    tables, w, aliceIn = data['table'], data['w'], data['aliceIn']
    aliceIndex, bobIndex = data['aliceIndex'], data['bobIndex'], 
    outputDecryption, gateSet = data['outputDecryption'], data['gateSet'],
    bobColouring = data['bobColouring']

    """
    TODO: 
    - test that the bobhandler can get the original output.
    x use encryption instead of xor.
    - build parser for the table.
    x table should be indexed by encryption and p value.

    NOTE:

    you need to implement:
    - finding the encrypted value for alice
    - finding the encrypted value for bob
    - finding the corresponding matching value that corresponds to this input.
    - storing this in the encrypted array
    - getting the output value.
    """
    
    encryptedStore = [0 for i in range(data['numberOfIndexes']+1)]
    
    print("----------------")
    print("Received Tables:")
    for table in tables:
        for i in table:
            print((i[0][0],i[0][1][-10:-2]),(i[1][0],i[1][1][-10:-2]),":-", (table[i][0],table[i][1][-10:-2]))


    alicesDecryptedBits = []
    bobsDecryptedBits = []

    # encrypt bob's input.
    bobsInput = inputs

    bobsEncryptedInputs = [xor(data['bobP'][i],inputs[i]) for i in range(len(inputs))]
    # encrypt bob's input with w.
    # bobsEncryptedInputs = []
    # for i in range(len(bobIndex)):
    #     colouredInput = xor(bobsInput[i], bobColouring[i])
    #     encryptedInp = fern.encryptInput(w[bobIndex[i]][bobsInput[i]], colouredInput)
    #     bobsEncryptedInputs.append(encryptedInp)

    # # store bob's input in the store array.
    # for i in range(len(bobIndex)):
    #     encryptedStore[bobIndex[i]] = bobsEncryptedInputs[i]

    # store alices input in the store array.
    for i in range(len(aliceIndex)):
        encryptedStore[aliceIndex[i]] = aliceIn[i]
        for wAttempt in w[aliceIndex[i]]:
            try:
                alicesDecryptedBits.append((aliceIndex[i], int(fern.decryptInput(wAttempt,aliceIn[i])), aliceIn[i]))
            except:
                pass
    print("Alices Decrypted Bits:",alicesDecryptedBits)
    # get bob's decrypted bit inputs.


    # iterate through the gates
    for i in range(len(gateSet)):
        # get gate value.
        gate = gateSet[i]
        print(gate['in'])
        # get garbled table for this gate
        garbledTable = tables[i]
        for row in garbledTable:
            print(row)
        
        # # get the values and get the outcome and store it.
        # tupleSet = []
        # for inputIndex in gate['in']:
        #     encryptedValue = encryptedStore[inputIndex]
        #     tupleSet.append((inputIndex,encryptedValue))
        # tupleSet = tuple(tupleSet)

        # print((tupleSet[0][0],tupleSet[0][1][-10:-2]),(tupleSet[1][0],tupleSet[1][1][-10:-2]))
        # print("got",table[tupleSet])
    # get the output gate value
    # decrypt.
    # xor with p
    pass
    