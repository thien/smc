import circuit as c
import fern
import os
import bobHandler
import json


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

folderpath = "../json"
for file in os.listdir(folderpath):
    filename = os.path.join(folderpath,file)
    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    for json_circuit in json_circuits['circuits']:
        if "Smart" in json_circuit['name']:
            circuit = c.Circuit(json_circuit)
            print("----------------")
            print(json_circuit['name'])
            print("Alice:",json_circuit['alice'],"\t","Bob:",json_circuit['bob'])
            print("Generating Alice's Values")
            for x in perms(len(json_circuit['alice'])):
                aliceInput = x
                print("Sending encrypted response to Bob")
                toBob = circuit.sendToBob(aliceInput)
                print("Generating Bob's Values")
                # print(toBob['aliceIn'])


                for y in perms(len(json_circuit['bob'])):
                    bobInput = y
                    # do oblivious transfer on this.
                    bobPInput= toBob['bobPotentialP'][tuple(bobInput)]
                    output = bobHandler.bobHandler(toBob,inputs=bobInput, pinputs=bobPInput)

                    print("Alice:",aliceInput," Bob",bobInput,":- ",output)
            # break
    # break