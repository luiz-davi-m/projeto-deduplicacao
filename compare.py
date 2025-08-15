"""
Comparação de pares de registros para ligação/deduplicação.
Este script carrega os arquivos de blocagem de vários níveis (L1, L2, L3),
calcula similaridade entre campos dos pares e salva os resultados em arquivos separados.
"""
import pandas as pd
import os
import jellyfish

# Lista dos níveis para processar
levels = [1, 2, 3]

# Função de similaridade Jaro-Winkler usando jellyfish
def jw_sim(a, b):
    if pd.isnull(a) or pd.isnull(b):
        return 0.0
    try:
        return jellyfish.jaro_winkler_similarity(str(a), str(b))
    except Exception:
        return 0.0

for lvl in levels:
    input_base_path = f'datasets/compas_l{lvl}_preproc.csv'
    input_pares_path = f'datasets/pares_blocagem_l{lvl}.csv'
    output_comparacao_path = f'datasets/comparacao_blocagem_l{lvl}.csv'
    
    # Checa a existência dos arquivos para não quebrar
    if not os.path.exists(input_base_path) or not os.path.exists(input_pares_path):
        print(f"Arquivo compas_l{lvl}_preproc.csv ou pares_blocagem_l{lvl}.csv não encontrado, pulando L{lvl}...")
        continue

    print(f"\nProcessando comparação para L{lvl}...")
    
    # Carrega a base principal
    df = pd.read_csv(input_base_path).reset_index(drop=True)
    
    # Carrega pares
    pares_df = pd.read_csv(input_pares_path)
    pares_df['idx1'] = pares_df['idx1'].astype(int)
    pares_df['idx2'] = pares_df['idx2'].astype(int)

    print(f"Total de pares a comparar em L{lvl}: {len(pares_df)}")
    print(f"Total de registros na base: {len(df)}")

    # Preenche dados dos pares lado a lado
    res = pares_df.copy()
    for col in ['FirstName', 'LastName', 'DateOfBirth', 'blocking_key']:
        res[f'{col}_1'] = df.loc[res['idx1'], col].values
        res[f'{col}_2'] = df.loc[res['idx2'], col].values

    # Calcula similaridade de nomes
    res['FirstName_sim'] = [jw_sim(a, b) for a, b in zip(res['FirstName_1'], res['FirstName_2'])]
    res['LastName_sim'] = [jw_sim(a, b) for a, b in zip(res['LastName_1'], res['LastName_2'])]
    
    # Data de nascimento - igualdade exata
    res['DateOfBirth_eq'] = (res['DateOfBirth_1'] == res['DateOfBirth_2']).astype(int)

    # Salva resultados
    os.makedirs('datasets', exist_ok=True)
    res.to_csv(output_comparacao_path, index=False)
    print(f"Arquivo de comparação salvo em: {output_comparacao_path}")
    print(res.head(5))

print("\nComparação finalizada para todas as bases.")
