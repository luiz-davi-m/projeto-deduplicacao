import pandas as pd
import random
import os

# Caminhos
CAMINHO_ORIGINAL = "datasets/compas-scores-raw.csv"
CAMINHO_SAIDA = "datasets/"

# Colunas onde os ruídos são inseridos
COLUNAS_RUIDO = ["FirstName", "LastName", "DateOfBirth"]
PROBABILIDADE_RUIDO = 0.3

# --- Funções de ruído individuais ---
def substituir_caractere_texto(s):
    if pd.isna(s) or len(s) < 2:
        return s
    i = random.randint(0, len(s) - 1)
    c = random.choice("abcdefghijklmnopqrstuvwxyz")
    return s[:i] + c + s[i + 1:]

def substituir_digito_data(s):
    if pd.isna(s) or not any(ch.isdigit() for ch in str(s)):
        return s
    s = list(str(s))
    indices_digitos = [i for i, ch in enumerate(s) if ch.isdigit()]
    if not indices_digitos:
        return s
    idx = random.choice(indices_digitos)
    s[idx] = str(random.randint(0, 9))
    return "".join(s)

def truncar_string(s):
    if pd.isna(s) or len(s) < 4:
        return s
    i = random.randint(1, len(s) - 1)
    return s[:i]

# --- Funções de aplicação de ruído por nível ---
def aplicar_ruido_l2(df):
    df_mod = df.copy()
    for col in COLUNAS_RUIDO:
        if col == "DateOfBirth":
            df_mod[col] = df_mod[col].apply(lambda x: substituir_digito_data(x) if random.random() < PROBABILIDADE_RUIDO else x)
        else:
            df_mod[col] = df_mod[col].apply(lambda x: substituir_caractere_texto(str(x)) if random.random() < PROBABILIDADE_RUIDO else x)
    return df_mod

def aplicar_ruido_l3(df):
    df_mod = df.copy()
    for col in COLUNAS_RUIDO:
        if col == "DateOfBirth":
            df_mod[col] = df_mod[col].apply(lambda x: substituir_digito_data(x) if random.random() < PROBABILIDADE_RUIDO else x)
        else:
            df_mod[col] = df_mod[col].apply(lambda x: truncar_string(substituir_caractere_texto(str(x))) if random.random() < PROBABILIDADE_RUIDO else x)
    return df_mod

def main():
    print("Gerando bases com ruído...")
    df = pd.read_csv(CAMINHO_ORIGINAL)

    os.makedirs(CAMINHO_SAIDA, exist_ok=True)

    # compas_l1: apenas cópia
    df.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l1.csv"), index=False)

    # compas_l2: substituição
    df_l2 = aplicar_ruido_l2(df)
    df_l2.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l2.csv"), index=False)

    # compas_l3: substituição + truncamento (exceto datas)
    df_l3 = aplicar_ruido_l3(df)
    df_l3.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l3.csv"), index=False)

    print("Geração de bases com ruído finalizadas com sucesso.")

if __name__ == "__main__":
    main()
