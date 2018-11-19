import os
import json
import gates as gate
from cryptography.fernet import Fernet
import random
import array

class Circuit:
    def __init__(self,circuitDict, pBitOverride=None):
        """
        Circuit class to be computed by Alice. This means
        Alice knows the p
        """
        self.name = None
        self.alice = None
        self.bob = None
        self.gates = None
        self.out = None
        # processes json.
        self.processCircuit(circuitDict)
        # generate wire encryption keys
        self.generateWireKeys()
        # generate p bits
        self.generatePBits(override=pBitOverride)
        # load logic gates
        self.logic = gate.Gates()

    def processCircuit(self,circuit):
        """
        Loads the json and adds the relevant contents into the
        object.
        """
        for key in circuit.keys():
            setattr(self,key,circuit[key])
        self.raw = circuit
            
    def compute(self,inputs, encrypt=False):
        """
        Computes the gate operations and then returns the output.
        """
        # creates stores.
        limit = max([max(self.out),max([i['id'] for i in self.gates])])
        # create array to reference values at.
        store = [0 for i in range(limit+1)]

        # store inputs
        input_ids = self.alice+self.bob if self.bob else self.alice
        for i in input_ids:
            store[i] = inputs.pop(0)
        
        # iterate through the gate operations
        for gate in self.gates:
            # load logic gate
            logic = getattr(self.logic,gate['type'])
            # load inputs
            if encrypt:
                parameters = tuple([self.xor(store[i],self.p[i]) for i in gate['in']])
            else:
                parameters = tuple([store[i] for i in gate['in']])
            # get output
            result = logic(parameters)
            # store result
            store[gate['id']] = result
        
        if encrypt:
            return [self.xor(store[i],self.p[i]) for i in self.out]
        else:
            return [store[i] for i in self.out]
    
    def generateWireKeys(self):
        wire_count = max([max(self.out),max([i['id'] for i in self.gates])])
        # generate arbitary zeros and ones
        w = [[Fernet.generate_key() for j in range(0,2)] for i in range(wire_count+1)]
        # assign values.
        self.w = w
    
    def generatePBits(self, override=None):
        """
        generates random p bits.
        these are the colouring bits on each wire.
        """
        # each wire w has two random keys (consult p28)
        w = override if override else []
        # get max limit of the gates.
        wire_count = max([max(self.out),max([i['id'] for i in self.gates])])
        
        if override and (len(override) != wire_count):
            print("YOUR P BITS WONT WORK.")
        # generate arbitary zeros and ones
        w = [random.choice([0,1]) for i in range(wire_count+1)]
        self.p = w
    
    def printRow(self, alice, bob, encrypt=False):
        """
        Prints an individual row given inputs from alice and bob.
        alice and bob are lists of binary values i.e [0,0,1]
        """
        if bob:
            inputs = alice + bob
            pr = "Alice"+str(self.alice)+" = " 
            for i in alice:
                pr += str(i) + " "
            pr += "  Bob"+str(self.bob)+" = "
            for i in bob:
                pr += str(i) + " "
            pr += "  Outputs"+str(self.out)+" = "
            for i in self.compute(inputs,encrypt=encrypt):
                pr += str(i) + " "
            print(pr)
        else:
            inputs = alice
            pr = "Alice"+str(self.alice)+" = " 
            for i in alice:
                pr += str(i) + " "
            pr += "  Outputs"+str(self.out)+" = "
            for i in self.compute(inputs,encrypt=encrypt):
                pr += str(i) + " "
            print(pr)
    
    def printall(self, encrypt=False):
        """
        Helper function to handle printing as is specified in the
        coursework notes.
        """
        print(self.name)
        for alice in self.perms(len(self.alice)):
            if self.bob:
                for bob in self.perms(len(self.bob)):
                    self.printRow(alice,bob,encrypt=encrypt)
            else:
                self.printRow(alice,bob=None,encrypt=encrypt)
        print()
        
    def fernetXOR(encryptedToken, p):
        xoredTokenBits = []
        for i in encryptedToken:
            binary = i
            newBinary = [XOR(int(binary[j]),p) for j in range(len(binary))]
            newBinary = ''.join(str(i) for i in newBinary)
            xoredTokenBits.append(newBinary)
        return xoredTokenBits
    
    def encodeFernetXOR(token):
        return ["{0:b}".format(i) for i in token]
    
    def decodeFernetXOR(ku):
        ku = [int(m, 2) for m in ku]
        ku = "".join(map(chr, ku))
        return  ku.encode('utf-8')
    
    def generateGarbledCiruitTables(self,encrypt=True):
        """
        Computes the gate operations and then returns the output.
        """   
        garbledTables = []
        
        # iterate through the gate operations
        for gate in self.gates:
            garbledLogicGateTable = []
            # load logic gate
            logic = getattr(self.logic,gate['type'])
                # generate permutations of inputs.
                
            for potentialInput in self.perms(len(gate['in'])):
                
                encryptedInput = []
                # encrypt the values with w, and then XOR with p.
                for i in range(len(gate['in'])):
                    wire, value = gate['in'][i], potentialInput[i]
                    # xor with w[wire]
                    encryptedValue = self.xor(value,self.w[wire][value])
                    # xor with p[wire]
                    encryptedValue = self.xor(encryptedValue,self.p[wire])
                    encryptedInput.append(encryptedValue)
                    
                parameters = tuple(encryptedInput)  
                # get output
                result = logic(parameters)
                # encrypt output
                encryptedOutput = self.xor(result,self.p[gate['id']])
                # generate dictionary to store.
                entry = {'id': gate['id'], 'inputs' : [], 'outputs':[]}
                for i in range(len(gate['in'])):
                    entry['inputs'].append({
                                  'wire':   gate['in'][i], 
                        'encryptedValue':   parameters[i]
                    })
                # there should be only one output.
                entry['outputs'].append({
                              'wire':   gate['id'], 
                    'encryptedValue':   encryptedOutput
                })
                
                # add table row into our list
                garbledLogicGateTable.append(entry)
            # add our logic gate table to the main table
            garbledTables.append(garbledLogicGateTable)

        return garbledTables
        
        
    def sendToBob(self,aliceInput):
        # garble the table
        garbled = self.generateGarbledCiruitTables()
        # get wire keys
        w = self.w
        # get alice's encrypted bits
        encryptedBits = []
        
        for i in range(len(aliceInput)):
            bit = self.xor(aliceInput[i], self.w[self.alice[i]][aliceInput[i]])
            encryptedBits.append(bit)
            
        # get decryption bit for output wire
        outputDecryptionBit = self.p[self.out[0]]
        
        return {
            'table'  : garbled,
            'w'      : w,
            'aliceIn': encryptedBits,
            'aliceIndex' : self.alice,
            'bobIndex' : self.bob,
            'numberOfIndexes' : max([max(self.out),max([i['id'] for i in self.gates])]),
            'outputDecryption': outputDecryptionBit
        }
        
    @staticmethod
    def perms(n):
        """
        Helper function to generate permutations for binary integers
        based on the length n.
        """
        if not n:
            return
        entries = []
        for i in range(2**n):
            s = bin(i)[2:]
            s = "0" * (n-len(s)) + s
            ent = [int(i) for i in s]
            entries.append(ent)
        return entries
    
    @staticmethod
    def xor(value, key):
        # use once to encrypt
        # twice to decrypt
        if value == key:
            return 0
        return 1


if __name__ == "__main__":
    folderpath = "../json"
    for file in os.listdir(folderpath):
        filename = os.path.join(folderpath,file)
        with open(filename) as json_file:
            json_circuits = json.load(json_file)
            for json_circuit in json_circuits['circuits']:
                circuit = Circuit(json_circuit)
#         print(circuit.name)
                if "Smart" in circuit.name:
#             circuit.printRow([0,0], [0,0])
                    circuit.printall(encrypt=False)
    #         print(circuit.p)
    #         garble  = GarbledCircuit(circuit)
    #         print(circuit.raw)
                break
        
	#     break
    
	# loadall()
