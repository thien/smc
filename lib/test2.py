import circuit as c
import fern
import os
import bobHandler
import json
import ot

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
        if " " in json_circuit['name']:
            circuit = c.Circuit(json_circuit)
            print("----------------")
            print(json_circuit['name'])
            
            for aliceInput in perms(len(json_circuit['alice'])):
                # build relevant files needed to send to bob
                toBob = circuit.sendToBob(aliceInput)
                # iterate through bob's potential inputs.
                for bobInput in perms(len(json_circuit['bob'])):
                    # get the reference output to verify the results.
                    test = circuit.compute(aliceInput + bobInput)
                    # do oblivious transfer on this.
                    bobPInput = []
                    for i in range(len(bobInput)):
                        bobValue = bobInput[i]
                        bobIndex = toBob['bobIndex'][i]
                        # print("bobV", bobValue, "bobI",bobIndex)
                        otB = ot.Bob(bobValue)
                        inp1, inp2 = circuit.setupBobOT(bobIndex)
                        otA = ot.Alice(inp1, inp2)
                        # garbled circuit stuff.
                        ot_c = otA.send_c()
                        h0 = otB.send_h0(ot_c)
                        c_1, E, length = otA.sendMessage(h0)
                        payload = int(otB.getMessage(c_1, E, length))
                        bobPInput.append(payload)
                    # bob evaluates the output.
                    output = bobHandler.bobHandler(toBob,pinputs=bobPInput)
                    # create checksum to determine whether
                    # our output is the same as the input.
                    check = True if test == output else False
                    if check:
                        print("Alice:",aliceInput," Bob",bobInput,":- ",output)
                    else:
                        print("The garbled circuit does not compute.")
            # break
    # break
