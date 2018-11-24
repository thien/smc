import util
import ot
import os
import time
import sys
import circuit
import json
import bobHandler as bh

os.system('clear')

class Alice:
    def __init__(self):
        self.server = util.ServerSocket()

    def obliviousTransfer(self, input1, input2):
        alice = ot.Alice(input1, input2)
        # wait until bob is online
        ready = server.receive()
        if ready:
            # send c
            c = alice.send_c()
            self.server.send(c)
            # wait for bob to send H0 so that we can receive it.
            h0 = self.server.receive()
            # compute c_1, E, length
            c_1, E, length = alice.sendMessage(h0)
            # send c_1, E, length to Bob.
            payload = (c_1, E, length)
            self.server.send(payload)
            print("Completed transaction of payload.")

    def garbledTable(self,garbled):
        ready = server.receive()
        if ready:
            server.send(garbled)

class Bob:
    def __init__(self):
        self.client = util.ClientSocket()
        self.inputs = []


    def obliviousTransfer(self, inputIndex):
        # set up ot class for Bob
        bob = ot.Bob(inputIndex)
        # set up ready.
        self.client.send(True)
        # wait to receive c value
        c = client.receive()
        # generate H0
        H0 = bob.send_h0(c)
        # send H0 to alice
        self.client.send(H0)
        # wait for Alice to send h0, E, length as a payload
        (c_1, E, length) = client.receive()
        # compute response
        message = bob.getMessage(c_1, E, length).decode()
        return int(message)


    def garbledTable(self,input):
        self.client.send(True)
        # wait to receive garbled table
        self.garbledTable = self.client.receive()

    def evaluate(self, bobInputs):
        output = bh.bobHandler(self.garbledTable, bobInputs)

def loadJson(filepath):
    circ = None
    with open(filepath) as json_file:
        json_circuits = json.load(json_file)
        for json_circuit in json_circuits['circuits']:
            circ = circuit.Circuit(json_circuit)
            break
    return circ

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

if __name__ == "__main__":

    if sys.argv[1] == 'alice':
        print("this is alice")
        # json circuit
        circ = None
        if sys.argv[2]:
            jsonPath = sys.argv[2]
        circ = loadJson(jsonPath)
        # setup alices bits (do an iteration)
        alicesPotentialBits = perms(len(circ.alice))
        for aliceBits in alicesPotentialBits:
            # compute garbled circuit and other
            # necessary things to transfer to bob.
            garbledCircuit = circuit.sendToBob(aliceBits)
            for i in len(circ.bob):
                # 

    elif sys.argv[1] == 'bob':
        # prime_group = None			# bob receives group from alice
        print("this is bob")
        print(perms(3))
