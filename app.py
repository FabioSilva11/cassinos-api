import random
import json
from flask import Flask, jsonify

app = Flask(__name__)

# Dicionário de opções de imagens com URLs
opcoes = {
    "cereja": {"valor": 5, "img": "https://cdn.pixabay.com/photo/2014/12/21/23/34/cherry-575547_640.png"},
    "limao": {"valor": 8, "img": "https://dcdn.mitiendanube.com/stores/002/296/660/products/limao1-ec0330346f306e615a16606772664916-1024-1024.png"},
    "laranja": {"valor": 3, "img": "https://ibassets.com.br/ib.item.image.big/b-0c92a27787154a9db42f6777e5daa995.png"},
    "uva": {"valor": 7, "img": "https://i.pinimg.com/originals/7e/3d/9a/7e3d9aab4a5969747f203ef3beea2b64.png"},
    "7": {"valor": 10, "img": "https://cdn-icons-png.flaticon.com/512/6913/6913789.png"}
}

# Contador para controlar as requisições
contador_requisicoes = 0

# Função para realizar um sorteio
def realizar_sorteio():
    global contador_requisicoes
    contador_requisicoes += 1

    # A cada 1000 requisições, mostrar três símbolos idênticos
    if contador_requisicoes % 1000 == 0:
        simbolo = random.choice(list(opcoes.keys()))
        sorteios = [opcoes[simbolo].copy() for _ in range(3)]
        faltam_requisicoes = 1000 - (contador_requisicoes % 1000)
    else:
        # Caso contrário, retorna 3 símbolos diferentes
        simbolos_aleatorios = random.sample(list(opcoes.keys()), 3)
        sorteios = [opcoes[simbolo].copy() for simbolo in simbolos_aleatorios]
        faltam_requisicoes = 1000 - (contador_requisicoes % 1000)

    return sorteios, faltam_requisicoes

# Rota para retornar o resultado dos sorteios
@app.route('/')
def obter_resultado_sorteio():
    resultados_combinados, faltam_requisicoes = realizar_sorteio()

    # Verificar se o usuário ganhou ou perdeu
    valores = [simbolo["valor"] for simbolo in resultados_combinados]
    if len(set(valores)) == 1:
        resultado = "Ganhou!"
    else:
        resultado = "Perdeu."

    resultados_combinados.append({"faltam_requisicoes": faltam_requisicoes, "resultado": resultado})
    return jsonify(resultados_combinados)

# Rodar a nossa API
if __name__ == '__main__':
    app.run(host='0.0.0.0')
