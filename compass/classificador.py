import pandas as pd
import recordlinkage as rl
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Função de classificação
def classificar(caminho_csv, nome_saida):
    print(f"\n==== Processando {caminho_csv} ====")

    # Ler arquivo da comparação
    pares = pd.read_csv(caminho_csv, sep=",")

    # Cria MultiIndex para todos os pares
    pairs_index = pd.MultiIndex.from_arrays(
        [pares["idx1"], pares["idx2"]],
        names=["idx1", "idx2"]
    )

    # Colunas que foi feita a comparação
    features = pares[["FirstName_sim", "LastName_sim", "DateOfBirth_eq"]]
    features.index = pairs_index

    # Cria MultiIndex para os casos positivos
    match_index = pd.MultiIndex.from_arrays(
        [pares.loc[pares["Person_ID_1"] == pares["Person_ID_2"], "idx1"],
         pares.loc[pares["Person_ID_1"] == pares["Person_ID_2"], "idx2"]],
        names=["idx1", "idx2"]
    )

    # Treinamento
    classifier = rl.LogisticRegressionClassifier()
    classifier.fit(features, match_index)

    # Predição
    predicoes = classifier.predict(features)

    # Juntar predição ao DataFrame
    pares_indexed = pares.set_index(["idx1", "idx2"])
    pares_indexed["match_predito"] = 0
    pares_indexed.loc[predicoes, "match_predito"] = 1
    pares_indexed["match_verdadeiro"] = (pares_indexed["Person_ID_1"] == pares_indexed["Person_ID_2"]).astype(int)

    # Salva resultado
    resultado = pares_indexed.reset_index()
    resultado.to_csv(f"compass/datasets/{nome_saida}", index=False)

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
    print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")


# Processar cada base separadamente
classificar("compass/datasets/comparacao_blocagem_l1.csv", "resultado_classificacao_l1.csv")
classificar("compass/datasets/comparacao_blocagem_l2.csv", "resultado_classificacao_l2.csv")
classificar("compass/datasets/comparacao_blocagem_l3.csv", "resultado_classificacao_l3.csv")
