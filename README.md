# Implementa-o_Raft

O projeto implementa o algoritmo de consenso Raft, utilizado para gerenciar um cluster de nós distribuídos, garantindo consenso entre eles mesmo na presença de falhas. 

Possui:
Eleição de líderes: Quando nenhum líder está definido, os nós disputam o papel através de votação.
Replicação de log: Após a eleição, o líder coordena a sincronização dos logs entre os nós seguidores.
Gerenciamento de falhas: Nós podem falhar e se recuperar durante a execução, e o consenso deve ser mantido.

Instruções para Configurar o Ambiente e Executar o Código

Pré-requisitos:

Python 3.8+ instalado no sistema.
Biblioteca unittest 

Clonar o repositório com o comando:

git clone <link-do-repositorio>
cd <nome-do-repositorio>

Executar o cluster: 
Execute o arquivo principal para simular o funcionamento dos nós no cluster:

python raft_cluster.py

Executar os testes: Para validar a implementação e os cenários de teste:

python -m unittest test_raft.py


Explicação de Cada Fase do Algoritmo no Contexto da Implementação

1. Inicialização do Cluster
Cada nó inicia no estado de seguidor e aguarda um tempo limite aleatório antes de tentar se eleger.

2. Eleição de Líder
Se um nó não receber batimentos cardíacos dentro de um prazo, ele se torna candidato e solicita votos dos outros nós.
O nó que obtiver a maioria dos votos se torna o líder e começa a enviar batimentos cardíacos para os seguidores.

3. Manutenção de Consenso
O líder garante que os logs sejam consistentes em todos os nós.
Sempre que um nó seguidor detecta inconsistências, ele se sincroniza com o líder.

4. Recuperação de Nós Falhos
Um nó que falhou retorna ao estado de seguidor ao se recuperar e começa a aceitar mensagens do líder novamente.

Descrição de Possíveis Falhas Simuladas e Respostas

Falha de Nós:
Durante a execução, um nó pode ser desligado. Os demais continuam a operar, e a falha é registrada no log.
Quando o nó retorna, ele se sincroniza com o líder para atualizar seu estado.

Conexão Intermitente:
Quando um nó não responde por tempo suficiente, ele é considerado fora do cluster até que a comunicação seja restaurada.

Falha de Líder:
Se o líder falhar, uma nova eleição é iniciada entre os seguidores restantes.
Organização do Repositório

Estrutura projetada:

 README.md                   Instruções detalhadas
 requirements.txt            Dependências (se necessário)
 raft_node.py                Código do nó individual
 raft_cluster.py             Gerenciamento do cluster
 test_raft.py                Testes automatizados
 raft_logs.txt               Logs das execuções

Principais componentes requisitados:

A capacidade do algoritmo Raft de alcançar consenso.
Recuperação de falhas simuladas.
Eleição de líder e manutenção de logs consistentes.
