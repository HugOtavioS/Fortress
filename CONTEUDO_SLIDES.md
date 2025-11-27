# 📊 Conteúdo Textual para Slides - Fortress
## Gerenciador de Senhas com Arquitetura de Microsserviços

---

## SLIDE 1: Introdução e Contexto do Projeto

### Título
**Fortress - Gerenciador de Senhas com Arquitetura de Microsserviços**

### Conteúdo

**O que é o Fortress?**
- Sistema completo de gerenciamento de senhas
- Arquitetura baseada em microsserviços
- Projeto acadêmico desenvolvido para demonstrar conceitos avançados de desenvolvimento de software

**Objetivos do Projeto**
- Demonstrar implementação prática de arquitetura de microsserviços
- Aplicar conceitos de segurança em aplicações web
- Integrar múltiplas tecnologias de forma coordenada
- Desenvolver aplicação completa com frontend e backend separados

**Relevância Acadêmica**
- Projeto para disciplina de Backend - 2º Semestre
- Integra conhecimentos de:
  - Arquitetura de software
  - Segurança da informação
  - Desenvolvimento web
- Demonstra competências em Python, Flask e Django

---

## SLIDE 2: Arquitetura do Sistema

### Título
**Arquitetura de Microsserviços**

### Conteúdo

**Visão Geral**
Sistema composto por 4 serviços independentes que se comunicam via APIs REST

**1. Auth Service (Porta 5000)**
- Autenticação e autorização de usuários
- Cadastro, login e verificação de tokens JWT
- Banco: `auth_service.db`
- Funcionalidades: Registro, autenticação, tokens JWT (24h)

**2. Encryption Service (Porta 5002)**
- Criptografia e descriptografia de senhas
- Algoritmo Fernet (AES 128)
- Isolamento da lógica de criptografia

**3. Password Manager Service (Porta 5001)**
- Operações CRUD de senhas
- Banco: `password_manager.db`
- Validação de tokens JWT
- Isolamento de dados entre usuários

**4. Frontend Django (Porta 8000)**
- Interface web para usuários
- Consome APIs dos serviços backend
- Templates: login, registro, dashboard, CRUD de senhas

**Vantagens da Arquitetura**
- ✅ Escalabilidade independente por serviço
- ✅ Manutenibilidade com código organizado
- ✅ Testabilidade isolada de serviços
- ✅ Flexibilidade para trocar tecnologias

---

## SLIDE 3: Tecnologias e Ferramentas Utilizadas

### Título
**Stack Tecnológico**

### Conteúdo

**Backend**
- **Python 3.x** - Linguagem principal
- **Flask 2.3.3** - Framework para microsserviços
- **Django 4.2.7** - Framework para frontend

**Segurança**
- **cryptography 41.0.7** - Criptografia Fernet (AES 128)
- **PyJWT 2.8.0** - JSON Web Tokens
- **SHA-256** - Hash de senhas

**Banco de Dados**
- **SQLite** - Banco relacional leve
- Isolamento: cada serviço possui seu próprio banco

**Testes e Qualidade**
- **pytest 7.4.3** - Testes unitários e integração
- **locust 2.17.0** - Testes de carga
- **requests 2.31.0** - Comunicação HTTP

**Ferramentas**
- Git - Controle de versão
- Scripts de automação - Inicialização de serviços
- Ambiente virtual - Isolamento de dependências

**Justificativa**
- Python: versátil e amplamente utilizado
- Flask: minimalista, ideal para microsserviços
- Django: robusto para interface completa
- SQLite: simplicidade para projeto acadêmico

---

## SLIDE 4: Funcionalidades e Segurança

### Título
**Funcionalidades e Medidas de Segurança**

### Conteúdo

**Funcionalidades para Usuários**

**Gestão de Conta**
- Cadastro com validação de dados
- Login seguro com JWT
- Sessões com expiração (24 horas)

**Gerenciamento de Senhas**
- Dashboard para visualização
- Adicionar novas senhas
- Editar senhas existentes
- Deletar senhas
- Visualizar com opção mostrar/ocultar

**Interface**
- Navegação simples
- Feedback visual
- Tratamento de erros

**Medidas de Segurança**

