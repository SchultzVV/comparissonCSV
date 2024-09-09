# old
import pandas as pd
import numpy as np

def load_dfs(file_path1, file_path2):
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    return df1, df2

# def load_and_print_shape(df1, df2):
    # df1 = pd.read_csv(file_path1)
    # df2 = pd.read_csv(file_path2)
def look_shapes_and_types(df1, df2):
    print(f"Shape of DataFrame 1: {df1.shape}")
    print(f"Columns of DataFrame 1: {df1.columns}")
    print(f"Shape of DataFrame 2: {df2.shape}")
    print(f"Columns of DataFrame 2: {df2.columns}")
    
    if df1.shape[0] != df2.shape[0]:
        print('ERRO !')
        print('DataFrames have different number of rows')
    if df1.shape[1] != df2.shape[1]:
        print('ERRO !')
        print('DataFrames have different number of columns')
    
    # Checar tipos de colunas diferentes
    z=[]
    for col in df1.columns:
        if col in df2.columns:
            dtype1 = df1[col].dtype
            dtype2 = df2[col].dtype
            if dtype1 != dtype2:
                z.append(col)
                print(f"Type mismatch in column '{col}':")
                print(f" - DataFrame 1: {dtype1}")
                print(f" - DataFrame 2: {dtype2}")            
        else:
            print(f"Column '{col}' is missing in DataFrame 2")
    if len(z) == 0:
        print('*'*50)
        print('All columns have the same data types')
        print('*'*50)
    for col in df2.columns:
        if col not in df1.columns:
            print(f"Column '{col}' is missing in DataFrame 1")
    
    # return df1, df2
# def load_and_print_shape(file_path1, file_path2):
#     df1 = pd.read_csv(file_path1)
#     df2 = pd.read_csv(file_path2)
#     print(f"Shape of DataFrame 1: {df1.shape}")
#     print(f"Shape of DataFrame 1: {df1.columns}")
#     print(f"Shape of DataFrame 2: {df2.shape}")
#     print(f"Shape of DataFrame 2: {df2.columns}")
#     if df1.shape[0] != df2.shape[0]:
#         print('ERRO !')
#         print('DataFrames have different number of rows')
#     if df1.shape[1] != df2.shape[1]:
#         print('ERRO !')
#         print('DataFrames have different number of columns')
#     return df1, df2

def print_markdown_table(df):
    # Mostra o cabeçalho da tabela
    header = "| " + " | ".join(df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(df.columns)) + " |"

    # Mostra as linhas do DataFrame
    rows = "\n".join(
        ["| " + " | ".join(map(str, row)) + " |" for row in df.values]
    )

    # Exibe o resultado em formato de tabela Markdown
    markdown_table = header + "\n" + separator + "\n" + rows
    print(markdown_table)

def compare_group_sizes(df1, df2, group_column='CD_PESS'):
    # Agrupando por 'group_column' e obtendo o tamanho dos grupos
    # group_df1 = df1.groupby(group_column).size().sort_values(ascending=False)
    # group_df2 = df2.groupby(group_column).size().sort_values(ascending=False)
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
        
    return result, diferente

def print_all(df1, df2):
    print('+'*50)
    print(' COMPARAÇÕES DE TAMANHO DOS GRUPOS ')
    print('+'*50)
    i = 0
    for col in df1.columns:
        r, d = compare_group_sizes(df1, df2, group_column=col)
        print(f' COLUNA : {col}')
        if d.shape[0] != 0:
            i+=1
            print(' ERRADO '*5)
            df1_group = df1.groupby(col).size().sort_values(ascending=False)#.isin(d.index)]
            df2_group = df2.groupby(col).size().sort_values(ascending=False)#.isin(d.index)]
            # print(f"Shape of DataFrame 1: {df1_group.shape}")
            # print(f"Shape of DataFrame 2: {df2_group.shape}")
            print(f' shape df1.{col} = {df1_group.shape[0]}')
            print(df1_group.head(5))
            print(f' shape df2.{col} = {df2_group.shape[0]}')
            print(df2_group.head(5))

            print('d.shape[0] = ', d.shape[0])
            print('diferences:')
            print(d.head(4))
            print_markdown_table(d)
            print('+'*50)
        # else:
            
            # print(' CERTO ')
            # print('r.shape[0] = ', r.shape[0])
            # print(r.head(5))
            # print('+'*50)
    if i == 0:
        print(' Tudo CERTO ')
    elif i != 0:
        print(' ERRADO '*5)
        print(f' Tem {len(df1.columns)} colunas e {i} contém diferenças')
def run_path(path1, path2):
    df1, df2 = load_dfs(path1, path2)
    print(df1.info())
    print(df2.info())
    print_all(df1, df2)
def run(df1, df2):
    print(df1.info())
    print(df2.info())
    print_all(df1, df2)

# def result_of_compare_column_elements(file_path1, file_path2, column_name):
def result_of_compare_column_elements(df1, df2, column_name):
    # Obter os valores únicos da coluna em ambos os DataFrames e arredondar para 8 casas decimais
    df1_elements = set(round(val, 5) for val in df1[column_name])
    df2_elements = set(round(val, 5) for val in df2[column_name])
    
    # Identificar os elementos que estão somente em df1 e somente em df2
    only_in_df1 = list(df1_elements - df2_elements)
    only_in_df2 = list(df2_elements - df1_elements)
    
    # Verificar se os tamanhos das listas são diferentes
    if len(only_in_df1) != len(only_in_df2):
        print(f"Tamanho de 'only_in_df1' {column_name}: {len(only_in_df1)}")
        print(f"Tamanho de 'only_in_df2' {column_name}: {len(only_in_df2)}")
        
        # Garantir que ambas as listas tenham o mesmo tamanho
        max_len = max(len(only_in_df1), len(only_in_df2))
        only_in_df1.extend([np.nan] * (max_len - len(only_in_df1)))
        only_in_df2.extend([np.nan] * (max_len - len(only_in_df2)))
    
    # Criar o DataFrame de resultado com duas colunas
    result_df = pd.DataFrame({
        f'Only_in_df1_{column_name}': only_in_df1,
        f'Only_in_df2_{column_name}': only_in_df2
    })
    
    return result_df


def compare_dataframes(df1, df2):
    import pdb; pdb.set_trace()
    # Verificar se ambos os DataFrames têm o mesmo número de linhas e colunas
    if df1.shape != df2.shape:
        print(f"ERRO! Os DataFrames têm tamanhos diferentes: {df1.shape} vs {df2.shape}")
        return None

    # Verificar se ambos os DataFrames têm as mesmas colunas na mesma ordem
    if not df1.columns.equals(df2.columns):
        print("ERRO! Os DataFrames têm colunas diferentes ou em ordens diferentes.")
        return None

    # Verificar a igualdade dos valores em cada célula
    comparison = df1.equals(df2)

    if comparison:
        print("Os DataFrames são iguais em todos os valores.")
    else:
        print("Diferenças encontradas:")
        # Localizar e imprimir as diferenças
        differences = df1.ne(df2)
        diff_locations = differences.stack()[differences.stack()]
        for index, value in diff_locations.items():
            print(f"Diferença encontrada em {index}: df1={df1.loc[index]}, df2={df2.loc[index]}")

    return comparison

# path1 = 'comparacoes/df_geral_s23.csv'
# path2 = 'comparacoes/df_geral_s23.csv'
# df1, df2 = load_and_print_shape(path1, path2)