# Zupit

### Tecnologias usadas no projeto
- python ^3.12
- fastapi
- postegres
- jinja
- docker

### Colaborando com o código
- Após fazer o clone do repositório é necessário entrar no ambiente virtual,
nesse caso estamos usando o `poetry` para fazer essa função
- Caso não possua o poetry recomendo a instalação via pip ou pipx
```bash
$ pip install poetry
```
- Depois de instalado precisamos baixar as dependências do projeto, ou seja,
baixar as bibliotecas que presentes no projeto com o comando:
```bash
$ poetry install
```
- Após a instalação completa devemos entrar no ambiente virtualizado gerado pelo
poetry, apenas assim nossas bibliotecas recém baixadas serão reconhecidas
```
$ poetry shell
```
- Esse ultimo passo deve ser todas as vezes que você for colaborar no código, o
restante apenas é na primeira vez estiver usando.

##### Atalhos de desenvolvimento
- Para a formatação do codigo é so escrever:
```
$ task format
```
- Para testar o codigo é so escrever:
```
$ task test
```
- Para rodar o servidor basta escrever:
```
$ task run
```

### Subindo a aplicação.
- Para mitigar problemas envolvendo configurações específicas de computador,
optamos por utilizar o `docker` para fazer a conteinerização da aplicação e do
banco de dados.

- Caso não possua `docker` e `docker-compose` recomendo que aprenda a instalação
na documentação deles

- Para colocar a aplicação no em loopback:
```bash
$ docker-compose up
```

- Caso queira parar a aplicação:
```
$ docker-compose down
```

