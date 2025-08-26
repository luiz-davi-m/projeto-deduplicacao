"""
Indexação e blocagem para ligação de registros na base CORA usando recordlinkage.
Carrega o arquivo cora_preproc.csv, realiza a blocagem para encontrar pares candidatos,
e salva o resultado em coda/datasets/pares_blocagem_cora.csv.
"""

import pandas as pd
import recordlinkage
import os

# Caminhos
input_path = 'datasets/cora_preproc.csv'
output_pares_path = 'datasets/pares_blocagem_cora.csv'

# Confere se o arquivo existe
if not os.path.exists(input_path):
    print(f"Arquivo {input_path} não encontrado, encerrando...")
else:
    # Carrega o DataFrame
    df = pd.read_csv(input_path)
    print(f"\nProcessando {input_path}: {len(df)} registros...")

    # Indexação/blocagem usando blocking_key
    indexer = recordlinkage.Index()
    indexer.block('blocking_key')
    candidate_links = indexer.index(df)
    print(f"Pares candidatos encontrados: {len(candidate_links)}")

    # Monta DataFrame de pares
    pairs_data = []
    for idx1, idx2 in candidate_links:
        row1 = df.loc[idx1]
        row2 = df.loc[idx2]
        pairs_data.append({
            "idx1": idx1,
            "idx2": idx2,
            # Registro 1
            "id_1": row1['id'],
            "authors_1": row1['authors'],
            "title_1": row1['title'],
            "venue_name_1": row1['venue_name'],
            "venue_vol_1": row1['venue_vol'],
            "venue_date_1": row1['venue_date'],
            "blocking_key_1": row1['blocking_key'],
            # Registro 2
            "id_2": row2['id'],
            "authors_2": row2['authors'],
            "title_2": row2['title'],
            "venue_name_2": row2['venue_name'],
            "venue_vol_2": row2['venue_vol'],
            "venue_date_2": row2['venue_date'],
            "blocking_key_2": row2['blocking_key'],
        })
    pares_df = pd.DataFrame(pairs_data)

    # Salva CSV de pares de blocagem
    os.makedirs('cora/datasets', exist_ok=True)
    pares_df.to_csv(output_pares_path, index=False)
    print(f"Arquivo de pares candidatos salvo em: {output_pares_path}")
    print(pares_df.head())

print("\nProcessamento finalizado para a base CORA.")
