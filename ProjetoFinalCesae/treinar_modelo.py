import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import joblib
import os

# Define uma semente para garantir que os resultados aleatórios sejam sempre os mesmos.
np.random.seed(42)

# ==============================================================================
# 1. Caminho e leitura dos dados
# Constrói o caminho para o ficheiro 'bank-full.csv' na mesma pasta que o script.
# Isto torna o script portátil e evita erros de 'Ficheiro não encontrado'.
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'bank-full.csv')

# Verifica se o ficheiro existe antes de tentar lê-lo para evitar erros.
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Erro: O ficheiro {file_path} não foi encontrado.")

# Lê o ficheiro CSV. O separador é ';' porque é um formato comum em certas regiões.
data = pd.read_csv(file_path, sep=';')

# ==============================================================================
# 2. Seleção de features e variável alvo
# ==============================================================================
# Define as colunas que serão usadas como variáveis de entrada (features).
features = ["age", "job", "marital", "education", "balance", "housing", "loan"]
# Define a coluna que queremos prever (target).
target = "default"

# Cria um novo DataFrame apenas com as colunas de interesse.
df = data[features + [target]].copy()

# Transforma a coluna alvo de texto ('yes'/'no') para números (1/0).
df[target] = df[target].apply(lambda x: 1 if x == 'yes' else 0)

# ==============================================================================
# 3. Split treino/teste estratificado
# ==============================================================================
# Separa os dados em variáveis de entrada (X) e variável alvo (y).
X = df[features]
y = df[target]

# Divide os dados em conjuntos de treino e teste.
# 'stratify=y' garante que a proporção de 'default' seja a mesma em ambos os conjuntos.
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ==============================================================================
# 4. One-hot encoding (dummies)
# ==============================================================================
# Converte variáveis categóricas (texto) em colunas numéricas (0s e 1s).
# 'drop_first=True' remove uma categoria de cada feature para evitar redundância.
X_train = pd.get_dummies(X_train_raw, drop_first=True, dtype=int)
X_test = pd.get_dummies(X_test_raw, drop_first=True, dtype=int)

# IMPORTANTE: Garantir que o teste tenha as mesmas colunas do treino
# Se uma categoria existir no treino mas não no teste, esta linha garante que a coluna é criada no teste com valor 0.
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# ==============================================================================
# 5. Treino do modelo logit
# ==============================================================================
# Adiciona uma coluna de 'constante' (intercepto) aos dados, necessária para o modelo estatístico.
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

# Treina o modelo de regressão logística.
logit_model = sm.Logit(y_train, X_train_const).fit()

# Usa o modelo treinado para prever as probabilidades no conjunto de teste.
test_proba = logit_model.predict(X_test_const)

# ==============================================================================
# PARTE 2: Métricas e Limiares
# ==============================================================================

# Calcula os pontos necessários para desenhar a Curva ROC.
fpr, tpr, thresholds = roc_curve(y_test, test_proba)
# Calcula a Área Sob a Curva (AUC), uma métrica geral da qualidade do modelo.
roc_auc = auc(fpr, tpr)

# Desenha e mostra o gráfico da Curva ROC.
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', label=f'AUC = {roc_auc:.3f}')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.title('Curva ROC')
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos (Sensitivity)')
plt.legend(loc="lower right")
plt.show()

print(f"AUC: {roc_auc:.4f}")

# Função para avaliar o desempenho do modelo com diferentes limiares de decisão.
def testar_limiares(probas, y_true, limiares=np.arange(0.01, 0.51, 0.01)):
    resultados = []
    
    for thr in limiares:
        # Classifica como 1 (risco) se a probabilidade for maior ou igual ao limiar.
        pred = (probas >= thr).astype(int)
        
        # Calcula a matriz de confusão para obter verdadeiros/falsos positivos/negativos.
        tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
        
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0 # Recall
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        f1 = f1_score(y_true, pred, zero_division=0)
        acc = accuracy_score(y_true, pred)
        
        resultados.append({
            'limiar': thr,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'precision': precision,
            'f1': f1,
            'accuracy': acc
        })
        
    return pd.DataFrame(resultados)

# Testa os limiares de 0.01 a 0.50 e guarda os resultados.
resultados_limiares = testar_limiares(test_proba, y_test)

