import os
import pandas as pd
from unidecode import unidecode
import re
import recordlinkage.preprocessing as rl_pre

# Diretórios
input_path = 'datasets/'
output_path = 'datasets/'

# Arquivo de entrada
coraDataSetPath = 'cora.csv'

# Função para normalizar texto
def normalizar_texto(s):
    if pd.isna(s):
        return None
    return unidecode(str(s).strip().lower())

# Função para padronizar data apenas pelo ano
def padronizar_data(d):
    if pd.isna(d):
        return None
    d = str(d).strip()
    match = re.search(r"(19|20)\d{2}", d)
    if match:
        return match.group(0)
    return None

# Função para gerar chave de blocagem usando Soundex
def gerar_chave_soundex(row):
    if pd.isna(row['title']) or pd.isna(row['authors']) or pd.isna(row['venue_date']):
        return None
    ano = row['venue_date']
    title_code = rl_pre.phonetic(pd.Series([row['title']]), method='soundex').iloc[0]
    authors_code = rl_pre.phonetic(pd.Series([row['authors']]), method='soundex').iloc[0]
    return f"{title_code}{authors_code}{ano}"

# Leitura do arquivo
df = pd.read_csv(os.path.join(input_path, coraDataSetPath))

# Normalização dos textos
for col in ['title', 'authors']:
    df[col] = df[col].apply(normalizar_texto)

# Padronização de datas
df['venue_date'] = df['venue_date'].apply(padronizar_data)

# Geração da chave de blocagem Soundex
df['blocking_key'] = df.apply(gerar_chave_soundex, axis=1)

# Contagem de registros sem chave
sem_chave = df['blocking_key'].isna().sum()
print(f"{coraDataSetPath}: {sem_chave} registros sem chave de blocagem")

# Salvando arquivo processado
nome_saida = coraDataSetPath.replace('.csv', '_preproc.csv')
df.to_csv(os.path.join(output_path, nome_saida), index=False)
print(f"Arquivo salvo: {nome_saida}")
