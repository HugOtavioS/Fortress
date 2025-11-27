# 📊 Roteiro de Apresentação Acadêmica - Fortress
## Gerenciador de Senhas com Arquitetura de Microsserviços

---

## 🎯 Estrutura da Apresentação (6 Slides)

### **SLIDE 1: Introdução e Contexto do Projeto**
**Tempo estimado: 2-3 minutos**

**Título:** Fortress - Gerenciador de Senhas com Arquitetura de Microsserviços

**Conteúdo Textual:**

**Apresentação do Projeto:**
- O Fortress é um sistema completo de gerenciamento de senhas desenvolvido como projeto acadêmico
- Implementa uma arquitetura baseada em microsserviços para demonstrar conceitos avançados de desenvolvimento de software
- Foco em segurança, escalabilidade e boas práticas de engenharia de software

**Objetivos do Projeto:**
- Demonstrar a implementação prática de arquitetura de microsserviços
- Aplicar conceitos de segurança em aplicações web (criptografia, autenticação JWT)
- Integrar múltiplas tecnologias e serviços de forma coordenada
- Desenvolver uma aplicação completa com frontend e backend separados

**Relevância Acadêmica:**
- Projeto desenvolvido para a disciplina de Backend do 2º Semestre
- Integra conhecimentos de arquitetura de software, segurança da informação e desenvolvimento web
- Demonstra competências técnicas em Python, Flask, Django e padrões de projeto

---

### **SLIDE 2: Arquitetura do Sistema**
**Tempo estimado: 3-4 minutos**

**Título:** Arquitetura de Microsserviços

**Conteúdo Textual:**

**Visão Geral da Arquitetura:**
O sistema Fortress é composto por 4 serviços independentes que se comunicam via APIs REST:

**1. Auth Service (Porta 5000)**
- Responsável pela autenticação e autorização de usuários
- Gerencia cadastro, login e verificação de tokens JWT
- Banco de dados: `auth_service.db` (SQLite)
- Funcionalidades: Registro de usuários, autenticação, geração de tokens JWT com expiração de 24 horas

**2. Encryption Service (Porta 5002)**
- Serviço dedicado exclusivamente à criptografia e descriptografia
- Utiliza algoritmo Fernet (AES 128) para criptografia simétrica
- Garante que as senhas armazenadas estejam sempre criptografadas
- Isolamento da lógica de criptografia facilita manutenção e testes

**3. Password Manager Service (Porta 5001)**
- Gerencia operações CRUD (Create, Read, Update, Delete) de senhas
- Armazena senhas criptografadas no banco `password_manager.db`
- Valida tokens JWT antes de permitir acesso aos dados
- Garante isolamento de dados entre usuários

**4. Frontend Django (Porta 8000)**
- Interface web para interação do usuário
- Consome as APIs dos serviços backend
- Templates HTML para: login, registro, dashboard, adicionar/editar senhas
- Gerencia sessões e estado da aplicação

**Vantagens da Arquitetura:**
- **Escalabilidade:** Cada serviço pode ser escalado independentemente
- **Manutenibilidade:** Código organizado por responsabilidade
- **Testabilidade:** Serviços podem ser testados isoladamente
- **Flexibilidade:** Tecnologias podem ser trocadas sem afetar outros serviços

---

### **SLIDE 3: Tecnologias e Ferramentas Utilizadas**
**Tempo estimado: 2-3 minutos**

**Título:** Stack Tecnológico

**Conteúdo Textual:**

**Backend:**
- **Python 3.x:** Linguagem principal do projeto
- **Flask 2.3.3:** Framework web leve para criação dos microsserviços
- **Django 4.2.7:** Framework full-stack para o frontend web

**Segurança:**
- **cryptography 41.0.7:** Biblioteca para criptografia Fernet (AES 128)
- **PyJWT 2.8.0:** Implementação de JSON Web Tokens para autenticação
- **SHA-256:** Algoritmo de hash para senhas de usuários

**Banco de Dados:**
- **SQLite:** Banco de dados relacional leve, ideal para desenvolvimento e demonstração
- Cada serviço possui seu próprio banco de dados para isolamento de dados

**Testes e Qualidade:**
- **pytest 7.4.3:** Framework de testes unitários e de integração
- **locust 2.17.0:** Ferramenta para testes de carga e performance
- **requests 2.31.0:** Biblioteca para comunicação HTTP entre serviços

