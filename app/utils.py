#bibliotecas
import random, math
from datetime import datetime

#gerar de dados fictícios 
def gerar_dado(i, df, le, model, ideal, limite_inferior, limite_superior, session_state):
    #10% de chance de gerar anomalia
    prob_anomalia = 0.1
    #gerar velocidade
    if random.random() < prob_anomalia:
        #gerar anomalia
        if random.random() < 0.5:
            velocidade = round(random.uniform(0.06, limite_inferior - 0.001), 4)
        else:
            velocidade = round(random.uniform(limite_superior + 0.001, 0.12), 4)
    else:
        #gerar valor normal com ruido
        amplitude = 0.002
        ruido_max = 0.001
        if len(session_state.dados_reais) == 0:
            velocidade = ideal
        else:
            velocidade = round(
                ideal + amplitude * math.sin(i * 0.1) + random.uniform(-ruido_max, ruido_max), 4
            )
            velocidade = max(limite_inferior, min(limite_superior, velocidade))
    #selecionar movimento aleatório
    movimento = random.choice(list(df['movimento'].unique()))
    #prever status com modelo
    movimento_num = le.transform([movimento])[0]
    #fazer predição
    pred = model.predict([[velocidade, movimento_num]])[0]
    #status
    status = "Normal" if pred == 1 else "Anômalo"
    #retornar dado
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "velocidade": velocidade,
        "status": status
    }
