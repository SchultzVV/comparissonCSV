def compare_group_sizes_and_rows(df1, df2, group_column='CD_PESS'):
    # Ordenando os DataFrames por group_column antes de comparar
    df1_sorted = df1.sort_values(by=group_column).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=group_column).reset_index(drop=True)

    # Comparando se as linhas (após ordenação) são iguais
    rows_equal = df1_sorted.equals(df2_sorted)

    # Agrupando por 'group_column' e obtendo o tamanho dos grupos
    group_df1 = df1.round({group_column: 7}).groupby(group_column).size().sort_values(ascending=False)
    group_df2 = df2.round({group_column: 7}).groupby(group_column).size().sort_values(ascending=False)

    # Criando um DataFrame para armazenar as colunas
    result = pd.DataFrame({
        'df1_size': group_df1,
        'df2_size': group_df2
    })

    # Preenchendo valores ausentes com 0 (caso um código exista em apenas um dos DataFrames)
    result = result.fillna(0)

    # Adicionando uma coluna com a subtração dos tamanhos
    result['size_difference'] = result['df1_size'] - result['df2_size']
    diferente = result[result['size_difference'] != 0]

    return result, diferente, rows_equal

def print_all_with_row_comparison(df1, df2):
    print('+'*50)
    print(' COMPARAÇÕES DE TAMANHO DOS GRUPOS E LINHAS ')
    print('+'*50)
    i = 0
    for col in df1.columns:
        r, d, rows_equal = compare_group_sizes_and_rows(df1, df2, group_column=col)
        print(f' COLUNA : {col}')
        if d.shape[0] != 0:
            i += 1
            print(' ERRADO '*5)
            df1_group = df1.groupby(col).size().sort_values(ascending=False)
            df2_group = df2.groupby(col).size().sort_values(ascending=False)
            print(f' shape df1.{col} = {df1_group.shape[0]}')
            print(df1_group.head(5))
            print(f' shape df2.{col} = {df2_group.shape[0]}')
            print(df2_group.head(5))

            print('d.shape[0] = ', d.shape[0])
            print('diferences:')
            print(d.head(4))
            print(d.tail(4))
            print('+'*50)
        else:
            print(' CERTO ')
            print('r.shape[0] = ', r.shape[0])
            print(r.head(5))
            print('+'*50)

        # Comparando as linhas
        if not rows_equal:
            print(' ERRADO NA ORDEM DAS LINHAS ')
        else:
            print(' LINHAS ESTÃO CORRETAS ')

    if i == 0:
        print(' Tudo CERTO ')
    elif i != 0:
        print(' ERRADO '*5)
        print(f' Tem {len(df1.columns)} colunas e {i} contém diferenças')

def compare_rows_by_key(df1, df2, key_column='CD_PTOV'):
    # Definir a chave como índice para os dois DataFrames
    df1_keyed = df1.set_index(key_column)
    df2_keyed = df2.set_index(key_column)
    
    # Identificar chaves comuns e chaves que faltam em um dos DataFrames
    common_keys = df1_keyed.index.intersection(df2_keyed.index)
    missing_in_df1 = df2_keyed.index.difference(df1_keyed.index)
    missing_in_df2 = df1_keyed.index.difference(df2_keyed.index)
    
    # Comparar as linhas para as chaves comuns
    differences = []
    for key in common_keys:
        row_df1 = df1_keyed.loc[key]
        row_df2 = df2_keyed.loc[key]
        if not row_df1.equals(row_df2):
            differences.append((key, row_df1, row_df2))
    
    return common_keys, missing_in_df1, missing_in_df2, differences

def print_comparison_by_key(df1, df2, key_column='CD_PTOV'):
    print('+'*50)
    print(f'COMPARAÇÃO BASEADA NA CHAVE: {key_column}')
    print('+'*50)

    common_keys, missing_in_df1, missing_in_df2, differences = compare_rows_by_key(df1, df2, key_column)

    if missing_in_df1.empty and missing_in_df2.empty and len(differences) == 0:
        print('Tudo CERTO: As chaves e os dados correspondem entre os DataFrames.')
    else:
        if not missing_in_df1.empty:
            print('FALTANDO FALTANDO Faltando no df1:')
            print(missing_in_df1)
            
        if not missing_in_df2.empty:
            print('FALTANDO FALTANDO Faltando no df2:')
            print(missing_in_df2)
        if differences:
            print('DIFERENÇAS ENCONTRADAS DIFERENÇAS ENCONTRADAS:')
            for key, row_df1, row_df2 in differences:
                print(f'Chave: {key}')
                print(f'Dados no df1: \n{row_df1}')
                print(f'Dados no df2: \n{row_df2}')
                print('-'*50)

