
import json
import random
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent
HISTORICO_DIR = BASE_DIR / "historico"
HISTORICO_DIR.mkdir(exist_ok=True)

ARQUIVO_HISTORICO = HISTORICO_DIR / "historico.json"


class AgenteLoteria:
    def __init__(self):
        self.todos_numeros = list(range(1, 61))
        self.historico = self.carregar_historico()

    def carregar_historico(self):
        if ARQUIVO_HISTORICO.exists():
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                return json.load(f)

        return {
            "analises": [],
            "avaliacoes": []
        }

    def salvar_historico(self):
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, indent=4, ensure_ascii=False)

    def analisar_numeros(self, numeros):
        numeros = sorted(set(numeros))

        if len(numeros) != 6:
            raise ValueError("Você deve informar exatamente 6 números únicos.")

        for n in numeros:
            if n < 1 or n > 60:
                raise ValueError("Os números devem estar entre 1 e 60.")

        nao_usados = [n for n in self.todos_numeros if n not in numeros]

        frequencias = self.calcular_frequencias()

        # Mistura números antigos e novos para aprendizado
        candidatos = sorted(
            nao_usados,
            key=lambda x: frequencias.get(str(x), 0)
        )

        # pega 3 números pouco usados
        novos = candidatos[:3]

        # pega 3 números aleatórios
        aleatorios = random.sample(nao_usados, 3)

        nova_ordem = list(set(novos + aleatorios))

        while len(nova_ordem) < 6:
            extra = random.choice(nao_usados)
            if extra not in nova_ordem:
                nova_ordem.append(extra)

        random.shuffle(nova_ordem)

        registro = {
            "entrada": numeros,
            "sugestao": nova_ordem
        }

        self.historico["analises"].append(registro)
        self.salvar_historico()

        return registro

    def calcular_frequencias(self):
        contador = Counter()

        for item in self.historico["analises"]:
            for numero in item["entrada"]:
                contador[str(numero)] += 1

        return contador

    def avaliar_resultado(self, numeros_sorteados, numeros_agente):
        acertos = len(set(numeros_sorteados) & set(numeros_agente))

        avaliacao = {
            "numeros_sorteados": numeros_sorteados,
            "numeros_agente": numeros_agente,
            "acertos": acertos
        }

        if acertos >= 4:
            print(f"\n🎯 ÓTIMO RESULTADO: {acertos} acertos!")

        self.historico["avaliacoes"].append(avaliacao)
        self.salvar_historico()

        return avaliacao


def menu():
    agente = AgenteLoteria()

    while True:
        print("\n===== AGENTE LOTERIA =====")
        print("1 - Analisar números")
        print("2 - Avaliar resultado")
        print("3 - Ver histórico")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                entrada = input(
                    "Digite 6 números entre 1 e 60 separados por espaço: "
                )

                numeros = [int(x) for x in entrada.split()]

                resultado = agente.analisar_numeros(numeros)

                print("\nNúmeros analisados:")
                print(resultado["entrada"])

                print("\nNova sugestão do agente:")
                print(resultado["sugestao"])

            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            try:
                sorteados = input(
                    "Digite os números sorteados: "
                )

                agente_nums = input(
                    "Digite os números gerados pelo agente: "
                )

                numeros_sorteados = [int(x) for x in sorteados.split()]
                numeros_agente = [int(x) for x in agente_nums.split()]

                avaliacao = agente.avaliar_resultado(
                    numeros_sorteados,
                    numeros_agente
                )

                print("\nResultado da avaliação:")
                print(avaliacao)

            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "3":
            print("\n=== HISTÓRICO ===")
            print(json.dumps(agente.historico, indent=4, ensure_ascii=False))

        elif opcao == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
