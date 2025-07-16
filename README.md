# Maps-LLM

A project developed for the **Introduction to Artificial Intelligence** course at the Federal University of Minas Gerais (UFMG), Brazil.

This application allows users to request routes between two locations using **natural language**. Through the use of **agents** and **Large Language Models (LLMs)**, the system extracts relevant information such as the **origin** and **destination**, and uses it to search for a path using two classic search algorithms:

- **A\*** (informed search)
- **Bidirectional BFS** (uninformed search)

---

## 🌐 Project Overview

### 🧠 What it does

- Accepts **natural language input** from the user (e.g., “How do I get from Copacabana to Maracanã?”)
- Uses an **LLM-based agent** to extract structured data: **start point** and **end point**
- Computes the path using two search strategies:
  - **A\***: Uses heuristics (informed search)
  - **Bidirectional BFS**: Explores from both ends until paths meet (uninformed search)
- Returns and optionally compares both paths

### ⚙️ Technologies

- Python
- Natural Language Processing (via LLMs)
- Search algorithms: A\*, Bidirectional BFS
- Agents for language understanding

---

## 📁 Visão Geral do Projeto

### 🧠 O que o projeto faz

- Recebe uma **pergunta em linguagem natural** do usuário (ex: “Como vou da Urca até o Maracanã?”)
- Utiliza um **agente baseado em LLM** para extrair os dados estruturados: **origem** e **destino**
- Realiza a busca de caminho entre os dois pontos usando dois algoritmos clássicos:
  - **A\***: busca informada com heurística
  - **BFS Bidirecional**: busca não informada que parte dos dois extremos até se encontrar
- Exibe e compara os caminhos encontrados por cada estratégia

### ⚙️ Tecnologias

- Python
- Processamento de Linguagem Natural com LLMs
- Algoritmos de busca: A\*, BFS Bidirecional
- Agentes inteligentes para interpretação de linguagem

---

## 🏫 Institution

Federal University of Minas Gerais (UFMG)  
Discipline: Introduction to Artificial Intelligence

---
