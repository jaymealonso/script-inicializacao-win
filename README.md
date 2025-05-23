# Script de Inicialização do Windows

Este projeto contém scripts para automatizar o processo de inicialização de ambientes de desenvolvimento ou produção.

## Funcionalidades

- Automatização de tarefas iniciais
- Configuração de variáveis de ambiente
- Instalação de dependências necessárias

## Como usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/script-inicializacao.git
    ```
2. Acesse o diretório:
    ```bash
    cd script-inicializacao
    ```
3. Renomeie o ```app-config-sample.json``` para ```app-config.json```

4. Adicione ou remova os programas do app-config.json que quer que sejam abertos na inicialização

5. Execute o script principal:
    ```bash
    ./inicializar.sh
    ```

## Requisitos

- Bash ou terminal compatível
- Permissões de execução

## Licença

Este projeto está licenciado sob a licença MIT.