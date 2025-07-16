import osmnx as ox
from shapely.geometry import Point
from math import radians, cos, sin, asin, sqrt
import heapq
from collections import deque

#mapa da cidade com escopo global, para evitar gasto de tempo desnecessário
cidade = "Rio de Janeiro, Brasil"
custom_filter = '["highway"~"primary|secondary|tertiary"]'

G = ox.graph_from_place(cidade, network_type='walk', custom_filter=custom_filter)
area = ox.geocode_to_gdf(cidade)
areaGeo = area.iloc[0]["geometry"]


def end_valido(org, dest): # Verifica se o endereco existe na area de atuacao

    try: # verifica se o endereco passado existe
        org_point = ox.geocode(org)
        dest_point = ox.geocode(dest)

        ponto_org = Point(org_point[1], org_point[0])
        ponto_dest = Point(dest_point[1], dest_point[0])

        if areaGeo.contains(ponto_org) and areaGeo.contains(ponto_dest): # Ambos os pontos estão no Rio de Janeiro
            return True, org_point, dest_point
        
        if not areaGeo.contains(ponto_org): # se o ponto_org fica fora do rio de janeiro
            
            if "Rio" not in org: # tenta verificar se existe um endereco com mesmo nome no Rio
                org = org + ", Rio de Janeiro"
                
                try: # verifica se esse novo endereco existe
                    org_point = ox.geocode(org)
                except: # se ele nao existir
                    print("Ponto de origem fora da area de atuacao")
                    return False, None, None   
                
                ponto_org = Point(org_point[1], org_point[0]) # se ele exisitir
                
                if not areaGeo.contains(ponto_org): # verifica se o novo ponto, mais especifico, fica na cidade do Rio de Janeiro
                    print("Ponto de origem fora da area de atuacao")
                    return False, None, None     
                
        if not areaGeo.contains(ponto_dest): # se o ponto_dest fica fora do rio de janeiro
            
            if "Rio" not in dest: # tenta verificar se existe um endereco com mesmo nome no Rio
                dest = dest + ", Rio de Janeiro"
                
                try: # verifica se esse novo endereco existe
                    dest_point = ox.geocode(dest)
                except: # se ele nao existir
                    print("Ponto de destino fora da area de atuacao")
                    return False, None, None   
                
                ponto_dest = Point(dest_point[1], dest_point[0]) # se ele exisitir
                
                if not areaGeo.contains(ponto_dest): # verifica se o novo ponto, mais especifico, fica na cidade do Rio de Janeiro
                    print("Ponto de destino fora da area de atuacao")
                    return False, None, None
        
        return True, org_point, dest_point # retorna os enderecos caso eles existam e fiquem no Rio de Janeiro   
        
    except:
        print("Endereco nao encontrado")
        return False, None, None

def heu(coord1, coord2): # heuristica de distancia para o A* (distancia euclidiana no contexto planetario (levando em consideracao a curvatura))
    # basicamente recria o experimento de Eratóstenes no Egito

    # inspiracao: https://github.com/vraj152/googlemapsastar

    # graus -> radianos
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # delta latitude, longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2 # formula de Haversine
    c = 2 * asin(sqrt(a)) # angulo entre os dois pontos
    r = 6371 # raio da terra em km

    return c * r

def A(g, org, dest): # A*

    fila = []
    heapq.heappush(fila, (0, org))
    ant = {org: None}
    custo_atualizado = {org: 0}

    while fila:
        _, atual = heapq.heappop(fila)

        if atual == dest:
            break

        for vizinho in g.neighbors(atual):

            # Custo para chegar ao vizinho
            peso = g[atual][vizinho][0].get('length', 1)
            novo_custo = custo_atualizado[atual] + peso

            if vizinho not in custo_atualizado or novo_custo < custo_atualizado[vizinho]:

                custo_atualizado[vizinho] = novo_custo

                # Coordenadas dos nós
                coord_vizinho = (g.nodes[vizinho]['y'], g.nodes[vizinho]['x'])
                coord_dest = (g.nodes[dest]['y'], g.nodes[dest]['x'])
                custo_est = novo_custo + heu(coord_vizinho, coord_dest)
                heapq.heappush(fila, (custo_est, vizinho))
                ant[vizinho] = atual

    caminho = []
    atual = dest

    while atual != org:
        caminho.append(atual)
        atual = ant[atual]

    caminho.append(org)
    caminho.reverse()

    return caminho