**Ferramentas de Desenvolvimento:**
- **Git:** Controle de versão
- **Scripts de automação:** Scripts bash/batch para inicialização dos serviços
- **Ambiente virtual:** Isolamento de dependências Python

**Justificativa das Escolhas:**
- Python: Linguagem versátil, amplamente utilizada em desenvolvimento web
- Flask: Framework minimalista, ideal para microsserviços leves
- Django: Framework robusto para interface web completa
- SQLite: Simplicidade de configuração, adequado para projeto acadêmico

---

### **SLIDE 4: Funcionalidades e Segurança**
**Tempo estimado: 3-4 minutos**

**Título:** Funcionalidades e Medidas de Segurança

**Conteúdo Textual:**

**Funcionalidades para Usuários:**

**1. Gestão de Conta:**
- Cadastro de novos usuários com validação de dados
- Login seguro com autenticação JWT
- Sessões com expiração automática (24 horas)

**2. Gerenciamento de Senhas:**
- Dashboard para visualização de todas as senhas armazenadas
- Adicionar novas senhas com informações de site/serviço
- Editar senhas existentes
- Deletar senhas que não são mais necessárias
- Visualização de senhas descriptografadas com opção de mostrar/ocultar

**3. Interface Intuitiva:**
- Navegação simples e direta
- Feedback visual para ações do usuário
- Tratamento de erros com mensagens claras

**Medidas de Segurança Implementadas:**

**1. Criptografia de Dados:**
- Todas as senhas armazenadas são criptografadas usando Fernet (AES 128)
- Criptografia simétrica com chave única por instalação
- Senhas nunca são armazenadas em texto plano

**2. Hash de Senhas de Usuários:**
- Senhas de autenticação são hasheadas com SHA-256
- Impossibilidade de recuperação da senha original
- Verificação segura durante login

**3. Autenticação JWT:**
- Tokens JSON Web Token para autenticação stateless
- Expiração automática após 24 horas
- Validação em cada requisição aos serviços protegidos

**4. Isolamento de Dados:**
- Cada usuário só acessa suas próprias senhas
- Validação de token e user_id em todas as operações
- Prevenção de acesso não autorizado a dados de outros usuários

**5. Validação de Entrada:**
- Validação rigorosa de todos os dados de entrada
- Prevenção de injeção SQL e outros ataques
- Mensagens de erro apropriadas sem expor informações sensíveis

---

### **SLIDE 5: APIs e Integração entre Serviços**
**Tempo estimado: 3-4 minutos**

**Título:** APIs REST e Comunicação entre Serviços

**Conteúdo Textual:**

**APIs Disponíveis:**

**Auth Service (Porta 5000):**
- `POST /register` - Cadastro de novo usuário
  - Recebe: username, email, password
  - Retorna: token JWT, user_id, mensagem de sucesso
- `POST /login` - Autenticação de usuário
  - Recebe: username, password
  - Retorna: token JWT, user_id, dados do usuário
- `POST /verify` - Verificação de token
  - Recebe: token JWT
  - Retorna: validade do token, dados do usuário
- `GET /health` - Health check do serviço

**Encryption Service (Porta 5002):**
- `POST /encrypt` - Criptografar senha
  - Recebe: senha em texto plano
  - Retorna: senha criptografada
- `POST /decrypt` - Descriptografar senha
  - Recebe: senha criptografada
  - Retorna: senha em texto plano
- `GET /health` - Health check do serviço

**Password Manager Service (Porta 5001):**
- `GET /passwords` - Listar todas as senhas do usuário autenticado
  - Requer: token JWT no header
  - Retorna: lista de senhas (criptografadas)
- `POST /passwords` - Criar nova senha
  - Requer: token JWT, dados da senha
  - Retorna: senha criada
- `GET /passwords/{id}` - Obter senha específica
  - Requer: token JWT, ID da senha
  - Retorna: dados da senha
- `PUT /passwords/{id}` - Atualizar senha existente
  - Requer: token JWT, ID da senha, novos dados
  - Retorna: senha atualizada
- `DELETE /passwords/{id}` - Deletar senha
  - Requer: token JWT, ID da senha
  - Retorna: confirmação de exclusão
- `GET /health` - Health check do serviço

**Fluxo de Integração:**

**Exemplo: Adicionar Nova Senha**
1. Usuário preenche formulário no Frontend Django
2. Frontend envia requisição ao Password Manager Service com token JWT
3. Password Manager Service valida token com Auth Service
4. Password Manager Service envia senha ao Encryption Service para criptografar
5. Encryption Service retorna senha criptografada
6. Password Manager Service armazena senha criptografada no banco
7. Frontend recebe confirmação e atualiza a interface

