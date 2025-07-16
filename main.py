from agente import agenteFun

while True:
    entrada = input("Digite o caminho desejado ou 'sair' para encerrar: ")
    if entrada == 'sair':
        print("Até mais!")
        break
    else:
        agenteFun(entrada)
    