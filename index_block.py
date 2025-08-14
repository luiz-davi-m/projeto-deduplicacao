"""
Indexação e blocagem para ligação de registros usando a biblioteca recordlinkage.
Este script carrega um conjunto de dados, realiza a blocagem para encontrar pares candidatos
e salva os resultados em um arquivo CSV.
"""

import pandas as pd
import recordlinkage
import os

input_path = 'datasets/compas_l1_preproc.csv'
output_pares_path = 'datasets/pares_blocagem_l1.csv'

# Carrega a base inteira
df = pd.read_csv(input_path)

print(f"Total de registros carregados: {len(df)}")

# Indexação - blocagem usando 'blocking_key'
indexer = recordlinkage.Index()
indexer.block('blocking_key')
candidate_links = indexer.index(df)

print(f"Pares candidatos encontrados: {len(candidate_links)}")

# Monta um DataFrame com dados dos pares para facilitar a análise e salvar no CSV
pairs_data = []

for idx1, idx2 in candidate_links:
    row1 = df.loc[idx1]
    row2 = df.loc[idx2]
    pairs_data.append({
        # Índices originais
        "idx1": idx1,
        "idx2": idx2,
        # Dados do registro 1
        "Person_ID_1": row1['Person_ID'],
        "FirstName_1": row1['FirstName'],
        "LastName_1": row1['LastName'],
        "DateOfBirth_1": row1['DateOfBirth'],
        "blocking_key": row1['blocking_key'],
        # Dados do registro 2
        "Person_ID_2": row2['Person_ID'],
        "FirstName_2": row2['FirstName'],
        "LastName_2": row2['LastName'],
        "DateOfBirth_2": row2['DateOfBirth'],
    })

pares_df = pd.DataFrame(pairs_data)

#Salva o resultado em CSV
os.makedirs('datasets', exist_ok=True)
pares_df.to_csv(output_pares_path, index=False)
print(f"Arquivo de pares candidatos salvo em: {output_pares_path}")
print("Exemplo das primeiras linhas:")
print(pares_df.head())