def compare_rows_by_key_old(df1, df2, key_column='CD_PTOV'):
    # Definir a chave como índice para os dois DataFrames
    df1_keyed = df1.set_index(key_column)
    df2_keyed = df2.set_index(key_column)
    
    # Identificar chaves comuns e chaves que faltam em um dos DataFrames
    common_keys = df1_keyed.index.intersection(df2_keyed.index)
    missing_in_df1 = df2_keyed.index.difference(df1_keyed.index)
    missing_in_df2 = df1_keyed.index.difference(df2_keyed.index)
    
    # Comparar as linhas para as chaves comuns
    differences = []
    for key in common_keys:
        row_df1 = df1_keyed.loc[key]
        row_df2 = df2_keyed.loc[key]
        if not row_df1.equals(row_df2):
            differences.append((key, row_df1, row_df2))
    
    return common_keys, missing_in_df1, missing_in_df2, differences

def write_comparison_to_file_old(df1, df2, key_column='CD_PTOV', file_name='comparison_output.txt'):
    with open(file_name, 'w') as file:
        file.write('+'*50 + '\n')
        file.write(f'COMPARAÇÃO BASEADA NA CHAVE: {key_column}\n')
        file.write('+'*50 + '\n')

        common_keys, missing_in_df1, missing_in_df2, differences = compare_rows_by_key_old(df1, df2, key_column)

        if missing_in_df1.empty and missing_in_df2.empty and len(differences) == 0:
            file.write('Tudo CERTO: As chaves e os dados correspondem entre os DataFrames.\n')
        else:
            if not missing_in_df1.empty:
                file.write('Faltando no df1:\n')
                file.write(missing_in_df1.to_string() + '\n')
            if not missing_in_df2.empty:
                file.write('Faltando no df2:\n')
                file.write(missing_in_df2.to_string() + '\n')
            if differences:
                file.write('Diferenças encontradas:\n')
                for key, row_df1, row_df2 in differences:
                    file.write(f'Chave: {key}\n')
                    file.write('Dados no df1:\n')
                    file.write(row_df1.to_string() + '\n')
                    file.write('Dados no df2:\n')
                    file.write(row_df2.to_string() + '\n')
                    file.write('-'*50 + '\n')

def compare_rows_by_key(df1, df2, key_column='CD_PTOV'):
    # Definir a chave como índice para os dois DataFrames
    df1_keyed = df1.set_index(key_column)
    df2_keyed = df2.set_index(key_column)
    
    # Identificar chaves comuns e chaves que faltam em um dos DataFrames
    common_keys = df1_keyed.index.intersection(df2_keyed.index)
    missing_in_df1 = df2_keyed.index.difference(df1_keyed.index)
    missing_in_df2 = df1_keyed.index.difference(df2_keyed.index)
    
    # Comparar as linhas para as chaves comuns
    differences = []
    for key in common_keys:
        row_df1 = df1_keyed.loc[key]
        row_df2 = df2_keyed.loc[key]
        if not row_df1.equals(row_df2):
            differences.append((key, row_df1, row_df2))
    
    return common_keys, missing_in_df1, missing_in_df2, differences
def write_comparison_to_file(df1, df2, key_column='CD_PTOV', file_name='comparison_output.txt'):
    with open(file_name, 'w') as file:
        file.write(f'COMPARAÇÃO BASEADA NA CHAVE: {key_column}\n')
        file.write(f'Chave;Coluna;Valor_df1;Valor_df2\n')  # Cabeçalho para o arquivo CSV-like

        common_keys, missing_in_df1, missing_in_df2, differences = compare_rows_by_key(df1, df2, key_column)

        if missing_in_df1.empty and missing_in_df2.empty and len(differences) == 0:
            file.write('Tudo CERTO: As chaves e os dados correspondem entre os DataFrames.\n')
        else:
            if not missing_in_df1.empty:
                file.write(f'Faltando no df1 (Presentes no df2): {",".join(missing_in_df1)}\n')
            if not missing_in_df2.empty:
                file.write(f'Faltando no df2 (Presentes no df1): {",".join(missing_in_df2)}\n')
            
            if differences:
                # Escrevendo diferenças em formato tabular (CSV-like)
                for key, row_df1, row_df2 in differences:
                    for column in row_df1.index:  # Iterar sobre as colunas
                        val_df1 = row_df1[column]
                        val_df2 = row_df2[column]
                        if val_df1 != val_df2:
                            file.write(f'{key};{column};{val_df1};{val_df2}\n')

def df_de_duplicados(df, col):
    df_dup_check = df.groupby(col).size().reset_index(name='count')
    df_dup_check = df_dup_check[df_dup_check['count'] > 1]
    return df_dup_check