**Vantagens da Comunicação via API:**
- Desacoplamento entre serviços
- Facilidade de testes e mock de serviços
- Possibilidade de substituir serviços sem afetar outros
- Comunicação padronizada via HTTP/REST

---

### **SLIDE 6: Testes, Conclusões e Próximos Passos**
**Tempo estimado: 3-4 minutos**

**Título:** Testes, Resultados e Considerações Finais

**Conteúdo Textual:**

**Estratégia de Testes:**

**1. Testes Unitários:**
- Testes para cada serviço isoladamente
- Cobertura de funções críticas (hash, criptografia, validação)
- Uso de pytest para execução automatizada
- Mock de dependências externas

**2. Testes de Integração:**
- Testes end-to-end entre múltiplos serviços
- Validação do fluxo completo de operações
- Verificação de comunicação entre serviços
- Testes de cenários de erro

**3. Testes de Carga:**
- Utilização do Locust para simulação de carga
- Avaliação de performance sob diferentes condições
- Identificação de gargalos e pontos de melhoria
- Métricas de tempo de resposta e throughput

**Resultados e Aprendizados:**

**Conquistas:**
- Sistema funcional com arquitetura de microsserviços implementada
- Segurança robusta com múltiplas camadas de proteção
- Código organizado e manutenível
- Documentação completa do projeto

**Desafios Enfrentados:**
- Coordenação entre múltiplos serviços
- Gerenciamento de estado e sessões
- Tratamento de erros em arquitetura distribuída
- Configuração e inicialização de múltiplos serviços

**Aprendizados:**
- Compreensão prática de arquitetura de microsserviços
- Aplicação de conceitos de segurança em desenvolvimento web
- Integração de diferentes tecnologias e frameworks
- Boas práticas de desenvolvimento e testes

**Próximos Passos e Melhorias Futuras:**

**Para Produção:**
- Migração para banco de dados mais robusto (PostgreSQL/MySQL)
- Implementação de HTTPS/SSL
- Uso de variáveis de ambiente para configurações sensíveis
- Implementação de proxy reverso (Nginx/Apache)
- Sistema de logs e monitoramento
- Backup automatizado de bancos de dados

**Melhorias Técnicas:**
- Implementação de cache (Redis)
- Adição de filas de mensagens para comunicação assíncrona
- Containerização com Docker
- Orquestração com Kubernetes
- Implementação de CI/CD

**Funcionalidades Adicionais:**
- Geração automática de senhas seguras
- Compartilhamento seguro de senhas entre usuários
- Categorização e tags para organização
- Histórico de alterações
- Exportação/importação de dados

**Conclusão:**
O projeto Fortress demonstra com sucesso a implementação de uma arquitetura de microsserviços para gerenciamento de senhas, aplicando conceitos avançados de segurança, desenvolvimento web e engenharia de software. O sistema serve como base sólida para aprendizado e expansão futura.

---

## 📝 Notas para Apresentação

### **Dicas de Apresentação:**
1. **Slide 1:** Comece com uma introdução clara do projeto e seu propósito acadêmico
2. **Slide 2:** Use diagramas visuais da arquitetura se possível (desenhe ou mostre um diagrama)
3. **Slide 3:** Destaque as tecnologias mais importantes e justifique as escolhas
4. **Slide 4:** Enfatize as medidas de segurança, pois são críticas para um gerenciador de senhas
5. **Slide 5:** Demonstre o fluxo de comunicação entre serviços com exemplos práticos
6. **Slide 6:** Seja honesto sobre desafios e demonstre aprendizado adquirido

### **Tempo Total Estimado:**
- Apresentação: 18-22 minutos
- Perguntas: 5-7 minutos
- **Total: 25-30 minutos**

### **Elementos Visuais Recomendados:**
- Diagrama de arquitetura mostrando os 4 serviços
- Fluxograma de comunicação entre serviços
- Screenshots da interface web (se disponível)
- Exemplos de requisições/respostas das APIs
- Gráficos de testes de carga (se disponível)

### **Pontos de Destaque:**
- Arquitetura de microsserviços bem implementada
- Múltiplas camadas de segurança
- Integração bem-sucedida de diferentes tecnologias
- Código organizado e testável
- Documentação completa

---

**Boa apresentação! 🎓**

