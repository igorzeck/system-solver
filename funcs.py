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
                            if ema not in lista_letras:
                                lista_letras.append(ema)
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
    print('Letras: ', lista_letras)
    # max_linhas = len(lista_letras)
    return lista_letras


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
def matrificar(valor, matriz):
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
        for el in linha_str.split():
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

                    matriz[v_lin][v_col] += val_p_soma  # Tenho que decidir a operação certa, muito trabalho!!!

            # Adição de números
            # Procura elementos numéricos
            # Verifica se tem '-' no número
            el_aux = el
            negativo = False
            if '-' in el_aux:
                # Retira parte negativa
                el_aux = el_aux.replace('-', '')
                negativo = True
            if el_aux.isnumeric():
                indie_p_soma += float(el_aux)
            if negativo:
                indie_p_soma *= -1

        matriz[v_lin][col_cont - 1] = indie_p_soma # Coloca os termos independentes


    for linha in matriz:
        print(linha)
