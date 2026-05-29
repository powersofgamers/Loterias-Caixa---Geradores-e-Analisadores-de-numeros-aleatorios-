# 🎰 Loterias Caixa — Geradores e Analisadores de Números Aleatórios

Sistema em Python para geração, análise e avaliação de jogos das loterias da Caixa Econômica Federal.

O projeto reúne agentes inteligentes simples com histórico, estatísticas, aprendizado baseado em frequência e análise de resultados.

---

# 🚀 Recursos

✅ Geradores automáticos de números  
✅ Análise estatística simples  
✅ Histórico em JSON  
✅ Aprendizado baseado em frequência  
✅ Avaliação automática de acertos  
✅ Estatísticas acumuladas  
✅ Estrutura modular  
✅ Menu interativo via terminal  
✅ Compatível com Windows, Linux e macOS  

---

# 🎯 Loterias Implementadas

| Loteria | Arquivo |
|---|---|
| Mega-Sena | `agente_loteria.py` |
| Quina | `quina.agent.py` |
| +Milionária | `milionaria.agent.py` |

---

# 🧠 Como Funciona

Os agentes utilizam:

- geração pseudoaleatória
- frequência histórica
- reaproveitamento de padrões
- números menos utilizados
- mistura entre estratégia e aleatoriedade

O sistema salva automaticamente:

- análises
- sugestões geradas
- avaliações
- estatísticas
- histórico de desempenho

---

# 📂 Estrutura do Projeto

```bash
Loterias-Caixa/
│
├── agente_loteria.py
├── quina.agent.py
├── milionaria.agent.py
│
├── historico/
│   ├── historico.json
│   ├── historico_quina.json
│   └── historico_milionaria.json
│
└── README.md
