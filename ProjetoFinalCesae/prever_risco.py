import joblib
import pandas as pd
import os

def prever_risco_cliente(dados_cliente):
    """
    Carrega o modelo de credit score e prevê o risco para um novo cliente.

    Args:
        dados_cliente (dict): Um dicionário com os dados do cliente.
                              Ex: {'age': 30, 'job': 'technician', ...}

    Returns:
        tuple: Uma tupla contendo a probabilidade de incumprimento e a classificação de risco.
    """
    # --- Passo 1: Carregar o Modelo ---
    # O nosso modelo treinado foi guardado num ficheiro. Para o usarmos, primeiro precisamos de o carregar.
    # A linha abaixo constrói o caminho para o ficheiro do modelo de forma segura.
    # 'os.path.dirname(__file__)' obtém a pasta onde este script está, e 'os.path.join' junta
    # essa pasta com o nome do ficheiro do modelo. Isto garante que o encontramos, independentemente
    # de onde executamos a aplicação.
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'credit_scoring_model.joblib')

    try:
        # 'joblib.load' é a função que efetivamente carrega o nosso modelo guardado para a memória.
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        # Se o ficheiro do modelo não for encontrado, devolvemos uma mensagem de erro clara.
        return None, "Erro: Ficheiro 'credit_scoring_model.joblib' não encontrado."

    # --- Passo 2: Preparar os Dados do Novo Cliente ---
    # O nosso modelo foi treinado com um formato de dados específico (um DataFrame do pandas).
    # Por isso, temos de converter os dados do novo cliente (que recebemos como um dicionário)
    # para esse mesmo formato antes de os passarmos ao modelo.
    cliente_df = pd.DataFrame([dados_cliente])

    # --- Passo 3: Fazer a Previsão ---
    # Aqui é onde a "magia" acontece. Usamos o método 'predict_proba' do modelo.
    # Em vez de nos dar apenas uma resposta 'sim' ou 'não', ele dá-nos a probabilidade de cada classe.
    # O resultado será algo como [probabilidade_de_nao_incumprimento, probabilidade_de_incumprimento].
    # Como só nos interessa a probabilidade de incumprimento (a classe '1'), usamos '[:, 1][0]' para a extrair.
    probabilidade_incumprimento = model.predict_proba(cliente_df)[:, 1][0]

    # --- Passo 4: Classificar o Risco com Base nos Nossos Limiares ---
    # Com base nos testes que fizemos no ficheiro 'treinar_modelo.py', descobrimos que um limiar de 20%
    # nos dava um bom equilíbrio para detetar o máximo de risco possível.
    # Aqui, aplicamos essa regra de negócio.
    if probabilidade_incumprimento >= 0.50:
        # Se a probabilidade for muito alta, classificamos como 'Risco Alto'.
        risco = "Risco Alto"
    elif probabilidade_incumprimento >= 0.20:
        # Se estiver acima do nosso limiar de 20%, é um 'Risco Moderado' e deve ser analisado.
        risco = "Risco Moderado"
    else:
        # Abaixo de 20%, consideramos o risco baixo.
        risco = "Risco Baixo"

    # Devolvemos tanto a probabilidade exata como a classificação de risco final.
    return probabilidade_incumprimento, risco

# O bloco de código abaixo só é executado quando corremos este ficheiro diretamente (ex: 'python prever_risco.py').
# Serve para testar a nossa função 'prever_risco_cliente' de forma isolada.
if __name__ == '__main__':
    # --- Bloco de Teste ---

    # Teste 1: Simulamos um cliente com um perfil que, à partida, parece seguro.
    novo_cliente_1 = {
        'age': 45,
        'job': 'management',
        'marital': 'married',
        'education': 'tertiary',
        'balance': 5000,
        'housing': 'no',
        'loan': 'no'
    }
    # Chamamos a nossa função com os dados deste cliente.
    prob, risco = prever_risco_cliente(novo_cliente_1)
    if prob is not None:
        print(f"--- Cliente 1 ---")
        print(f"Dados: {novo_cliente_1}")
        print(f"Probabilidade de Incumprimento: {prob:.2%}")
        print(f"Classificação de Risco: {risco}\n")


    # Teste 2: Simulamos um cliente com um perfil que parece mais arriscado.
    novo_cliente_2 = {
        'age': 25,
        'job': 'student',
        'marital': 'single',
        'education': 'secondary',
        'balance': -100, # Saldo negativo
        'housing': 'yes',
        'loan': 'yes'
    }
    # Chamamos a função novamente com os dados do segundo cliente.
    prob, risco = prever_risco_cliente(novo_cliente_2)
    if prob is not None:
        print(f"--- Cliente 2 ---")
        print(f"Dados: {novo_cliente_2}")
        print(f"Probabilidade de Incumprimento: {prob:.2%}")
        print(f"Classificação de Risco: {risco}")
