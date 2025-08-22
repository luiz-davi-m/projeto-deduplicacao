import os
import pandas as pd
from unidecode import unidecode
from datetime import datetime
import recordlinkage.preprocessing as rl_pre

# Diretórios
input_path = 'datasets/'
output_path = 'datasets/'

# Arquivos de entrada
arquivos = ['compas_l1.csv', 'compas_l2.csv', 'compas_l3.csv']

# Função para normalizar texto
def normalizar_texto(s):
    if pd.isna(s):
        return None
    return unidecode(str(s).strip().lower())

# Função para padronizar data válida (YYYY-MM-DD)
def padronizar_data(d):
    if pd.isna(d):
        return None
    d = str(d).strip()
    try:
        # Se ano tem 2 dígitos, assume século passado
        if len(d.split('/')[-1]) == 2:
            data = datetime.strptime(d, "%m/%d/%y").replace(year=1900 + int(d.split('/')[-1]))
        else:
            data = pd.to_datetime(d, errors='coerce')
        return data.strftime('%Y-%m-%d') if pd.notna(data) else None
    except:
        return None


# Função para gerar chave de blocagem usando Soundex
def gerar_chave(row):
    if pd.isna(row['FirstName']) or pd.isna(row['LastName']) or pd.isna(row['DateOfBirth']):
        return None

    # rl_pre.phonetic precisa de uma Series
    primeiro_soundex = rl_pre.phonetic(pd.Series([row['FirstName']]), method='soundex').iloc[0][:2]
    sobrenome_soundex = rl_pre.phonetic(pd.Series([row['LastName']]), method='soundex').iloc[0][:2]

    try:
        ano = str(pd.to_datetime(row['DateOfBirth']).year)
    except:
        return None

    return f"{primeiro_soundex}{sobrenome_soundex}{ano}"

for arquivo in arquivos:
    df = pd.read_csv(os.path.join(input_path, arquivo))

    # Normalização de colunas textuais
    for col in ['FirstName', 'LastName']:
        df[col] = df[col].apply(normalizar_texto)

    # Padronização de datas
    df['DateOfBirth'] = df['DateOfBirth'].apply(padronizar_data)

    # Geração da chave de blocagem
    df['blocking_key'] = df.apply(gerar_chave, axis=1)

    # Contagem de registros sem chave
    sem_chave = df['blocking_key'].isna().sum()
    print(f"{arquivo}: {sem_chave} registros sem chave de blocagem")

    # Salvando arquivo processado
    nome_saida = arquivo.replace('.csv', '_preproc.csv')
    df.to_csv(os.path.join(output_path, nome_saida), index=False)
    print(f"Arquivo salvo: {nome_saida}")
