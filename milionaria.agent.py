
import json
import random
from pathlib import Path
from collections import Counter
from datetime import datetime

BASE_DIR = Path(__file__).parent
HISTORICO_DIR = BASE_DIR / "historico"
HISTORICO_DIR.mkdir(exist_ok=True)

ARQUIVO_HISTORICO = HISTORICO_DIR / "historico_milionaria.json"


class MilionariaAgente:

    def __init__(self):
        self.numeros_principais = list(range(1, 51))
        self.trevos = list(range(1, 7))
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
                "5_acertos": 0,
                "6_acertos": 0,
                "0_trevos": 0,
                "1_trevo": 0,
                "2_trevos": 0
            }
        }

    def salvar_historico(self):

        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(
                self.historico,
                f,
                indent=4,
                ensure_ascii=False
            )

    def calcular_frequencias(self):

        contador = Counter()

        for item in self.historico["analises"]:
            for numero in item["entrada"]:
                contador[str(numero)] += 1

        return contador

    def calcular_frequencias_trevos(self):

        contador = Counter()

        for item in self.historico["analises"]:
            for trevo in item["trevos_entrada"]:
                contador[str(trevo)] += 1

        return contador

    def analisar_numeros(self, numeros, trevos):

        numeros = sorted(set(numeros))
        trevos = sorted(set(trevos))

        if len(numeros) != 6:
            raise ValueError(
                "Você deve informar exatamente 6 números únicos."
            )

        if len(trevos) != 2:
            raise ValueError(
                "Você deve informar exatamente 2 trevos."
            )

        for n in numeros:
            if n < 1 or n > 50:
                raise ValueError(
                    "Os números devem estar entre 1 e 50."
                )

        for t in trevos:
            if t < 1 or t > 6:
                raise ValueError(
                    "Os trevos devem estar entre 1 e 6."
                )

        nao_usados = [
            n for n in self.numeros_principais
            if n not in numeros
        ]

        frequencias = self.calcular_frequencias()

        frequencias_trevos = self.calcular_frequencias_trevos()

        candidatos = sorted(
            nao_usados,
            key=lambda x: frequencias.get(str(x), 0)
        )

        inteligentes = candidatos[:3]

        aleatorios = random.sample(nao_usados, 3)

        nova_ordem = list(set(inteligentes + aleatorios))

        while len(nova_ordem) < 6:

            extra = random.choice(nao_usados)

            if extra not in nova_ordem:
                nova_ordem.append(extra)

        random.shuffle(nova_ordem)

        trevos_disponiveis = [
            t for t in self.trevos
            if t not in trevos
        ]

        trevos_sugeridos = sorted(
            trevos_disponiveis,
            key=lambda x: frequencias_trevos.get(str(x), 0)
        )[:2]

        while len(trevos_sugeridos) < 2:

            extra = random.choice(self.trevos)

            if extra not in trevos_sugeridos:
                trevos_sugeridos.append(extra)

        registro = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "entrada": numeros,
            "trevos_entrada": trevos,
            "sugestao": nova_ordem,
            "trevos_sugestao": trevos_sugeridos
        }

        self.historico["analises"].append(registro)

        self.salvar_historico()

        return registro

    def avaliar_resultado(
        self,
        numeros_sorteados,
        numeros_agente,
        trevos_sorteados,
        trevos_agente
    ):

        acertos_numeros = len(
            set(numeros_sorteados) & set(numeros_agente)
        )

        acertos_trevos = len(
            set(trevos_sorteados) & set(trevos_agente)
        )

        avaliacao = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "numeros_sorteados": numeros_sorteados,
            "numeros_agente": numeros_agente,
            "trevos_sorteados": trevos_sorteados,
            "trevos_agente": trevos_agente,
            "acertos_numeros": acertos_numeros,
            "acertos_trevos": acertos_trevos
        }

        if acertos_numeros == 2:
            self.historico["estatisticas"]["2_acertos"] += 1
            print("\n✅ 2 acertos!")

        elif acertos_numeros == 3:
            self.historico["estatisticas"]["3_acertos"] += 1
            print("\n🎯 3 acertos!")

        elif acertos_numeros == 4:
            self.historico["estatisticas"]["4_acertos"] += 1
            print("\n🔥 4 acertos!")

        elif acertos_numeros == 5:
            self.historico["estatisticas"]["5_acertos"] += 1
            print("\n🚀 5 acertos!")

        elif acertos_numeros == 6:
            self.historico["estatisticas"]["6_acertos"] += 1
            print("\n🏆 6 ACERTOS!")

        # Avaliação dos trevos

        if acertos_trevos == 0:
            self.historico["estatisticas"]["0_trevos"] += 1
            print("\n❌ Nenhum trevo correto.")

        elif acertos_trevos == 1:
            self.historico["estatisticas"]["1_trevo"] += 1
            print("\n🍀 1 trevo correto!")

        elif acertos_trevos == 2:
            self.historico["estatisticas"]["2_trevos"] += 1
            print("\n🌟 2 trevos corretos!")

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
        print(f"6 acertos: {stats.get('6_acertos', 0)}")

        print(f"0 trevos corretos: {stats.get('0_trevos', 0)}")
        print(f"1 trevo correto: {stats.get('1_trevo', 0)}")
        print(f"2 trevos corretos: {stats.get('2_trevos', 0)}")

    def mostrar_historico(self):

        print("\n===== HISTÓRICO COMPLETO =====")

        print(
            json.dumps(
                self.historico,
                indent=4,
                ensure_ascii=False
            )
        )


def menu():

    agente = MilionariaAgente()

    while True:

        print("\n===== MILIONÁRIA AGENTE =====")
        print("1 - Analisar números")
        print("2 - Avaliar resultado")
        print("3 - Ver histórico")
        print("4 - Ver estatísticas")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            try:

                entrada = input(
                    "Digite 6 números entre 1 e 50: "
                )

                entrada_trevos = input(
                    "Digite 2 trevos entre 1 e 6: "
                )

                numeros = [
                    int(x) for x in entrada.split()
                ]

                trevos = [
                    int(x) for x in entrada_trevos.split()
                ]

                resultado = agente.analisar_numeros(
                    numeros,
                    trevos
                )

                print("\nNúmeros analisados:")
                print(resultado["entrada"])

                print("\nTrevos analisados:")
                print(resultado["trevos_entrada"])

                print("\nSugestão do agente:")
                print(resultado["sugestao"])

                print("\nTrevos sugeridos:")
                print(resultado["trevos_sugestao"])

            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "2":

            try:

                sorteados = input(
                    "Digite os números sorteados: "
                )

                agente_nums = input(
                    "Digite os números do agente: "
                )

                trevos_sorteados = input(
                    "Digite os trevos sorteados: "
                )

                trevos_agente = input(
                    "Digite os trevos do agente: "
                )

                numeros_sorteados = [
                    int(x) for x in sorteados.split()
                ]

                numeros_agente = [
                    int(x) for x in agente_nums.split()
                ]

                trevos_sorteados_lista = [
                    int(x) for x in trevos_sorteados.split()
                ]

                trevos_agente_lista = [
                    int(x) for x in trevos_agente.split()
                ]

                avaliacao = agente.avaliar_resultado(
                    numeros_sorteados,
                    numeros_agente,
                    trevos_sorteados_lista,
                    trevos_agente_lista
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
