import pandas as pd
import recordlinkage as rl
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# Ler arquivos
pares_l1 = pd.read_csv("datasets/pares_blocagem_l1.csv", sep=",")
pares_l2 = pd.read_csv("datasets/pares_blocagem_l2.csv", sep=",")
pares_l3 = pd.read_csv("datasets/pares_blocagem_l3.csv", sep=",")

pares = pd.concat([pares_l1, pares_l2, pares_l3], ignore_index=True)

# Criar MultiIndex
pairs_index = pd.MultiIndex.from_arrays(
    [pares["idx1"], pares["idx2"]],
    names=["idx1", "idx2"]
)

# Comparação
compare = rl.Compare()
compare.exact("FirstName_1", "FirstName_2", label="first_name")
compare.exact("LastName_1", "LastName_2", label="last_name")
compare.exact("DateOfBirth_1", "DateOfBirth_2", label="date_of_birth")
compare.string("FirstName_1", "FirstName_2", method="jarowinkler", label="first_name_sim")
compare.string("LastName_1", "LastName_2", method="jarowinkler", label="last_name_sim")

features = compare.compute(pairs_index, pares)

# Criar MultiIndex dos pares correspondentes (labels)
match_index = pd.MultiIndex.from_arrays(
    [pares.loc[pares["Person_ID_1"] == pares["Person_ID_2"], "idx1"],
     pares.loc[pares["Person_ID_1"] == pares["Person_ID_2"], "idx2"]],
    names=["idx1", "idx2"]
)

# Treinamento do classificador
classifier = rl.LogisticRegressionClassifier()
classifier.fit(features, match_index)

# Predição
predicoes = classifier.predict(features)  # Retorna MultiIndex dos pares classificados como match

#Juntar predição ao DataFrame original
pares_indexed = pares.set_index(["idx1", "idx2"])

# Inicializa coluna com 0
pares_indexed["match_predito"] = 0

# Preenche apenas os pares previstos como 1
pares_indexed.loc[predicoes, "match_predito"] = 1

# Coluna com valor verdadeiro
pares_indexed["match_verdadeiro"] = (pares_indexed["Person_ID_1"] == pares_indexed["Person_ID_2"]).astype(int)

# Reseta índice e salvar como CSV
resultado = pares_indexed.reset_index()
resultado.to_csv("datasets/resultado_classificacao.csv", index=False)

print(resultado.head())

# Métricas
verdadeiro = resultado["match_verdadeiro"]
predito = resultado["match_predito"]

acuracia = accuracy_score(verdadeiro, predito)
precisao = precision_score(verdadeiro, predito, zero_division=0)
recall = recall_score(verdadeiro, predito, zero_division=0)
f1 = f1_score(verdadeiro, predito, zero_division=0)
matriz_confusao = confusion_matrix(verdadeiro, predito)

print("\nMétricas de Classificação:")
print(f"Acurácia:  {acuracia:.4f}")
print(f"Precisão:  {precisao:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print("\nMatriz de confusão:")
print(matriz_confusao)

tn, fp, fn, tp = matriz_confusao.ravel()

print(f"TN: {tn}")
print(f"FP: {fp}")
print(f"FN: {fn}")
print(f"TP: {tp}")