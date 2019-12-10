from qiskit import *

qr = QuantumRegister(25)
cr = ClassicalRegister(25)
circuit = QuantumCircuit(qr,cr)


while True :

    circuit.measure(qr,cr)
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend = simulator ).result()
    hist = result.get_counts(circuit)

    for h in hist:
        print(h," : ",hist[h])

    gate = input("Enter a gate: ")
    qubit = int(input("Enter a qubit: "))

    if gate == "x":
        circuit.x(qr[qubit])

    if gate == "cx0":
        circuit.cx(qr[0],qr[qubit])

    if gate == "reset":
        circuit.reset(qr[qubit])

    if gate == "h":
        circuit.h(qr[qubit])

    if gate == "swap0":
        circuit.swap(qr[0],qr[qubit])
