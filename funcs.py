IMPOSS = 0
POSS_INDET = 1
POSS_DET = 2


# Transforma string do sistema para string que reflita a matriz
def sis_p_str(valor):
    # PASSO 1
    # Primeiro identifica quantas variáveis a linha com maior número de variáveis tem
    # Lista os elementos
    # Separa por linha
    linhas_valor = valor.split('\n')
    lista_vars = []
    # Separa os elementos da linha para cada linha
    for l_i, linha in enumerate(linhas_valor):
        try:
            elementos = linha.split()
            # Verifica se linha é legal
            lista_el_linha = []
            if linha_e_legal(elementos):
                # Se for legal, próximo passo!
                # Contagem de variáveis! Guarda apenas o maior número de variáveis!
                # Conta apenas letras únicas
                for el in elementos:
                    # Verifica se tem múltiplos números
                    if el.isnumeric() and any(llle.isnumeric() for llle in lista_el_linha):
                        raise Exception(
                            f"Múltiplas ocorrências de números na mesma linha: {l_i} | {linha}")
                    elif el.isnumeric():
                        lista_el_linha.append(el)
                    for ema in el:
                        if ema.isalpha():
                            if ema not in lista_vars:
                                lista_vars.append(ema)
                            if ema not in lista_el_linha:
                                lista_el_linha.append(ema)
                            else:
                                raise Exception(
                                    f"Múltiplas ocorrências de uma mesma variável na mesma linha: {l_i} | {linha}")
            else:
                raise Exception(f'linha {l_i} | \'{linha}\' é ilegal!')
        except Exception as e:
            print(e)
            quit()
    print('Letras: ', lista_vars)
    # max_linhas = len(lista_vars)
    return lista_vars


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
# Função mestra
def matrificar(valor):
    # PASSO 1
    # Gera lista de letras únicas (variáveis)
    lista_var = sis_p_str(valor)
    # PASSO 2
    # Gera matriz usando como referência as letras
    col_cont = len(lista_var) + 1
    linha_cont = valor.count('\n') + 1
    # O '+ 1' é para considerar os elementos independentes nas colunas!
    matriz = [[0 for coluna in range(col_cont)] for linha in range(linha_cont)]
    # Agora adiciona valores das colunas de acordo com a ordem das variáveis
    # Para cada linha!
    # Usa a lista de valores para identificar variáveis para serem adicionadas
    for v_lin, linha_str in enumerate(valor.split('\n')):
        # Valor das variáveis numéricas na linha
        indie_p_soma = 0
        el_anterior = 0
        negativar_ = False
        negativar_inden_ = True
        for el in linha_str.split():
            if el == '=':
                negativar_ = True
                negativar_inden_ = False
            for v_col, var_type in enumerate(lista_var):
                val_p_soma = 1.0
                if var_type in el:
                    # 2 Casos (se houver número ou não!)
                    if any(char.isdigit() for char in el):
                        # Substring sem letras
                        clean_val = el
                        for char in el:
                            if char.isalpha():
                                clean_val = clean_val.replace(char, '')
                        # Transforma em número e soma
                        val_p_soma = float(clean_val)
                    else:
                        if '-' in el:
                            val_p_soma *= -1
                    # Verifica se é negativo por char anterior
                    if el_anterior == '-':
                        val_p_soma *= -1
                    # Se é negativo por posição
                    if negativar_:
                        val_p_soma *= -1

                    matriz[v_lin][v_col] += val_p_soma  # Tenho que decidir a operação certa, muito trabalho!!!

            # Adição de números
            # Procura elementos numéricos
            # Verifica se tem '-' no número ou se tem '-' antes do elemento
            el_aux = el
            negativo = False
            if '-' in el_aux:
                # Retira parte negativa
                el_aux = el_aux.replace('-', '')
                if len(el_aux) != 0:
                    negativo = True
            if el_aux.isnumeric():
                indie_p_soma += float(el_aux)
                if negativar_inden_:
                    indie_p_soma *= -1
                if negativo:
                    indie_p_soma *= -1
                if el_anterior == '-':
                    indie_p_soma *= -1
            # Muda o anterior
            el_anterior = el
        matriz[v_lin][col_cont - 1] = indie_p_soma  # Coloca os termos independentes

    return lista_var, matriz


