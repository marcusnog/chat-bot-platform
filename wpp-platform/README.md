# 🚀 WhatsApp Platform - DDD Architecture

Uma plataforma de atendimento automático via WhatsApp construída com **Domain-Driven Design (DDD)**, **SOLID Principles** e **Clean Code**.

## 📱 **Número de Teste Configurado**
- **Número**: +5585987049663
- **Formato WhatsApp**: 5585987049663
- **Display**: +55 (85) 98704-9663

## 🏗️ **Arquitetura DDD**

### **Camadas da Arquitetura**

```
src/
├── domain/                 # Camada de Domínio
│   ├── entities/          # Entidades de Negócio
│   ├── value_objects/     # Objetos de Valor
│   ├── services/          # Serviços de Domínio
│   └── repositories/      # Interfaces dos Repositórios
├── application/           # Camada de Aplicação
│   ├── use_cases/         # Casos de Uso
│   ├── dtos/              # Data Transfer Objects
│   └── interfaces/        # Interfaces de Aplicação
├── infrastructure/        # Camada de Infraestrutura
│   ├── database/          # Implementação do Banco
│   ├── repositories/      # Implementação dos Repositórios
│   └── external_services/ # Serviços Externos
└── presentation/          # Camada de Apresentação
    ├── controllers/        # Controladores FastAPI
    ├── schemas/           # Schemas Pydantic
    └── dependencies.py    # Injeção de Dependência
```

### **Princípios Aplicados**

- **✅ SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **✅ Clean Code**: Nomes significativos, funções pequenas, sem duplicação, tratamento de erros
- **✅ DDD**: Linguagem Ubíqua, Contextos Delimitados, Modelos de Domínio

## 🚀 **Início Rápido**

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Configurar Ambiente**
```bash
# Copiar arquivo de exemplo
cp config_example.env .env

# Editar com suas credenciais
# WHATSAPP_TOKEN=seu_token_aqui
# WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui
# WHATSAPP_WEBHOOK_VERIFY_TOKEN=seu_verify_token_aqui
# WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_id_aqui
```

### **3. Inicializar Banco de Dados**
```bash
python src/infrastructure/database/init_db.py
```

### **4. Executar Servidor**
```bash
python src/main.py
```

### **5. Testar API**
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Arquitetura**: http://localhost:8000/architecture

## 📋 **Funcionalidades**

### **✅ Implementadas**
- ✅ Arquitetura DDD completa
- ✅ Validação de números de telefone
- ✅ Criação de usuários
- ✅ Envio de mensagens (simulado)
- ✅ Webhook para receber mensagens
- ✅ Integração com OpenAI (GPT-3.5-turbo)
- ✅ Banco de dados SQLite/PostgreSQL
- ✅ Autenticação JWT
- ✅ Documentação automática

### **🔄 Para Configurar**
- 🔄 Credenciais WhatsApp Business API
- 🔄 Webhook do WhatsApp
- 🔄 Envio real de mensagens
- 🔄 Respostas automáticas com IA

## 📚 **Documentação**

- **[DDD Architecture](DDD_ARCHITECTURE.md)**: Documentação completa da arquitetura
- **[WhatsApp Setup](WHATSAPP_SETUP_GUIDE.md)**: Guia de configuração do WhatsApp
- **[Teste Concluído](TESTE_CONCLUIDO.md)**: Resultados dos testes realizados

## 🧪 **Testes Realizados**

### **✅ Arquitetura DDD**
- ✅ 6/6 testes passaram
- ✅ Validação de número +5585987049663
- ✅ Criação de usuário
- ✅ Envio de mensagem simulado

### **✅ Servidor**
- ✅ Online em http://localhost:8000
- ✅ Health check funcionando
- ✅ Documentação disponível
- ✅ Endpoints de teste funcionando

## 🎯 **Próximos Passos**

1. **Configure WhatsApp Business API**:
   - Acesse: https://developers.facebook.com/
   - Crie aplicação WhatsApp Business
   - Obtenha suas credenciais

2. **Configure arquivo `.env`** com suas credenciais

3. **Configure webhook** do WhatsApp

4. **Teste envio real** de mensagens

## 🛠️ **Tecnologias**

- **Python 3.8+**
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - Banco de dados
- **OpenAI GPT-3.5-turbo** - IA para respostas
- **WhatsApp Business API** - Integração WhatsApp
- **Pydantic** - Validação de dados
- **JWT** - Autenticação

## 📞 **Suporte**

Para dúvidas ou problemas:
1. Verifique a documentação em `DDD_ARCHITECTURE.md`
2. Consulte o guia de setup em `WHATSAPP_SETUP_GUIDE.md`
3. Verifique os resultados dos testes em `TESTE_CONCLUIDO.md`

---

**🎉 Plataforma pronta para uso com arquitetura DDD profissional!**