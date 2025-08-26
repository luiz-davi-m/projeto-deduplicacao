"""
Comparação de pares de registros para ligação/deduplicação na base CORA.
Carrega os arquivos de blocagem (pares_blocagem_cora.csv) e da base processada (cora_preproc.csv),
calcula similaridade entre campos dos pares e salva o resultado.
"""

import pandas as pd
import os
import jellyfish

# Função de similaridade Jaro-Winkler usando jellyfish
def jw_sim(a, b):
    if pd.isnull(a) or pd.isnull(b):
        return 0.0
    try:
        return jellyfish.jaro_winkler_similarity(str(a), str(b))
    except Exception:
        return 0.0

# Caminhos de entrada e saída
input_base_path = 'datasets/cora_preproc.csv'
input_pares_path = 'datasets/pares_blocagem_cora.csv'
output_comparacao_path = 'datasets/comparacao_blocagem_cora.csv'

# Valida arquivos
if not os.path.exists(input_base_path) or not os.path.exists(input_pares_path):
    print(f"Arquivo {input_base_path} ou {input_pares_path} não encontrado, encerrando...")
else:
    print(f"\nProcessando comparação para CORA...")
    # Carrega base e pares
    df = pd.read_csv(input_base_path).reset_index(drop=True)
    pares_df = pd.read_csv(input_pares_path)
    pares_df['idx1'] = pares_df['idx1'].astype(int)
    pares_df['idx2'] = pares_df['idx2'].astype(int)
    print(f"Total de pares a comparar: {len(pares_df)}")
    print(f"Total de registros na base: {len(df)}")

    # Preenche dados dos pares lado a lado
    res = pares_df.copy()
    for col in ['authors', 'title', 'venue_name', 'venue_vol', 'venue_date', 'blocking_key']:
        res[f'{col}_1'] = df.loc[res['idx1'], col].values
        res[f'{col}_2'] = df.loc[res['idx2'], col].values

    # Calcula similaridade de autores e título (Jaro-Winkler)
    res['authors_sim'] = [jw_sim(a, b) for a, b in zip(res['authors_1'], res['authors_2'])]
    res['title_sim'] = [jw_sim(a, b) for a, b in zip(res['title_1'], res['title_2'])]

    # Comparação exata de venue_date (ano da publicação)
    res['venue_date_eq'] = (res['venue_date_1'] == res['venue_date_2']).astype(int)

    # Salva resultados
    os.makedirs('datasets', exist_ok=True)
    res.to_csv(output_comparacao_path, index=False)
    print(f"Arquivo de comparação salvo em: {output_comparacao_path}")
    print(res.head(5))

print("\nComparação finalizada para a base CORA.")