def calcular(matriz):
    num_vars = len(matriz)
    for id_pivo in range(num_vars):  # id_pivo: Coordenadas transversais do pivô
        # Verifica se pivo == 0 'Para translocar linhas'
        pivo = matriz[id_pivo][id_pivo]
        if pivo == 0:
            continue  # Temporário

        # Divide linha pelo valor do pivo
        for id_val, _ in enumerate(matriz[id_pivo]):
            matriz[id_pivo][id_val] /= pivo

        # Elimina todos abaixo e acima do pivo (linha p/ linha)
        for id_linha, linha in enumerate(matriz):
            # Pula se for a linha atual
            if id_linha == id_pivo:
                continue

            # Soma correspondentes
            pseudo_linha = [el_+matriz[id_pivo][i_el]*(-linha[id_pivo])
                            for i_el, el_ in enumerate(linha)]
            matriz[id_linha] = pseudo_linha.copy()
        print(f"-- Passo {id_pivo} -- \nMatriz: {matriz}")
    return matriz


def resultar(matriz, variaveis):
    classific_id = POSS_DET
    classificacao = "Sistema não calculável."
    matriz_copy = []
    # Retira linhas zeradas (com termo independente == 0)!
    for id_termos_, termos_ in enumerate(matriz):
        if all(termos_el == 0 for termos_el in termos_):
            continue
        matriz_copy.append(termos_)
    matriz = matriz_copy
    print_matriz(matriz, "Pós tratamento: ")
    #
    # Verifica tipo do sistema!
    #
    conj_solucao = []
    sol_p_extenso = ""
    for linha in matriz:
        # Impossível
        if all(l_ == 0 for l_ in linha[:-1]):
            classific_id = IMPOSS
            break
        # Verifica se é indeterminado
        # Não dá break porque ainda pode ser impossível
        if linha.count(1.0) > 1:
            classific_id = POSS_INDET
    # Se não é impossível ou indeterminado só sobra determinado
    classificacao = descrever_s(matriz, conj_solucao, classific_id, variaveis)
    return classificacao


def diagonalizar(matriz):
    diagonal = []
    for i in range(len(matriz)):
        diagonal.append(matriz[i][i])
    return diagonal


def descrever_s(matriz, conj_s, tipo, variaveis):
    classificacao = "Sistema é possível"
    sol_p_extenso = " "
    num_linhas = len(matriz)
    match tipo:
        case 2:
            # Colocar numa função!
            # Possível e determinado (pela diagonal)
            diagonal_ = diagonalizar(matriz)
            if all(d_ == 1 for d_ in diagonal_):
                for id_l_ in range(num_linhas):
                    result = matriz[id_l_][-1]
                    conj_s.append(result)
                    # Criar função pra descrever o conjunto solução literalmente!
                    sol_p_extenso += str(f"{result:.3f}") + (", " if id_l_ != num_linhas - 1 else "")
            print("S = {" + sol_p_extenso + "}")
            classificacao += " e determinado."
        case 1:
            # Todos as 'primeiras' variáveis
            variaveis_ambulantes = variaveis[num_linhas :].copy()  # Aquelas que definem as outras
            print(variaveis_ambulantes)
            # Criar classe com sistemas?
            print("S = {" + sol_p_extenso + "}")
            classificacao += " e indeterminado."
        case 0:
            print("S = {" + sol_p_extenso + "}")
            classificacao = "Sistema impossível."
        case _:
            raise Exception ("Erro ao tentar descrever o conjunto S!")

    return classificacao


def print_matriz(matriz, titulo=""):
    print(titulo)
    for linha in matriz:
        print(linha)


# Inutil?
def pegar_col(matriz, i_col):
    coluna = []
    for linha in matriz:
        coluna.append(linha[i_col])
    return coluna
