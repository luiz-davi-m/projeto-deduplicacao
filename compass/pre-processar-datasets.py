import os
import pandas as pd
from unidecode import unidecode
from datetime import datetime
import recordlinkage.preprocessing as rl_pre

# Diretórios
input_path = 'datasets/'
output_path = 'datasets/'
arquivos = ['compas_l1.csv', 'compas_l2.csv', 'compas_l3.csv']

# Função para normalizar texto
def normalizar_texto(s):
    if pd.isna(s):
        return None
    return unidecode(str(s).strip().lower())

# Função para extrair apenas o ano da data
def extrair_ano(d):
    if pd.isna(d):
        return None
    try:
        # Tenta converter para datetime, serve para formatos tipo 'MM/DD/YYYY', 'YYYY-MM-DD', etc.
        data = pd.to_datetime(d, errors='coerce')
        if pd.isna(data):
            return None
        return str(data.year)
    except:
        return None

# Função para gerar chave de blocagem usando Soundex completo
def gerar_chave_soundex(row):
    if pd.isna(row['FirstName']) or pd.isna(row['LastName']) or pd.isna(row['DateOfBirth']):
        return None
    primeiro_code = rl_pre.phonetic(pd.Series([row['FirstName']]), method='soundex').iloc[0]
    sobrenome_code = rl_pre.phonetic(pd.Series([row['LastName']]), method='soundex').iloc[0]
    ano = extrair_ano(row['DateOfBirth'])
    if not ano:
        return None
    return f"{primeiro_code}{sobrenome_code}{ano}"

for arquivo in arquivos:
    df = pd.read_csv(os.path.join(input_path, arquivo))

    # Normalização dos nomes
    for col in ['FirstName', 'LastName']:
        df[col] = df[col].apply(normalizar_texto)

    # Extração do ano de nascimento
    df['DateOfBirth'] = df['DateOfBirth'].apply(lambda x: extrair_ano(x))

    # Geração da chave de blocagem Soundex
    df['blocking_key'] = df.apply(gerar_chave_soundex, axis=1)

    # Contagem de registros sem chave
    sem_chave = df['blocking_key'].isna().sum()
    print(f"{arquivo}: {sem_chave} registros sem chave de blocagem")

    # Salvando arquivo processado
    nome_saida = arquivo.replace('.csv', '_preproc.csv')
    df.to_csv(os.path.join(output_path, nome_saida), index=False)
    print(f"Arquivo salvo: {nome_saida}")