**1. Criptografia de Dados**
- Senhas criptografadas com Fernet (AES 128)
- Nunca armazenadas em texto plano

**2. Hash de Senhas**
- SHA-256 para senhas de autenticação
- Impossibilidade de recuperação original

**3. Autenticação JWT**
- Tokens stateless
- Expiração automática (24h)
- Validação em cada requisição

**4. Isolamento de Dados**
- Usuário só acessa suas próprias senhas
- Validação de token e user_id

**5. Validação de Entrada**
- Validação rigorosa
- Prevenção de injeção SQL
- Mensagens de erro apropriadas

---

## SLIDE 5: APIs e Integração entre Serviços

### Título
**APIs REST e Comunicação entre Serviços**

### Conteúdo

**Auth Service (Porta 5000)**
- `POST /register` - Cadastro de usuário
- `POST /login` - Autenticação
- `POST /verify` - Verificação de token
- `GET /health` - Health check

**Encryption Service (Porta 5002)**
- `POST /encrypt` - Criptografar senha
- `POST /decrypt` - Descriptografar senha
- `GET /health` - Health check

**Password Manager Service (Porta 5001)**
- `GET /passwords` - Listar senhas
- `POST /passwords` - Criar senha
- `GET /passwords/{id}` - Obter senha
- `PUT /passwords/{id}` - Atualizar senha
- `DELETE /passwords/{id}` - Deletar senha
- `GET /health` - Health check

**Fluxo de Integração: Adicionar Nova Senha**

1. Usuário preenche formulário (Frontend)
2. Frontend → Password Manager (com token JWT)
3. Password Manager valida token → Auth Service
4. Password Manager → Encryption Service (criptografar)
5. Encryption Service retorna senha criptografada
6. Password Manager armazena no banco
7. Frontend recebe confirmação e atualiza interface

**Vantagens da Comunicação via API**
- ✅ Desacoplamento entre serviços
- ✅ Facilidade de testes e mock
- ✅ Substituição de serviços sem afetar outros
- ✅ Comunicação padronizada HTTP/REST

---

## SLIDE 6: Testes, Conclusões e Próximos Passos

### Título
**Testes, Resultados e Considerações Finais**

### Conteúdo

**Estratégia de Testes**

**1. Testes Unitários**
- Testes isolados por serviço
- Cobertura de funções críticas
- Mock de dependências externas

**2. Testes de Integração**
- Testes end-to-end
- Validação de fluxo completo
- Verificação de comunicação entre serviços

**3. Testes de Carga**
- Locust para simulação
- Avaliação de performance
- Identificação de gargalos

**Resultados e Aprendizados**

**Conquistas**
- ✅ Sistema funcional com microsserviços
- ✅ Segurança robusta
- ✅ Código organizado
- ✅ Documentação completa

**Desafios Enfrentados**
- Coordenação entre múltiplos serviços
- Gerenciamento de estado
- Tratamento de erros distribuídos
- Configuração de múltiplos serviços

**Aprendizados**
- Arquitetura de microsserviços na prática
- Segurança em desenvolvimento web
- Integração de tecnologias
- Boas práticas de desenvolvimento

**Próximos Passos**

**Para Produção**
- Migração para PostgreSQL/MySQL
- HTTPS/SSL
- Variáveis de ambiente
- Proxy reverso (Nginx)
- Logs e monitoramento
- Backup automatizado

**Melhorias Técnicas**
- Cache (Redis)
- Filas de mensagens
- Containerização (Docker)
- Orquestração (Kubernetes)
- CI/CD

**Funcionalidades Adicionais**
- Geração automática de senhas
- Compartilhamento seguro
- Categorização e tags
- Histórico de alterações
- Exportação/importação

**Conclusão**
O projeto Fortress demonstra com sucesso a implementação de arquitetura de microsserviços para gerenciamento de senhas, aplicando conceitos avançados de segurança, desenvolvimento web e engenharia de software.

---

## 📋 Resumo para Apresentação

**Tempo Total: 25-30 minutos**
- Apresentação: 18-22 minutos
- Perguntas: 5-7 minutos

**Dicas:**
- Use diagramas visuais quando possível
- Demonstre o sistema funcionando (se possível)
- Enfatize as medidas de segurança
- Seja honesto sobre desafios e aprendizado

