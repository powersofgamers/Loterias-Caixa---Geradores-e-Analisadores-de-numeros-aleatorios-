
import json
import random
from pathlib import Path
from collections import Counter
from datetime import datetime

BASE_DIR = Path(__file__).parent
HISTORICO_DIR = BASE_DIR / "historico"
HISTORICO_DIR.mkdir(exist_ok=True)

ARQUIVO_HISTORICO = HISTORICO_DIR / "historico_quina.json"


class QuinaAgente:
    def __init__(self):
        self.todos_numeros = list(range(1, 81))
        self.historico = self.carregar_historico()

    def carregar_historico(self):
        if ARQUIVO_HISTORICO.exists():
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                return json.load(f)

        return {
            "analises": [],
            "avaliacoes": [],
            "estatisticas": {
                "2_acertos": 0,
                "3_acertos": 0,
                "4_acertos": 0,
                "5_acertos": 0
            }
        }

    def salvar_historico(self):
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, indent=4, ensure_ascii=False)

    def calcular_frequencias(self):
        contador = Counter()

        for item in self.historico["analises"]:
            for numero in item["entrada"]:
                contador[str(numero)] += 1

        return contador

    def analisar_numeros(self, numeros):
        numeros = sorted(set(numeros))

        if len(numeros) != 5:
            raise ValueError("Você deve informar exatamente 5 números únicos.")

        for n in numeros:
            if n < 1 or n > 80:
                raise ValueError("Os números devem estar entre 1 e 80.")

        nao_usados = [n for n in self.todos_numeros if n not in numeros]

        frequencias = self.calcular_frequencias()

        # IA simples baseada em frequência histórica
        candidatos = sorted(
            nao_usados,
            key=lambda x: frequencias.get(str(x), 0)
        )

        inteligentes = candidatos[:2]
        aleatorios = random.sample(nao_usados, 3)

        nova_ordem = list(set(inteligentes + aleatorios))

        while len(nova_ordem) < 5:
            extra = random.choice(nao_usados)

            if extra not in nova_ordem:
                nova_ordem.append(extra)

        random.shuffle(nova_ordem)

        registro = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "entrada": numeros,
            "sugestao": nova_ordem
        }

        self.historico["analises"].append(registro)

        self.salvar_historico()

        return registro

    def avaliar_resultado(self, numeros_sorteados, numeros_agente):
        acertos = len(set(numeros_sorteados) & set(numeros_agente))

        avaliacao = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "numeros_sorteados": numeros_sorteados,
            "numeros_agente": numeros_agente,
            "acertos": acertos
        }

        # Estatísticas automáticas
        if acertos == 2:
            self.historico["estatisticas"]["2_acertos"] += 1
            print("\n✅ 2 acertos registrados!")

        elif acertos == 3:
            self.historico["estatisticas"]["3_acertos"] += 1
            print("\n🎯 3 acertos! Bom desempenho!")

        elif acertos == 4:
            self.historico["estatisticas"]["4_acertos"] += 1
            print("\n🔥 4 acertos! Excelente resultado!")

        elif acertos == 5:
            self.historico["estatisticas"]["5_acertos"] += 1
            print("\n🏆 5 ACERTOS! QUINA COMPLETA!")

        else:
            print(f"\nAcertos: {acertos}")

        self.historico["avaliacoes"].append(avaliacao)

        self.salvar_historico()

        return avaliacao

    def mostrar_estatisticas(self):
        stats = self.historico.get("estatisticas", {})

        print("\n===== ESTATÍSTICAS =====")
        print(f"2 acertos: {stats.get('2_acertos', 0)}")
        print(f"3 acertos: {stats.get('3_acertos', 0)}")
        print(f"4 acertos: {stats.get('4_acertos', 0)}")
        print(f"5 acertos: {stats.get('5_acertos', 0)}")

    def mostrar_historico(self):
        print("\n===== HISTÓRICO COMPLETO =====")
        print(json.dumps(self.historico, indent=4, ensure_ascii=False))


def menu():
    agente = QuinaAgente()

    while True:
        print("\n===== QUINA AGENTE =====")
        print("1 - Analisar números")
        print("2 - Avaliar resultado")
        print("3 - Ver histórico")
        print("4 - Ver estatísticas")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                entrada = input(
                    "Digite 5 números entre 1 e 80 separados por espaço: "
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
            agente.mostrar_historico()

        elif opcao == "4":
            agente.mostrar_estatisticas()

        elif opcao == "5":
            print("Encerrando agente...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
