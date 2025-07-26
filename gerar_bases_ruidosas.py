import pandas as pd
import random
import string
import unicodedata

# --- Funções auxiliares de ruído ---

def abreviar_nome(nome):
    if not isinstance(nome, str):
        return ""
    nome = nome.strip()
    if nome.lower() == "michael":
        return "Mike"
    elif nome.lower() == "william":
        return "Will"
    elif len(nome) > 4:
        return nome[:4]
    return nome

def inverter_nome(first, last):
    return f"{last} {first}"

name_variants = {
    "Stephen": "Steven",
    "Geoffrey": "Jeffrey",
    "Sean": "Shawn",
    "Catherine": "Katherine",
    "Katherine": "Catherine",
    "Brian": "Bryan",
    "Bryan": "Brian",
    "Jon": "John",
    "John": "Jon",
    "Sara": "Sarah",
    "Sarah": "Sara",
    "Erik": "Eric",
    "Eric": "Erik",
    "Micheal": "Michael",
    "Mikael": "Michael",
    "Cristina": "Kristina",
    "Kristina": "Cristina"
}

phonetic_subs = {
    "ph": "f",
    "ght": "t",
    "c": "k",
    "ck": "k",
    "y": "i",
    "ch": "k",
    "x": "ks",
    "z": "s",
    "oo": "u",
    "ee": "i",
    "ou": "ow",
    "gn": "n",
    "wr": "r"
}


def substituir_fonetico(name):
    name_cap = name.capitalize()
    # 1. Substituição direta por variante fonética real
    if name_cap in name_variants:
        return name_variants[name_cap]

    # 2. Aplicação de substituições fonéticas genéricas
    name_lower = name.lower()
    for k, v in phonetic_subs.items():
        name_lower = name_lower.replace(k, v)
    return name_lower.capitalize()

# --- Leitura da base original ---

df = pd.read_csv("datasets/compas-scores-raw.csv")

# Correção de campos básicos
df["FirstName"] = df["FirstName"].fillna("").str.strip()
df["LastName"] = df["LastName"].fillna("").str.strip()
df["DateOfBirth"] = df["DateOfBirth"].fillna("").str.strip()

# --- I1: Base limpa (pequenas correções visuais) ---
I1 = df.copy()
I1["FullName"] = I1["FirstName"] + " " + I1["LastName"]
I1.to_csv("datasets/compas_l1.csv", index=False)

# --- I2: Base com ruído moderado ---
I2 = df.copy()
I2["FirstName"] = I2["FirstName"].apply(lambda x: substituir_fonetico(str(x)))
I2["LastName"] = I2["LastName"].apply(lambda x: substituir_fonetico(str(x)))
I2["FullName"] = I2["FirstName"] + " " + I2["LastName"]
I2.to_csv("datasets/compas_l3.csv", index=False)

# --- I3: Base com ruído severo ---
I3 = df.copy()
I3["FirstName"] = I3["FirstName"].apply(abreviar_nome)
I3["FullName"] = I3.apply(lambda row: inverter_nome(row["FirstName"], row["LastName"]), axis=1)
I3.to_csv("datasets/compas_l2.csv", index=False)
