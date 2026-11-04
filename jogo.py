import requests
import random
import time

def buscar_pokemon(nome_ou_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{str(nome_ou_id).lower()}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        tipo_principal = dados["types"][0]["type"]["name"]
        return {
            "nome": dados["name"].capitalize(),
            "tipo": tipo_principal,
            "hp": dados["stats"][0]["base_stat"],
            "hp_max": dados["stats"][0]["base_stat"],
            "ataque": dados["stats"][1]["base_stat"],
            "defesa": dados["stats"][2]["base_stat"]
        }
    return None

def calcular_vantagem(tipo_atacante, tipo_defensor):
    # Relações de vantagem elementar simples
    vantagens = {
        "water": "fire",
        "fire": "grass",
        "grass": "water",
        "electric": "water",
        "ghost": "psychic"
    }
    if vantagens.get(tipo_atacante) == tipo_defensor:
        return 1.3 # Bónus de 30% de dano por vantagem de tipo
    return 1.0

def iniciar_batalha():
    print("==================================================")
    print("    BATALHA POKÉMON AVANÇADA - TERMINAL EDITION   ")
    print("==================================================")
    
    opcoes = {1: "pikachu", 2: "charizard", 3: "blastoise", 4: "venusaur", 5: "gengar"}
    
    print("\nEscolhe o teu Pokémon inicial:")
    print("1. Pikachu (Electric)\n2. Charizard (Fire)\n3. Blastoise (Water)\n4. Venusaur (Grass)\n5. Gengar (Ghost)")
    
    try:
        escolha = int(input("Digite o número do teu Pokémon (1-5): "))
    except ValueError:
        escolha = 1
        
    pkmn_jogador_id = opcoes.get(escolha, "pikachu")
    
    print("\nA carregar dados da PokéAPI...")
    jogador = buscar_pokemon(pkmn_jogador_id)
    
    # Sorteio do Oponente
    oponente_id = random.choice([p for p in opcoes.values() if p != pkmn_jogador_id])
    computador = buscar_pokemon(oponente_id)
    
    # Recursos do jogador
    pocoes = 2
    
    print(f"\n[!] Batalha iniciada: {jogador['nome']} ({jogador['tipo']}) VS {computador['nome']} ({computador['tipo']})!\n")
    time.sleep(1)
    
    while jogador["hp"] > 0 and computador["hp"] > 0:
        print("--------------------------------------------------")
        print(f"[{jogador['nome']}] HP: {jogador['hp']}/{jogador['hp_max']} | Poções: {pocoes}")
        print(f"[{computador['nome']}] HP: {computador['hp']}/{computador['hp_max']}")
        print("--------------------------------------------------")
        print("O que desejas fazer?")
        print("1. Ataque Rápido")
        print("2. Ataque Especial (Mais dano, mas pode falhar)")
        print(f"3. Usar Poção de Cura (+40 HP) [Restantes: {pocoes}]")
        
        acao = input("Escolhe a tua ação (1, 2 ou 3): ")
        
        if acao == "3":
            if pocoes > 0:
                cura = 40
                jogador["hp"] = min(jogador["hp_max"], jogador["hp"] + cura)
                pocoes -= 1
                print(f"\n-> Usaste uma poção e recuperaste {cura} de HP!\n")
            else:
                print("\n-> Já não tens poções disponíveis! Perdeste a vez.\n")
            time.sleep(1)
            
            # Turno do computador após usar poção
            dano_comp = max(10, int(computador["ataque"] * 0.4) - int(jogador["defesa"] * 0.2) + random.randint(8, 18))
            jogador["hp"] = max(0, jogador["hp"] - dano_comp)
            print(f"-> {computador['nome']} aproveitou e atacou-te, causando {dano_comp} de dano!\n")
            time.sleep(1)
            continue

        # Turno do Jogador (Ataque)
        dano_jogador = 0
        critico = False
        mult_tipo = calcular_vantagem(jogador["tipo"], computador["tipo"])
        
        if acao == "2":
            if random.random() > 0.35:
                dano_base = int(jogador["ataque"] * 0.6) - int(computador["defesa"] * 0.2) + random.randint(12, 22)
                dano_jogador = int(max(12, dano_base) * mult_tipo)
                if random.random() < 0.2: # 20% de chance de crítico
                    dano_jogador = int(dano_jogador * 1.5)
                    critico = True
                print(f"\n-> {jogador['nome']} usou um Ataque Especial!")
            else:
                print(f"\n-> {jogador['nome']} tentou o ataque especial, mas errou o golpe!")
        else:
            dano_base = int(jogador["ataque"] * 0.4) - int(computador["defesa"] * 0.2) + random.randint(6, 14)
            dano_jogador = int(max(8, dano_base) * mult_tipo)
            if random.random() < 0.15: # 15% de chance de crítico
                dano_jogador = int(dano_jogador * 1.5)
                critico = True
            print(f"\n-> {jogador['nome']} usou Ataque Rápido.")
            
        if mult_tipo > 1.0:
            print("   Vantagem de tipo! Ataque supereficaz.")
        if critico:
            print("   ACERTO CRÍTICO!")
            
        print(f"   Causaste {dano_jogador} de dano a {computador['nome']}.")
        computador["hp"] = max(0, computador["hp"] - dano_jogador)
        
        if computador["hp"] == 0:
            break
            
        time.sleep(1)
        
        # Turno do Computador
        mult_comp = calcular_vantagem(computador["tipo"], jogador["tipo"])
        dano_comp_base = int(computador["ataque"] * 0.45) - int(jogador["defesa"] * 0.2) + random.randint(10, 22)
        dano_computador = int(max(10, dano_comp_base) * mult_comp)
        
        jogador["hp"] = max(0, jogador["hp"] - dano_comp) if 'dano_comp' in locals() else max(0, jogador["hp"] - dano_computador)
        # Ajuste limpo para o dano do comp
        dano_computador = int(max(10, int(computador["ataque"] * 0.45) - int(jogador["defesa"] * 0.2) + random.randint(10, 22)) * mult_comp)
        jogador["hp"] = max(0, jogador["hp"] - dano_computador)
        
        print(f"-> {computador['nome']} contra-atacou e causou {dano_computador} de dano em ti!\n")
        time.sleep(1)

    # Fim de Jogo
    print("\n==================================================")
    print("                 FIM DE JOGO                      ")
    print("==================================================")
    if jogador["hp"] > 0:
        print(f" Parabéns! {jogador['nome']} venceu a batalha épica!")
    else:
        print(f" Derrota! {computador['nome']} foi superior desta vez. Tenta novamente!")
    print("==================================================")

if __name__ == "__main__":
    iniciar_batalha()