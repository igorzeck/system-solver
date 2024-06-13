# Lê de arquivo e transforma em legivel
# Temporariamente
import funcs

arq = open("input_matriz", "r")
string = arq.read()
arq.close()
matriz = []
# funcs.matrificar(string, matriz)
# print(matriz)
variaveis, matriz = funcs.matrificar(string)
funcs.print_matriz(matriz)
matriz = funcs.calcular(matriz)
funcs.print_matriz(matriz)

# Resultado:
print("Classificação:", funcs.resultar(matriz, variaveis))
# print(funcs.linha_e_legal([1, '=', 2]))
# print(funcs.linha_e_legal([1, 'x', 2]))
# print(funcs.linha_e_legal([1, 'x']))
