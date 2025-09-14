# 🚀 WhatsApp Platform Frontend

Interface React moderna e profissional para a Plataforma de Atendimento Automático WhatsApp.

## ✨ **Funcionalidades**

### 📊 **Dashboard**
- Visão geral da plataforma
- Métricas em tempo real
- Gráficos interativos
- Conversas recentes
- Ações rápidas

### 💬 **Conversas**
- Lista de conversas ativas
- Interface de chat em tempo real
- Filtros e busca
- Status das conversas
- Histórico completo

### 👥 **Usuários**
- Gestão de usuários cadastrados
- Informações detalhadas
- Filtros por status
- Estatísticas por usuário

### 📈 **Analytics**
- Métricas detalhadas
- Gráficos interativos
- Insights automáticos
- Exportação de dados
- Análise de performance

### ⚙️ **Configurações**
- Configurações gerais
- Integração WhatsApp
- Configurações de IA
- Notificações
- Segurança

## 🛠️ **Tecnologias**

- **React 18** - Framework principal
- **React Router** - Navegação
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos
- **Lucide React** - Ícones
- **Axios** - Requisições HTTP
- **React Hot Toast** - Notificações
- **Framer Motion** - Animações

## 🚀 **Instalação**

### **1. Instalar Dependências**
```bash
npm install
```

### **2. Executar em Desenvolvimento**
```bash
npm start
```

### **3. Build para Produção**
```bash
npm run build
```

## 📱 **Responsividade**

- ✅ **Mobile First** - Otimizado para dispositivos móveis
- ✅ **Tablet** - Layout adaptado para tablets
- ✅ **Desktop** - Interface completa para desktop
- ✅ **Sidebar** - Navegação colapsável em mobile

## 🎨 **Design System**

### **Cores**
- **Primary**: Azul (#0ea5e9)
- **WhatsApp**: Verde (#22c55e)
- **Success**: Verde (#10b981)
- **Warning**: Amarelo (#f59e0b)
- **Error**: Vermelho (#ef4444)

### **Componentes**
- **Cards** - Containers de conteúdo
- **Buttons** - Botões primários e secundários
- **Inputs** - Campos de entrada
- **Sidebar** - Navegação lateral
- **Charts** - Gráficos interativos

## 🔗 **Integração com Backend**

A interface se conecta automaticamente com o backend em `http://localhost:8000` através do proxy configurado no `package.json`.

### **Endpoints Utilizados**
- `GET /conversations` - Lista conversas
- `GET /users` - Lista usuários
- `GET /analytics` - Métricas
- `POST /messages/send` - Enviar mensagens

## 📊 **Gráficos e Métricas**

### **Recharts**
- **LineChart** - Tendências temporais
- **BarChart** - Comparações
- **AreaChart** - Áreas preenchidas
- **PieChart** - Distribuições
- **ResponsiveContainer** - Responsividade

### **Métricas Disponíveis**
- Total de mensagens
- Conversas ativas
- Tempo de resposta
- Satisfação do cliente
- Taxa de resolução IA
- Usuários ativos

## 🎯 **Funcionalidades Principais**

### **Dashboard**
- Cards de métricas
- Gráficos de atividade
- Conversas recentes
- Ações rápidas

### **Conversas**
- Lista filtrada
- Interface de chat
- Status em tempo real
- Busca avançada

### **Usuários**
- Grid de usuários
- Filtros por status
- Informações detalhadas
- Ações em lote

### **Analytics**
- Múltiplos gráficos
- Filtros temporais
- Insights automáticos
- Exportação de dados

### **Configurações**
- Abas organizadas
- Validação de formulários
- Salvamento automático
- Configurações por categoria

## 🔧 **Desenvolvimento**

### **Estrutura de Arquivos**
```
src/
├── components/     # Componentes reutilizáveis
├── pages/         # Páginas principais
├── services/      # Serviços de API
├── hooks/         # Custom hooks
├── utils/         # Utilitários
└── assets/        # Recursos estáticos
```

### **Componentes Principais**
- `Layout` - Layout principal com sidebar
- `Dashboard` - Página inicial
- `Conversations` - Gestão de conversas
- `Users` - Gestão de usuários
- `Analytics` - Métricas e gráficos
- `Settings` - Configurações

## 🚀 **Deploy**

### **Build de Produção**
```bash
npm run build
```

### **Servir Arquivos Estáticos**
```bash
npx serve -s build
```

### **Deploy em Vercel**
```bash
vercel --prod
```

## 📱 **Preview**

Acesse `http://localhost:3000` para ver a interface em funcionamento.

### **Telas Principais**
- **Dashboard**: `http://localhost:3000/`
- **Conversas**: `http://localhost:3000/conversations`
- **Usuários**: `http://localhost:3000/users`
- **Analytics**: `http://localhost:3000/analytics`
- **Configurações**: `http://localhost:3000/settings`

---

**🎉 Interface moderna e profissional para sua plataforma de atendimento automático!**
