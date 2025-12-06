import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
# Importar o SMOTE e o Pipeline do imblearn
import shap
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

def train_credit_scoring_model():
    """
    Carrega os dados, pré-processa, otimiza e treina um modelo de RandomForest
    e guarda o modelo treinado.
    """
    # Carregar o dataset
    file_path = r'c:\Users\Pedro\Documents\GitHub\ProjetoFinalCesae\ProjetoFinalCesae\bank-full.csv'
    try:
        data = pd.read_csv(file_path, sep=';')
    except FileNotFoundError:
        print(f"Erro: O ficheiro {file_path} não foi encontrado.")
        return
    print("Dados carregados com sucesso.")

    # 1. Seleção de Features e da Variável-Alvo
    # 'features' são as colunas que vamos usar para treinar o modelo (as nossas variáveis de entrada).
    # Escolhemos colunas que, intuitivamente, podem influenciar o risco de crédito de uma pessoa.
    features = ['age', 'job', 'marital', 'education', 'balance', 'housing', 'loan']
    # 'target' é a coluna que queremos prever (a nossa variável de saída).
    target = 'default'

    X = data[features]
    # Os modelos de machine learning precisam de números, não de texto como 'yes' ou 'no'.
    # Por isso, convertemos a nossa coluna alvo 'default' para 1 (se for 'yes') e 0 (se for 'no').
    y = data[target].apply(lambda x: 1 if x == 'yes' else 0)

    # 2. Pré-processamento dos Dados
    # O modelo trata colunas com números (como 'age') de forma diferente de colunas com texto (como 'job').
    # Primeiro, separamos os nomes das colunas em duas listas.
    numeric_features = ['age', 'balance']
    categorical_features = ['job', 'marital', 'education', 'housing', 'loan']

    # Em seguida, criamos um 'preprocessor'. É uma ferramenta que aplica diferentes regras a diferentes colunas.
    preprocessor = ColumnTransformer(
        transformers=[
            # Regra 1 ('num'): Para as colunas numéricas, usamos o 'StandardScaler'.
            # Ele ajusta os números para que todos fiquem numa escala semelhante. Isto ajuda o modelo
            # a não dar mais importância a uma coluna só porque os seus números são maiores (ex: 'balance' vs 'age').
            ('num', StandardScaler(), numeric_features),
            # Regra 2 ('cat'): Para as colunas de texto, usamos o 'OneHotEncoder'.
            # Ele transforma categorias de texto em colunas de 0s e 1s. Por exemplo, a coluna 'marital'
            # com "single" e "married" será transformada em duas novas colunas: 'marital_single' e 'marital_married'.
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # 3. Divisão dos Dados em Treino e Teste
    # É crucial dividir os nossos dados. Usamos a maior parte para 'treinar' o modelo e guardamos
    # uma pequena parte (o conjunto de 'teste') para avaliá-lo no final, como se fosse um exame.
    # 'test_size=0.2' significa que 20% dos dados serão para o teste.
    # 'random_state=42' garante que a divisão seja sempre a mesma, para que os resultados sejam reprodutíveis.
    # 'stratify=y' é muito importante aqui. Garante que a proporção de 'default' (1s e 0s) seja a mesma
    # tanto no conjunto de treino como no de teste, o que é essencial para dados desequilibrados como os nossos.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Dados divididos: {len(X_train)} para treino, {len(X_test)} para teste.")

    # 4. Criação e Treino do Modelo com um Pipeline
    # Um 'Pipeline' é como uma linha de montagem. Ele encadeia vários passos para que sejam executados em ordem.
    # Isto torna o código mais limpo e seguro, evitando erros comuns.
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), # 1. Pré-processamento
                            # 2. Balanceamento com SMOTE: O nosso problema é que temos muito poucos clientes com 'default=yes'.
                            # O SMOTE ajuda a resolver isto criando novos exemplos "sintéticos" (artificiais mas realistas)
                            # da classe minoritária. Isto dá ao modelo mais exemplos para aprender.
                            ('smote', SMOTE(random_state=42)), # 2. Balanceamento com SMOTE
                            # 3. Classificador: Este é o cérebro da operação, o modelo em si.
                            # Usamos um 'RandomForestClassifier', que é um modelo potente que combina as previsões
                            # de muitas "árvores de decisão" para chegar a um resultado mais robusto.
                            # 'class_weight='balanced'' é uma segurança extra para dizer ao modelo para prestar mais atenção
                            # aos casos de 'default=yes', que são mais raros e mais importantes.
                            ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced'))]) # 3. Classificador

    # 5. Otimização de Hiperparâmetros com GridSearchCV
    # Um modelo tem várias "configurações" ou "hiperparâmetros" (ex: número de árvores).
    # O 'GridSearchCV' é uma ferramenta que testa várias combinações dessas configurações para encontrar a melhor.
    # ATENÇÃO: Este processo pode ser lento, pois treina o modelo várias vezes.
    param_grid = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [10, 20, None],
        'classifier__min_samples_leaf': [1, 2, 4]
    }

    # 'scoring="f1"': Dizemos ao GridSearchCV para otimizar o 'F1-score'. Esta métrica é ideal para o nosso problema
    # porque tenta encontrar um bom equilíbrio entre "não deixar passar os casos de risco" (recall) e
    # "estar certo quando prevê um risco" (precision).
    # 'cv=3' (Cross-Validation): Para cada combinação de parâmetros, ele divide os dados de treino em 3 partes,
    # treinando em duas e testando na terceira. Isto dá uma medida mais fiável da qualidade de cada combinação.
    # 'n_jobs=-1': Usa todos os processadores do computador para acelerar a busca.
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1', n_jobs=-1, verbose=2)

    print("A iniciar a otimização de hiperparâmetros com GridSearchCV...")
    grid_search.fit(X_train, y_train)

    print("\nMelhores parâmetros encontrados:")
    print(grid_search.best_params_)

    # No final, o 'grid_search' guarda o melhor modelo que encontrou, já treinado com os melhores parâmetros.
    model = grid_search.best_estimator_
    print("Modelo treinado com sucesso.")

    # 6. Avaliação do Modelo no Conjunto de Teste
    # Agora, usamos o conjunto de teste (os dados que o modelo nunca viu) para ver o seu desempenho real.
    print("\n--- Avaliação do Modelo ---")
    y_pred_default = model.predict(X_test)
    
    # Avaliação com o limiar padrão de 50%. O modelo prevê '1' se a probabilidade for > 50%.
    print("\n--- Resultados com Limiar Padrão (0.5) ---")
    print(f"Acurácia: {accuracy_score(y_test, y_pred_default):.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred_default))
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred_default))

    # 7. Avaliação com um Limiar de Decisão Ajustado
    # Manter os dois relatórios (50% e 20%) é importante. O de 50% é o nosso diagnóstico (mostra o problema)
    # e o de 20% é a nossa solução (mostra o desempenho com a nossa regra de negócio aplicada).
    # Para um problema de risco, podemos não querer esperar por 50% de certeza.
    # Podemos ser mais cautelosos e sinalizar um cliente como risco mesmo com uma probabilidade menor.
    # Aqui, testamos o que acontece se considerarmos risco qualquer cliente com probabilidade >= 20%.
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    novo_limiar = 0.20
    y_pred_ajustado = (y_pred_proba >= novo_limiar).astype(int)

    print(f"\n--- Resultados com Limiar Ajustado ({novo_limiar}) ---")
    print(f"Acurácia: {accuracy_score(y_test, y_pred_ajustado):.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred_ajustado))
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred_ajustado))

    # 9. Análise da Importância das Features
    # Agora que o modelo está treinado, podemos perguntar-lhe o que ele achou mais importante.
    print("\n--- Importância das Features ---")
    
    # Extrair os nomes das features após o OneHotEncoding
    # O OneHotEncoder cria novas colunas (ex: 'job_admin', 'job_student'), precisamos de obter esses nomes.
    cat_feature_names = model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    # Juntar os nomes das features numéricas e das novas features categóricas
    all_feature_names = numeric_features + list(cat_feature_names)
    
    # Extrair as importâncias do classificador RandomForest
    importances = model.named_steps['classifier'].feature_importances_
    
    # Criar um DataFrame para visualizar as importâncias de forma clara
    feature_importance_df = pd.DataFrame({'Feature': all_feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
    print("As 10 features mais importantes para o modelo:")
    print(feature_importance_df.head(10).to_string(index=False))

    # 10. Análise do Efeito Específico das Features (SHAP)
    # Para responder à pergunta "qual o efeito específico de cada feature?", usamos a técnica SHAP.
    # Ela mostra, para uma previsão individual, como cada feature contribuiu para aumentar ou diminuir o risco.
    print("\n--- Análise de Efeito Específico (SHAP) para um Cliente Exemplo ---")

    # O SHAP precisa do modelo e dos dados de treino transformados para criar um "explicador".
    # Primeiro, transformamos os dados de treino com o nosso pré-processador.
    X_train_transformed = model.named_steps['preprocessor'].transform(X_train).toarray()
    X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=all_feature_names)

    # Criamos o explicador SHAP. Usamos o TreeExplainer porque o nosso modelo é baseado em árvores.
    explainer = shap.TreeExplainer(model.named_steps['classifier'], X_train_transformed_df)

    # Agora, calculamos os valores SHAP para os nossos dados de teste.
    # Transformamos os dados de teste primeiro.
    X_test_transformed = model.named_steps['preprocessor'].transform(X_test).toarray()
    X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=all_feature_names)
    shap_values = explainer(X_test_transformed_df)

    # Vamos analisar o primeiro cliente do conjunto de teste como exemplo.
    # Em vez de imprimir o objeto complexo, vamos criar um gráfico interativo.
    print("\nAnálise para o primeiro cliente do conjunto de teste gerada.")
    
    # O SHAP gera valores para cada classe. Estamos interessados na classe '1' (incumprimento).
    # O base_value é a previsão média do modelo sobre todos os dados.
    base_value_class1 = explainer.expected_value[1]
    # Os shap_values_class1 são os "empurrões" de cada feature para a classe '1'.
    shap_values_class1 = shap_values.values[:, :, 1]
    
    # Criar o gráfico de força para o primeiro cliente do conjunto de teste.
    force_plot = shap.force_plot(base_value_class1, 
                                 shap_values_class1[0,:], 
                                 X_test_transformed_df.iloc[0,:], # Usamos os dados TRANSFORMADOS para corresponder aos shap_values
                                 matplotlib=False) # Usar a versão JS

    # Guardar o gráfico como um ficheiro HTML.
    shap.save_html("analise_cliente_shap.html", force_plot)
    print("Gráfico de análise SHAP guardado como 'analise_cliente_shap.html'. Abra este ficheiro num browser.")

    # 11. Guardar o Modelo Final
    # Guardamos o nosso modelo treinado e otimizado num ficheiro. Assim, podemos carregá-lo noutra aplicação
    # (como a nossa aplicação Flask) para fazer previsões em novos clientes sem ter de treinar tudo de novo.
    model_filename = 'credit_scoring_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nModelo guardado com sucesso como '{model_filename}'.")


if __name__ == '__main__':
    train_credit_scoring_model()
