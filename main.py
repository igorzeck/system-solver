# Lê de arquivo e transforma em legivel
# Temporariamente
import funcs

arq = open("input_matriz", "r")
string = arq.read()

matriz = []
funcs.matrificar(string, matriz)
