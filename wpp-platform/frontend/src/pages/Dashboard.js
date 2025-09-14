import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Users, 
  Clock, 
  TrendingUp, 
  Activity,
  Send,
  CheckCircle,
  AlertCircle,
  BarChart3
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalConversations: 150,
    activeConversations: 12,
    messagesToday: 45,
    responseTime: '2.3s',
    satisfaction: '4.8/5',
    aiResolutionRate: '78%'
  });

  const [recentConversations, setRecentConversations] = useState([
    {
      id: 'conv-001',
      phone: '+5585987049663',
      name: 'Cliente Teste',
      lastMessage: 'Olá, preciso de ajuda',
      time: '2 min atrás',
      status: 'active'
    },
    {
      id: 'conv-002',
      phone: '+5585999999999',
      name: 'João Silva',
      lastMessage: 'Qual o horário de funcionamento?',
      time: '5 min atrás',
      status: 'pending'
    },
    {
      id: 'conv-003',
      phone: '+5585888888888',
      name: 'Maria Santos',
      lastMessage: 'Obrigado pela ajuda!',
      time: '10 min atrás',
      status: 'resolved'
    }
  ]);

  const [chartData, setChartData] = useState([
    { name: 'Seg', messages: 45, conversations: 12 },
    { name: 'Ter', messages: 52, conversations: 15 },
    { name: 'Qua', messages: 38, conversations: 10 },
    { name: 'Qui', messages: 61, conversations: 18 },
    { name: 'Sex', messages: 48, conversations: 14 },
    { name: 'Sáb', messages: 25, conversations: 8 },
    { name: 'Dom', messages: 15, conversations: 5 }
  ]);

  const [aiMetrics, setAiMetrics] = useState([
    { name: 'Resolução Automática', value: 78, color: 'bg-green-500' },
    { name: 'Transferência Humana', value: 22, color: 'bg-blue-500' }
  ]);

  const StatCard = ({ title, value, icon: Icon, color, trend }) => (
    <div className="card">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {trend && (
            <p className="text-sm text-green-600 flex items-center">
              <TrendingUp className="h-4 w-4 mr-1" />
              {trend}
            </p>
          )}
        </div>
      </div>
    </div>
  );

  const ConversationItem = ({ conversation }) => (
    <div className="flex items-center p-3 hover:bg-gray-50 rounded-lg transition-colors">
      <div className="flex-shrink-0">
        <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
          <Users className="h-5 w-5 text-primary-600" />
        </div>
      </div>
      <div className="ml-3 flex-1">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-gray-900">{conversation.name}</p>
          <span className="text-xs text-gray-500">{conversation.time}</span>
        </div>
        <p className="text-sm text-gray-600">{conversation.lastMessage}</p>
      </div>
      <div className="ml-3">
        {conversation.status === 'active' && (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <Activity className="h-3 w-3 mr-1" />
            Ativa
          </span>
        )}
        {conversation.status === 'pending' && (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            <Clock className="h-3 w-3 mr-1" />
            Pendente
          </span>
        )}
        {conversation.status === 'resolved' && (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            <CheckCircle className="h-3 w-3 mr-1" />
            Resolvida
          </span>
        )}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Visão geral da plataforma de atendimento automático</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="h-3 w-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">Sistema Online</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Total de Conversas"
          value={stats.totalConversations}
          icon={MessageSquare}
          color="bg-primary-500"
          trend="+12% esta semana"
        />
        <StatCard
          title="Conversas Ativas"
          value={stats.activeConversations}
          icon={Activity}
          color="bg-whatsapp-500"
        />
        <StatCard
          title="Mensagens Hoje"
          value={stats.messagesToday}
          icon={Send}
          color="bg-blue-500"
          trend="+8% vs ontem"
        />
        <StatCard
          title="Tempo de Resposta"
          value={stats.responseTime}
          icon={Clock}
          color="bg-purple-500"
        />
        <StatCard
          title="Satisfação"
          value={stats.satisfaction}
          icon={CheckCircle}
          color="bg-green-500"
        />
        <StatCard
          title="Resolução IA"
          value={stats.aiResolutionRate}
          icon={TrendingUp}
          color="bg-indigo-500"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Messages Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Mensagens por Dia</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="messages" 
                stroke="#0ea5e9" 
                strokeWidth={2}
                dot={{ fill: '#0ea5e9' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* AI Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance da IA</h3>
          <div className="space-y-4">
            {aiMetrics.map((metric, index) => (
              <div key={index}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">{metric.name}</span>
                  <span className="text-sm font-semibold text-gray-900">{metric.value}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${metric.color}`}
                    style={{ width: `${metric.value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Conversations */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Conversas Recentes</h3>
          <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            Ver todas
          </button>
        </div>
        <div className="space-y-2">
          {recentConversations.map((conversation) => (
            <ConversationItem key={conversation.id} conversation={conversation} />
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-primary flex items-center justify-center">
            <Send className="h-5 w-5 mr-2" />
            Enviar Mensagem
          </button>
          <button className="btn-secondary flex items-center justify-center">
            <Users className="h-5 w-5 mr-2" />
            Ver Usuários
          </button>
          <button className="btn-secondary flex items-center justify-center">
            <BarChart3 className="h-5 w-5 mr-2" />
            Ver Analytics
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
