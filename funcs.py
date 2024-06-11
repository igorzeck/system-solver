# Transforma string do sistema para string que reflita a matriz
def sis_p_str(valor):
    # PASSO 1
    # Primeiro identifica quantas variáveis a linha com maior número de variáveis tem
    # Lista os elementos
    # Separa por linha
    linhas_valor = valor.split('\n')
    lista_letras = []
    # Separa os elementos da linha para cada linha
    for l_i, linha in enumerate(linhas_valor):
        try:
            elementos = linha.split()
            # Verifica se linha é legal
            if linha_e_legal(elementos):
                # Se for legal, próximo passo!
                # Contagem de variáveis! Guarda apenas o maior número de variáveis!
                # Conta apenas letras únicas
                for el in elementos:
                    for ema in el:
                        if ema.isalpha() and ema not in lista_letras:
                            lista_letras.append(ema)
            else:
                raise Exception(f'linha {l_i} | \'{linha}\' é ilegal!')
        except Exception as e:
            print(e)
            return False
    print('Letras: ', lista_letras)
    max_linhas = len(lista_letras)
    # PASSO 2
    # Gera matriz usando como referência as letras



def linha_e_legal(linha_el):
    # Primeiro verifica se tem, no mínimo 3 elementos a = c
    if len(linha_el) < 3:
        return False
    # Verifica se linha tem símbolo de = e apenas 1
    if linha_el.count('=') != 1:
        return False
    # Se nada errado, tudo certo
    return True


# Transforma string de valores em matriz no Python
def matrificar(valor, matriz):
    lines = valor.split('\n')
    # Por linha separa elementos
    for line in lines:
        line_list = line.split()
        val_list = []
        # Numerifica
        for val in line_list:
            if val.isdigit():
                val_list.append(int(val))
            else:
                raise ValueError ("Value is not numerical!")
        matriz.append(val_list)
