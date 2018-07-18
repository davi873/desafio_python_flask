# Desafio Python e Flask
Uma pequena aplicação desenvolida em Python, Flask e Materialcss. Aplicação cotem um serviço que observa um diretório e sempre que um novo arquivo .csv chegar, o mesmo é processado. O processamento do arquivo é a leitura do mesmo e a gravação de cada linha na tabela.


# Siga o passo a passo para executar a aplicação.
Ferramentas de desenvolvimento:
- Python v3.6.5
- Flask
- Materializecss

O projeto contem dois programas:
- Uma aplicação web
- Aplicação desktop/serviço

Passo a passo:
- Na raiz do projeto criar um ambiente virtual do python virtualenv
- Utilizar o seguinte comando para importar os módulos da aplicação: pip install -r requirements.txt
- Executar a aplicação: desafio/app/app.py
- Executar o serviço: desafio/service/service.py 

Após executar as aplicações é possível:
 - Alterar ou incluir um novo arquivo csv no diretório: desafio/service/dir para atualizar os dados da pontuação.
 - Acessar o link http://localhost:5000 para acessar a aplicação. 
