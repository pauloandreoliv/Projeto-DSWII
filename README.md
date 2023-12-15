# Projeto-DSWII
No mundo moderno, onde o tempo é um recurso cada vez mais valioso, as compras de supermercado frequentemente se tornam uma tarefa desafiadora e demorada. O projeto "Minha Feira: Seu Assistente de Compras" surge como uma solução inovadora para aprimorar a experiência de compras cotidianas, simplificando o processo de criação e gestão de listas de compras por meio de uma abordagem tecnológica.
O aplicativo "Minha Feira" visa proporcionar uma experiência de compra mais eficiente, prática e econômica para os usuários, economizando seu tempo valioso e contribuindo para a gestão financeira inteligente.

## 🚀 Começando
### Arquitetura do Nosso Projeto
O aplicativo Minha Feira adota a arquitetura cliente-servidor para otimizar sua estrutura. Essa escolha visa evitar complexidades desnecessárias, considerando a modelagem da aplicação.
Com isso, o Minha Feira consistirá em 3 componentes principais: o front-end, proporcionando a interface intuitiva aos usuários, o back-end com uma API para facilitar a comunicação, e o banco de dados em si, onde serão armazenadas as informações essenciais para uma experiência de compras eficiente. Essa abordagem garante um desempenho sólido e uma manutenção mais simplificada.

#### Back-end

A API Foi construída usando o framework Flask em Python. Ela permite a comunicação entre o sistemas, permitindo que eles troquem informações de maneira eficiente e estruturada por meio de endpoints específicos.
Principais rotas: 
- GET
- POST
- PUT
- DELETE

A Converção dos dados de é  para o formato JSON para que possam ser facilmente enviados e recebidos pela API.
A API interage com um banco de dados para armazenar, buscar, modificar ou excluir informações.

#### Front-End 
O desemvolvimento foi feito HTML, CSS, JavaScript

As principais telas do nosso Front-end: 

TELA DE CADASTRO 

![image](https://github.com/pauloandreoliv/Projeto-DSWII/assets/81064629/68f631d4-691b-4432-af09-f3047054e3d7)

TELA PRINCIPAL 

![image](https://github.com/pauloandreoliv/Projeto-DSWII/assets/81064629/b0697ec2-d855-4340-b7f2-a71fd92e9e48)

TELA DE MINHAS LISTAS

![image](https://github.com/pauloandreoliv/Projeto-DSWII/assets/81064629/04720406-c478-40df-996c-c7a41154ddc9)



## 🛠️Funcionalidades 
- Registro de Usuários
- Autenticação de Usuários
- Recuperação de Senha
- Acessar opções na tela Principal
- Criação de Listas de Compras
- Exclusão de Listas de Compras
- Visualização de Listas de Compras
- Adição de Itens à Lista
- Visualizar dicas
- Visualizar promoções da semana
- Obter suporte
- Cadastro de produtos
- Visualização de produto

### Diagrama de casos de uso 

![image](https://github.com/pauloandreoliv/Projeto-DSWII/assets/81064629/5d3aecbf-a504-4065-a16b-05d4e0e42809)


## 💻 Tecnologias
- Python 3.11.0: Linguagem de programação utilizada para o desenvolvimento do backend.
- Flask: Microframework web em Python utilizado para construir a aplicação e a API.
- PyJWT (JSON Web Token): Uma biblioteca que permite criar e decodificar tokens JWT, utilizada para autenticar os usuários e proteger as rotas da API.
- Python Logging Library: Utilizada na atividade de logging na API e aplicação
- Requests: Uma biblioteca em Python usada para fazer solicitações HTTP
- HTML, CSS, JavaScript: Utilizados para o desenvolvimento do frontend da aplicação.
- Firebase Firestore: Banco de dados NoSQL utilizado para armazenar dados.
- Postman: Ferramenta utilizada para realizar testes de requisições
- VSCode: IDE (Ambiente de Desenvolvimento Integrado) utilizado para codificação.
- Render.com: Plataforma utilizada para o deploy exemplificativo da API
- GitHub: Repositório

## 📌 Versão
Nosso projeto ainda esta na primeira versão. 
