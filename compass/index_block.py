"""
Indexação e blocagem para ligação de registros usando a biblioteca recordlinkage.
O script carrega todos os conjuntos de dados (L1, L2 e L3), realiza a blocagem para encontrar pares candidatos
e salva os resultados em arquivos CSV separados para cada base.
"""

import pandas as pd
import recordlinkage
import os

# Listas de níveis e seus respectivos arquivos
levels = [1, 2, 3]

for lvl in levels:
    input_path = f'compass/datasets/compas_l{lvl}_preproc.csv'
    output_pares_path = f'compass/datasets/pares_blocagem_l{lvl}.csv'

    # Checagem se o arquivo existe para evitar erros em ambientes em que nem todos os arquivos estejam prontos
    if not os.path.exists(input_path):
        print(f"Arquivo {input_path} não encontrado, pulando...")
        continue

    # Carrega a base inteira
    df = pd.read_csv(input_path)
    print(f"\nProcessando compas_l{lvl}_preproc.csv: {len(df)} registros...")

    # Indexação - blocagem usando 'blocking_key'
    indexer = recordlinkage.Index()
    indexer.block('blocking_key')
    candidate_links = indexer.index(df)
    print(f"Pares candidatos encontrados em L{lvl}: {len(candidate_links)}")

    # Monta o DataFrame com dados dos pares
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
            "blocking_key_1": row1['blocking_key'],
            # Dados do registro 2
            "Person_ID_2": row2['Person_ID'],
            "FirstName_2": row2['FirstName'],
            "LastName_2": row2['LastName'],
            "DateOfBirth_2": row2['DateOfBirth'],
            "blocking_key_2": row2['blocking_key'],
        })

    pares_df = pd.DataFrame(pairs_data)

    # Salva o resultado em CSV
    os.makedirs('compass/datasets', exist_ok=True)
    pares_df.to_csv(output_pares_path, index=False)
    print(f"Arquivo de pares candidatos salvo em: {output_pares_path}")
    print(pares_df.head())

print("\nProcessamento finalizado para todas as bases.")
