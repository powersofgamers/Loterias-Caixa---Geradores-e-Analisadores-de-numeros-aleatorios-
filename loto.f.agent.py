import os
import json
import random
from datetime import datetime

class AgenteNumerico:
    def __init__(self, pasta_historico="historico_agente"):
        self.pasta_historico = pasta_historico
        self.arquivo_pesos = os.path.join(pasta_historico, "pesos_aprendizado.json")
        self.universo_numeros = set(range(1, 26))
        
        if not os.path.exists(self.pasta_historico):
            os.makedirs(self.pasta_historico)
            
        self.pesos = self.carregar_ou_inicializar_pesos()

    def carregar_ou_inicializar_pesos(self):
        """Carrega o histórico de aprendizado ou inicializa pesos neutros para os 25 números."""
        if os.path.exists(self.arquivo_pesos):
            with open(self.arquivo_pesos, 'path', encoding='utf-8') as f:
                try:
                    # Converte as chaves de string de volta para inteiros
                    dados = json.load(f)
                    return {int(k): v for k, v in dados.items()}
                except:
                    pass
        # Se não existir, todos os números começam com peso base 1.0
        return {num: 1.0 for num in self.universo_numeros}

    def salvar_pesos(self):
        """Salva o estado atual do aprendizado."""
        with open(self.arquivo_pesos, 'w', encoding='utf-8') as f:
            json.dump(self.pesos, f, indent=4)

    def analisar_e_gerar(self, numeros_inseridos):
        """Analisa os 15 números inseridos e gera uma nova ordem/sugestão."""
        if len(numeros_inseridos) != 15 or not all(1 <= n <= 25 for n in numeros_inseridos):
            raise ValueError("Você deve fornecer exatamente 15 números únicos entre 1 e 25.")

        set_inseridos = set(numeros_inseridos)
        set_ausentes = self.universo_numeros - set_inseridos

        print(f"\n[Análise] Números fornecidos: {sorted(numeros_inseridos)}")
        print(f"[Análise] 10 Números ausentes: {sorted(list(set_ausentes))}")

        # Algoritmo de seleção baseado nos pesos do aprendizado
        # Seleciona uma mistura (ex: 9 dos inseridos e 6 dos ausentes, ajustável pelo peso)
        pool_inseridos = sorted(list(set_inseridos), key=lambda x: self.pesos[x], reverse=True)
        pool_ausentes = sorted(list(set_ausentes), key=lambda x: self.pesos[x], reverse=True)

        # Pegando os melhores avaliados de cada grupo (com uma pitada de aleatoriedade controlada)
        nova_sugestao = pool_inseridos[:9] + pool_ausentes[:6]
        
        # Garante que temos exatamente 15 e embaralha para gerar a "nova ordem"
        random.shuffle(nova_sugestao)
        
        return sorted(nova_sugestao), list(set_ausentes)

    def registrar_rodada(self, entrada, sugestao, ausentes, resultado_real=None):
        """Salva a rodada atual na pasta de histórico."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_rodada = os.path.join(self.pasta_historico, f"rodada_{timestamp}.json")
        
        dados_rodada = {
            "data": datetime.now().isoformat(),
            "entrada_usuario": entrada,
            "ausentes_analisados": ausentes,
            "sugestao_agente": sugestao,
            "resultado_real": resultado_real,
            "acertos": None
        }

        if resultado_real:
            acertos = len(set(sugestao) & set(resultado_real))
            dados_rodada["acertos"] = acertos
            self.aplicar_aprendizado(sugestao, resultado_real, acertos)

        with open(arquivo_rodada, 'w', encoding='utf-8') as f:
            json.dump(dados_rodada, f, indent=4)
        
        return dados_rodada

    def aplicar_aprendizado(self, sugestao, resultado_real, acertos):
        """Ajusta os pesos dos números baseando-se no sucesso do acerto (foco em 11 a 15)."""
        set_real = set(resultado_real)
        
        # Se o agente acertou na faixa de premiação importante (11 a 15)
        if acertos >= 11:
            print(f"🎉 Excelente! O agente cravou {acertos} acertos. Reforçando comportamento vitorioso.")
            fator_reforco = 0.2 * (acertos - 10) # Acertos maiores dão peso maior
        else:
            fator_reforco = 0.05 # Aprendizado mais lento para resultados comuns

        for num in self.universo_numeros:
            if num in set_real:
                # Se o número saiu no resultado real, ele ganha peso
                self.pesos[num] += fator_reforco
            else:
                # Se não saiu, perde um pouco de peso para balancear
                self.pesos[num] = max(0.1, self.pesos[num] - (fator_reforco / 2))
        
        self.salvar_pesos()


# --- FLUXO DE EXECUÇÃO ---
if __name__ == "__main__":
    agente = AgenteNumerico()
    
    print("--- Agente de Análise Numérica (1 a 25) ---")
    try:
        # Exemplo de entrada: digite 15 números separados por espaço
        entrada_usuario = input("Digite seus 15 números separados por espaço: ")
        numeros_usuario = [int(x) for x in entrada_usuario.split()]
        
        if len(numeros_usuario) != 15:
            # Exemplo padrão caso o usuário dê enter sem digitar tudo para testar
            print("[Info] Entrada inválida ou vazia. Usando sequência de teste simulada.")
            numeros_usuario = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        # 1. Análise e Geração
        nova_sugestao, ausentes = agente.analisar_e_gerar(numeros_usuario)
        print(f"\n🚀 [Sugestão do Agente]: {nova_sugestao}")
        
        # 2. Avaliação / Feedback de Acertos
        resposta_resultado = input("\nVocê já tem o resultado real para testar os acertos? (S/N): ")
        if resposta_resultado.upper() == 'S':
            entrada_real = input("Digite os 15 números do resultado real: ")
            resultado_real = [int(x) for x in entrada_real.split()]
            
            # Registra e aplica o aprendizado
            dados = agente.registrar_rodada(numeros_usuario, nova_sugestao, ausentes, resultado_real)
            print(f"\n📊 Avaliação Final: O agente acertou {dados['acertos']} números nesta rodada.")
            if dados['acertos'] >= 11:
                print(f"🎯 Meta atingida! Faixa de avaliação alcançada: {dados['acertos']} pontos.")
        else:
            # Salva apenas o histórico para avaliação posterior
            agente.registrar_rodada(numeros_usuario, nova_sugestao, ausentes)
            print("\n💾 Rodada salva no histórico. Você poderá computar os acertos mais tarde alterando o arquivo JSON.")
            
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
