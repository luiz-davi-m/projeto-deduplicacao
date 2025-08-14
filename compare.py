"""
Este script carrega um conjunto de dados, compara pares de registros e salva os resultados em um arquivo CSV.
"""
import pandas as pd
import os
import jellyfish

input_base_path = 'datasets/compas_l1_preproc.csv'
input_pares_path = 'datasets/pares_blocagem_l1.csv'
output_comparacao_path = 'datasets/comparacao_blocagem_l1.csv'

# Carrega a base principal
df = pd.read_csv(input_base_path).reset_index(drop=True)

# Carrega pares e garante que índices são INT
pares_df = pd.read_csv(input_pares_path)
pares_df['idx1'] = pares_df['idx1'].astype(int)
pares_df['idx2'] = pares_df['idx2'].astype(int)

print(f"Total de pares a comparar: {len(pares_df)}")
print(f"Total de registros na base: {len(df)}")

# Preencher dados dos pares lado a lado
res = pares_df.copy()
for col in ['FirstName', 'LastName', 'DateOfBirth']:
    res[col + '_1'] = df.loc[res['idx1'], col].values
    res[col + '_2'] = df.loc[res['idx2'], col].values

# Função de similaridade Jaro-Winkler usando rapidfuzz
def jw_sim(a, b):
    if pd.isnull(a) or pd.isnull(b):
        return 0.0
    try:
        return jellyfish.jaro_winkler(str(a), str(b))
    except Exception:
        return 0.0
    
# Calcular os scores
res['FirstName_sim'] = [jw_sim(a, b) for a, b in zip(res['FirstName_1'], res['FirstName_2'])]
res['LastName_sim'] = [jw_sim(a, b) for a, b in zip(res['LastName_1'], res['LastName_2'])]
res['DateOfBirth_eq'] = (res['DateOfBirth_1'] == res['DateOfBirth_2']).astype(int)

# Salvar resultados
os.makedirs('datasets', exist_ok=True)
res.to_csv(output_comparacao_path, index=False)
print(f"\nArquivo de comparação salvo em: {output_comparacao_path}\n")
print(res.head(10))