# Mostra os 10 limiares que melhor detetam os casos de risco (maior Sensitivity/Recall).
print("\nTop 10 limiares por Sensitivity:")
print(resultados_limiares.sort_values(by='sensitivity', ascending=False).head(10))

# Encontra o limiar que oferece o melhor equilíbrio entre precisão e recall (máximo F1-Score).
idx_max_f1 = resultados_limiares['f1'].idxmax()
limiar_otimo = resultados_limiares.loc[idx_max_f1, 'limiar']
print(f"\nLimiar ótimo (max F1): {limiar_otimo:.3f}")

# Função auxiliar para mostrar as métricas de um limiar específico.
def avaliar_limiar(probas, y_true, thr):
    pred = (probas >= thr).astype(int)
    print(f"\n--- Resultados para Limiar: {thr} ---")
    print(confusion_matrix(y_true, pred))
    print(f"F1 Score: {f1_score(y_true, pred):.4f}")
    print(f"Sensitivity (Recall): {recall_score(y_true, pred):.4f}")

# Avalia o desempenho do modelo com o limiar ótimo e outros de referência.
avaliar_limiar(test_proba, y_test, thr=limiar_otimo)
avaliar_limiar(test_proba, y_test, thr=0.2)
avaliar_limiar(test_proba, y_test, thr=0.5)

# ==============================================================================
# PARTE 3: Sumário do Modelo (Equivalente ao Stargazer)
# ==============================================================================
# Mostra um resumo estatístico detalhado do modelo, incluindo coeficientes e significância.
print("\n")
print(logit_model.summary())

# ==============================================================================
# PARTE 4: Previsão em Novos Clientes
# ==============================================================================
# Cria um DataFrame com exemplos de novos clientes para testar a previsão.
novos_clientes = pd.DataFrame({
    'age': [25, 45, 60, 30],
    'job': ["student", "admin.", "retired", "blue-collar"],
    'marital': ["single", "married", "divorced", "married"],
    'education': ["secondary", "tertiary", "primary", "secondary"],
    'balance': [500, 2000, -200, 1500],
    'housing': ["no", "yes", "yes", "no"],
    'loan': ["no", "no", "yes", "yes"]
})

# Aplica o mesmo pré-processamento de one-hot encoding aos novos clientes.
novos_x = pd.get_dummies(novos_clientes, drop_first=True, dtype=int)

# Garante que os novos dados tenham exatamente as mesmas colunas que os dados de treino.
novos_x = novos_x.reindex(columns=X_train.columns, fill_value=0)

# Adiciona a coluna de constante, necessária para o modelo.
novos_x_const = sm.add_constant(novos_x, has_constant='add')

# Faz a previsão de probabilidade para os novos clientes.
novos_proba = logit_model.predict(novos_x_const)

# Classifica o risco com base num limiar de negócio definido (0.06).
limiar_risco = 0.06
novos_risco = np.where(novos_proba >= limiar_risco, "ALTO RISCO", "BAIXO RISCO")

# Cria um DataFrame para apresentar os resultados da previsão de forma clara.
previsoes = pd.DataFrame({
    'Cliente': [f"Cliente {i+1}" for i in range(len(novos_clientes))],
    'Idade': novos_clientes['age'],
    'Job': novos_clientes['job'],
    'Balance': novos_clientes['balance'],
    'P_default': round(novos_proba, 3),
    'Risco': novos_risco
})

print("\n--- Previsões para Novos Clientes ---")
print(previsoes)

# ==============================================================================
# PARTE 5: Guardar o Modelo e as Colunas para Produção
# ==============================================================================
# Guarda os artefactos necessários para usar o modelo noutra aplicação (ex: uma API).
print("\n--- A guardar artefactos do modelo para produção ---")

artefactos_para_producao = {
    'model': logit_model,                      # O objeto do modelo treinado.
    'model_columns': X_train.columns.tolist(), # A lista de colunas que o modelo espera.
    'target_threshold': 0.06                   # O limiar de decisão para classificar o risco.
}

output_filename = 'logit_model_artefacts.joblib'
joblib.dump(artefactos_para_producao, output_filename)

print(f"Modelo, colunas e limiar guardados com sucesso em '{output_filename}'")
