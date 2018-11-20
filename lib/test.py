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
            bobHandler.bobHandler(toBob)
#         for i in circuit.generateGarbledCiruitTables():
#             for j in i:
#                 print(j)

#         key = Fernet.generate_key()
#         f = Fernet(key)
#         inpStr = b"my deep dark secret"
#         token = f.encrypt(inpStr)
#         print(token)
#         col = circuit.computeWireColouring(token,1)
#         print(col)
#         colback = circuit.computeWireColouring(col,1)
#         print(colback)
#         print(circuit.w)
#         print(circuit.p)
#         circuit.printall()
#         garble  = GarbledCircuit(circuit)
#         print(circuit.raw)
        # break
    # break
# loadall()