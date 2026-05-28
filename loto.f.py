import random

def exibir_banner():
    # Cores ANSI
    ROXO = "\033[1;35m"
    RESET = "\033[0m"
    
    # Banner com letras separadas e desenho limpo para não distorcer
    banner = f"""
{ROXO}===========================================================
   ██       ██████▄  ████████▄  ██████▄    ████████
   ██       ██    ██    ██      ██    ██   ██      
   ██       ██    ██    ██      ██    ██   ██████  
   ██       ██    ██    ██      ██    ██   ██      
   ███████  ██████▀     ██      ██████▀  . ██      
                                                   
                 >> SCRIPT: loto.f.py <<           
==========================================================={RESET}"""
    print(banner)

def gerar_jogos_lotofacil():
    ROXO = "\033[1;35m"
    RESET = "\033[0m"

    # Seleciona 15 números únicos de 1 a 25
    numeros_sorteados = random.sample(range(1, 26), 15)
    numeros_sorteados.sort()
    
    # Exibe o banner corrigido
    exibir_banner()
    
    print(f" 🎲  {ROXO}NÚMEROS SORTEADOS PARA O SEU JOGO:{RESET}  🎲")
    print(f" {ROXO}-----------------------------------------------------------{RESET}")
    
    # Formata com os dois espaços para ficar organizado no terminal
    numeros_formatados = "  ".join(f"{num:02d}" for num in numeros_sorteados)
    print(f"   {ROXO}{numeros_formatados}{RESET}")
    
    print(f" {ROXO}-----------------------------------------------------------{RESET}\n")

if __name__ == "__main__":
    gerar_jogos_lotofacil()