def bidirectional_bfs(G, org, dest):

    if org == dest:
        return [org]

    # filamentos de busca e dicionários de rastreamento
    fwd_queue = deque([org])
    bwd_queue = deque([dest])
    fwd_prev = {org: None}
    bwd_prev = {dest: None}
    fwd_visited = {org}
    bwd_visited = {dest}

    # enquanto ambas as frentes tiverem nós para expandir
    while fwd_queue and bwd_queue:
        # expandir um nível da frente mais curta (balanceamento simples)
        if len(fwd_queue) <= len(bwd_queue):
            enc = bfs(G, fwd_queue, fwd_visited, fwd_prev, bwd_visited)
        else:
            enc = bfs(G, bwd_queue, bwd_visited, bwd_prev, fwd_visited)

        # se houve interseção, reconstruir o caminho
        if enc:
            return percurso(enc, fwd_prev, bwd_prev)

    # sem caminho encontrado
    return []

def bfs(G, fila, visit, prev, outros_visit):

    atual = fila.popleft()

    for vizinho in G.neighbors(atual):
        if vizinho not in visit:

            visit.add(vizinho)
            prev[vizinho] = atual
            fila.append(vizinho)

            if vizinho in outros_visit:
                return vizinho

    return None

def percurso(ponto_enc, fwd_prev, bwd_prev):

    # caminho da origem até ponto_enc
    path_fwd = []
    ver = ponto_enc
    while ver is not None:
        path_fwd.append(ver)
        ver = fwd_prev[ver]

    # caminho do destino até ponto_enc
    path_bwd = []
    ver = bwd_prev[ponto_enc]
    while ver is not None:
        path_bwd.append(ver)
        ver = bwd_prev[ver]

    return path_fwd[::-1] + path_bwd

def gerar_instrucoes(G, caminho):
    
    instrucoes = []
    idx = 0
    ultimaRua = ''
    
    for i in range(len(caminho) - 1):
        
        u = caminho[i]
        v = caminho[i + 1]
        
        
        dados_arestas = G.get_edge_data(u, v)

        for chave in dados_arestas:
            dados = dados_arestas[chave]
            nome_rua = dados.get('name', 'Rua sem nome')
            dist = dados.get('length', 0)
            if type(nome_rua) is not list:
                if nome_rua != ultimaRua:
                    ultimaRua = nome_rua
                    instrucoes.append([nome_rua, dist])
                    idx+=1
                else:
                    instrucoes[idx - 1][1] += dist

    return instrucoes

def normalizaInstrucoes(alg, caminho):
    
    instrucoes = []
    tam = 0
    
    for ins in caminho:
        instrucoes.append(f"Siga na {ins[0]} por {int(ins[1])} metros")
        tam += ins[1]
    
    print(f"{alg} tamanho: {tam}")
    return instrucoes


def principal(org, dest):

    end_enc = True

    end_enc, org_point, dest_point = end_valido(org, dest)
    
    if end_enc:
        
        orig_node = ox.distance.nearest_nodes(G, org_point[1], org_point[0])
        dest_node = ox.distance.nearest_nodes(G, dest_point[1], dest_point[0])
        
        # Algoritimo com informacao (A*)
        caminho = A(G, orig_node, dest_node)
        instrucoes = gerar_instrucoes(G, caminho)
        instrucoes = normalizaInstrucoes("A*", instrucoes)
        
        print("Caminho A*:")
        for idx, instrucao in enumerate(instrucoes, 1):
            print(f"{idx}. {instrucao}")
        
        fig, ax = ox.plot_graph_route(G, caminho, route_linewidth=4, node_size=0, bgcolor='k', route_color='green')
        
        orig_x = G.nodes[orig_node]['x']
        orig_y = G.nodes[orig_node]['y']
        dest_x = G.nodes[dest_node]['x']
        dest_y = G.nodes[dest_node]['y']

        ax.scatter([orig_x, dest_x], [orig_y, dest_y], c='green', s=50, zorder=5)
        ax.set_title("Busca com Informação (A*)", color='white')

        fig.savefig("busca_com_informacao.png", dpi=300, bbox_inches='tight')
        
        #Algoritimo sem informacao (Bidirecional)

        caminho = bidirectional_bfs(G, orig_node, dest_node)
        instrucoes = gerar_instrucoes(G, caminho)
        instrucoes = normalizaInstrucoes("BFS", instrucoes)
        
        print("\nCaminho BFS bidirecional")
        for idx, instrucao in enumerate(instrucoes, 1):
            print(f"{idx}. {instrucao}")
        
        fig, ax = ox.plot_graph_route(G, caminho, route_color='green', route_linewidth=4, node_size=0)
        ax.set_title("Busca sem Informação (BFS Bidirecional)", color='white')
        
        fig.savefig("busca_sem_informacao.png", dpi=300, bbox_inches='tight')