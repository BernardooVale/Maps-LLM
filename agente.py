from smolagents import LiteLLMModel, tool, ToolCallingAgent
from mapas import principal
   
@tool
def calcular_rota_Tool(origem: str, destino: str) -> None:
    """
    Only function that can find a path between two points in Rio de Janeiro.
    As long as you know both the start end end points use this function.
    
    Args:
        origem (str): Starting point
        destino (str): End point

    Returns:
        str: None
    """
    principal(origem, destino)

def agenteFun(entrada):
    
    modelo = LiteLLMModel(
        model_id="ollama_chat/qwen2:7b",
        api_base="http://localhost:11434",
        num_ctx=8192
    )

    agente = ToolCallingAgent(
        tools=[calcular_rota_Tool],
        model=modelo,
        add_base_tools=False,
        max_steps=1,
    )
    
    tarefa = f"""
        Sua funcao e extrair os pontos de partida e chegada de uma entrada em linguagem natural e enviar para a funcao calcular_rota_Tool que fara todo o resto e nao retornara nada.
        Voce esta estritamente proibido de gerar qualquer codigo além de chamar a funcao calcular_rota_Tool(origem, destino), onde origem e o ponto de partida e destino o ponto de chegada.
        Voce nao precisa de retornar uma final_answer
        
        Exemplo de como chamar a função calcular_rota_Tool corretamente:

        {{
            "name": "calcular_rota_Tool",
            "arguments": {{
                "origem": "Ponto de partida extraido",
                "destino": "Ponto de chegada extraido"
            }}
        }}
        
        A mensagem do usuario foi: {entrada}
    """
    
    agente.run(tarefa)