def matrificar(input, matriz):
    lines = input.split('\n')
    # Por linha separa elementos
    for line in lines:
        line_list = line.split()
        matriz.append(line_list)
