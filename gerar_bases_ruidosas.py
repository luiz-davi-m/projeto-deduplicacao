import pandas as pd
import random
import os

# Caminhos
CAMINHO_ORIGINAL = "datasets/compas-scores-raw.csv"
CAMINHO_SAIDA = "datasets/"

# Colunas-alvo para ruído
COLUNAS_RUIDO = ["FirstName", "LastName", "DateOfBirth"]
PROBABILIDADE_RUIDO = 0.3  # 30% dos registros

# --- Funções de ruído individuais ---
def substituir_caractere(s):
    if pd.isna(s) or len(s) < 2:
        return s
    i = random.randint(0, len(s) - 1)
    c = random.choice("abcdefghijklmnopqrstuvwxyz")
    return s[:i] + c + s[i + 1:]

def truncar_string(s):
    if pd.isna(s) or len(s) < 4:
        return s
    i = random.randint(1, len(s) - 1)
    return s[:i]

# --- Funções de aplicação de ruído por nível ---
def aplicar_ruido_l2(df):
    df_mod = df.copy()
    for col in COLUNAS_RUIDO:
        df_mod[col] = df_mod[col].apply(lambda x: substituir_caractere(str(x)) if random.random() < PROBABILIDADE_RUIDO else x)
    return df_mod

def aplicar_ruido_l3(df):
    df_mod = df.copy()
    for col in COLUNAS_RUIDO:
        df_mod[col] = df_mod[col].apply(lambda x: truncar_string(substituir_caractere(str(x))) if random.random() < PROBABILIDADE_RUIDO else x)
    return df_mod

# --- Execução principal ---
def main():
    # Carrega base original
    df = pd.read_csv(CAMINHO_ORIGINAL)

    # Garante que diretório de saída exista
    os.makedirs(CAMINHO_SAIDA, exist_ok=True)

    # compas_l1: sem ruído
    df.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l1.csv"), index=False)

    # compas_l2: substituição de caracteres
    df_l2 = aplicar_ruido_l2(df)
    df_l2.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l2.csv"), index=False)

    # compas_l3: substituição + truncamento
    df_l3 = aplicar_ruido_l3(df)
    df_l3.to_csv(os.path.join(CAMINHO_SAIDA, "compas_l3.csv"), index=False)

    print("Bases com ruído geradas com sucesso.")

if __name__ == "__main__":
    main()
