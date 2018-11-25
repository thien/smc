import circuit as c
import fern
import os
import bobHandler
import json

folderpath = "json"
for file in os.listdir(folderpath):
    filename = os.path.join(folderpath,file)
    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    for json_circuit in json_circuits['circuits']:
        if "AND gate" in json_circuit['name']:
            circuit = c.Circuit(json_circuit)
            print("----------------")
            print(json_circuit['name'])
            print("Alice:",json_circuit['alice'],"\t","Bob:",json_circuit['bob'])
            print("Generating Alice's Values")
            aliceInput = [0]
            print("Sending encrypted response to Bob")
            toBob = circuit.sendToBob(aliceInput)
            print("Generating Bob's Values")
            bobInput = [0]


            for i in toBob['table'][0].keys():
                print(i)

            output = bobHandler.bobHandler(toBob,inputs=bobInput)
            print("Alice:",aliceInput," Bob",bobInput,":- ",output)
            
            break