import random, math
from datetime import datetime

def gerar_dado(i, df, model, le, ideal, limite_inferior, limite_superior):
    """
    Gera um dado fictício de velocidade e classifica como Normal ou Anômalo
    usando o modelo treinado.
    Retorna um dicionário com timestamp, velocidade, movimento e status.
    """
    prob_anomalia = 0.1

    # Gerar velocidade
    if random.random() < prob_anomalia:
        # Anomalia (abaixo ou acima)
        if random.random() < 0.5:
            # abaixo do limite inferior
            velocidade = round(random.uniform(limite_inferior - 0.02, limite_inferior - 0.001), 4)
        else:
            # acima do limite superior
            velocidade = round(random.uniform(limite_superior + 0.001, limite_superior + 0.02), 4)
    else:
        # Valor normal com ruído
        amplitude = 0.002
        ruido_max = 0.001
        velocidade = round(
            ideal + amplitude * math.sin(i * 0.1) + random.uniform(-ruido_max, ruido_max), 4
        )
        # garante que valor normal fique dentro dos limites
        velocidade = max(limite_inferior, min(limite_superior, velocidade))

    # Selecionar movimento aleatório
    movimento = random.choice(list(df['movimento'].unique()))

    # Classificar com o modelo
    movimento_num = le.transform([movimento])[0]
    pred = model.predict([[velocidade, movimento_num]])[0]
    status = "Normal" if pred == 1 else "Anômalo"

    # Retorna como dicionário
    dado = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "velocidade": velocidade,
        "movimento": movimento,
        "status": status
    }

    return dado
