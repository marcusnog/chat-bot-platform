# 📱 Guia de Configuração WhatsApp Business API

## 🎯 Configuração para Teste com Número: 85987049663

### 📋 Pré-requisitos

1. **Conta Facebook Business** ativa
2. **Número de telefone** 85987049663 cadastrado no WhatsApp Business
3. **Acesso ao Facebook Developers**

### 🔧 Passo 1: Criar Aplicação WhatsApp Business

1. **Acesse**: https://developers.facebook.com/
2. **Clique em**: "Meus Apps" → "Criar App"
3. **Selecione**: "Business" → "Continuar"
4. **Preencha**:
   - Nome do App: "WhatsApp Platform Test"
   - Email de contato: seu email
   - Categoria: "Business"

### 🔧 Passo 2: Configurar WhatsApp Business API

1. **No painel do app**, adicione o produto "WhatsApp Business API"
2. **Configure**:
   - Business Account ID: Anote este ID
   - Phone Number ID: Anote este ID
   - Access Token: Gere um token permanente

### 🔧 Passo 3: Configurar Webhook

1. **No painel WhatsApp**, vá para "Configuration"
2. **Configure Webhook**:
   - Callback URL: `https://seu-dominio.com/webhook`
   - Verify Token: Crie um token seguro (ex: `meu_token_secreto_123`)
   - Webhook Fields: Marque "messages"

### 🔧 Passo 4: Configurar Arquivo .env

Crie arquivo `.env` com suas credenciais:

```env
# WhatsApp Business API
WHATSAPP_TOKEN=seu_token_de_acesso_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id_aqui
WHATSAPP_WEBHOOK_VERIFY_TOKEN=meu_token_secreto_123
WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_account_id_aqui

# Database
DATABASE_URL=sqlite:///./whatsapp_platform.db

# OpenAI (opcional para teste)
OPENAI_API_KEY=sua_chave_openai_aqui

# Security
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Número de teste
TEST_PHONE_NUMBER=+5585987049663
```

### 🔧 Passo 5: Testar Localmente

#### Opção A: Usando ngrok (Recomendado)

1. **Instale ngrok**: https://ngrok.com/download
2. **Execute ngrok**:
   ```bash
   ngrok http 8000
   ```
3. **Copie a URL HTTPS** (ex: `https://abc123.ngrok.io`)
4. **Configure no Facebook**:
   - Callback URL: `https://abc123.ngrok.io/webhook`

#### Opção B: Servidor em nuvem

1. **Deploy em servidor** (Heroku, Railway, etc.)
2. **Configure URL pública** no webhook

### 🧪 Passo 6: Executar Testes

1. **Inicializar banco**:
   ```bash
   python src/infrastructure/database/init_db.py
   ```

2. **Executar servidor**:
   ```bash
   python src/main.py
   ```

3. **Executar testes**:
   ```bash
   python test_whatsapp_number.py
   ```

### 📱 Passo 7: Testar Envio Real

1. **Acesse**: http://localhost:8000/docs
2. **Teste endpoint**: `POST /messages/send`
3. **Payload**:
   ```json
   {
     "phone_number": "+5585987049663",
     "message": "Teste da plataforma WhatsApp!",
     "message_type": "text"
   }
   ```

### 🔍 Verificação de Funcionamento

#### ✅ Checklist de Sucesso

- [ ] Servidor rodando em http://localhost:8000
- [ ] Webhook configurado e verificado
- [ ] Token de acesso válido
- [ ] Número cadastrado no WhatsApp Business
- [ ] Mensagem enviada com sucesso
- [ ] Resposta recebida no WhatsApp

#### 🚨 Problemas Comuns

**Erro: "Invalid phone number"**
- ✅ Verifique se o número está no formato: +5585987049663
- ✅ Confirme se está cadastrado no WhatsApp Business

**Erro: "Invalid access token"**
- ✅ Gere um novo token no Facebook Developers
- ✅ Verifique se o token tem permissões corretas

**Erro: "Webhook verification failed"**
- ✅ Confirme se o token de verificação está correto
- ✅ Verifique se a URL está acessível publicamente

**Mensagem não chega**
- ✅ Verifique se o número está no WhatsApp Business
- ✅ Confirme se o webhook está configurado corretamente
- ✅ Verifique os logs do servidor

### 📊 Monitoramento

#### Logs do Servidor
```bash
# Ver logs em tempo real
tail -f logs/whatsapp_platform.log
```

#### Teste de Webhook
```bash
# Testar webhook manualmente
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook"}'
```

### 🎯 Próximos Passos

1. **Configurar OpenAI** para respostas inteligentes
2. **Implementar templates** de mensagem
3. **Adicionar mídias** (imagens, documentos)
4. **Configurar respostas automáticas**
5. **Implementar escalação** para humanos

### 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** do servidor
2. **Teste endpoints** individualmente
3. **Confirme credenciais** do WhatsApp
4. **Verifique configuração** do webhook

---

## 🎉 Sucesso!

Se tudo estiver funcionando, você receberá mensagens no WhatsApp do número **85987049663**!

**A plataforma está pronta para atendimento automático! 🚀**
