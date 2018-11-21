import circuit as c
import fern
import os
import bobHandler
import json

folderpath = "../json"
for file in os.listdir(folderpath):
    filename = os.path.join(folderpath,file)
    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    for json_circuit in json_circuits['circuits']:
        if "AND gate" == json_circuit['name']:
            circuit = c.Circuit(json_circuit)
            print(json_circuit)
            aliceInput = [1]
            toBob = circuit.sendToBob(aliceInput)
            bobInput = [1]

            output = bobHandler.bobHandler(toBob,inputs=bobInput)
            print("Alice:",aliceInput," Bob",bobInput,":- ",output)
