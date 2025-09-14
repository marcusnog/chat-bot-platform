import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  MessageSquare,
  Users,
  Clock,
  CheckCircle,
  AlertCircle,
  Calendar,
  Download,
  Activity
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area,
  BarChart, 
  Bar,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [metrics, setMetrics] = useState({
    totalMessages: 1250,
    totalConversations: 150,
    avgResponseTime: '2.3s',
    satisfaction: '4.8/5',
    aiResolutionRate: '78%',
    activeUsers: 45
  });

  const [messageData, setMessageData] = useState([
    { name: 'Seg', messages: 45, conversations: 12 },
    { name: 'Ter', messages: 52, conversations: 15 },
    { name: 'Qua', messages: 38, conversations: 10 },
    { name: 'Qui', messages: 61, conversations: 18 },
    { name: 'Sex', messages: 48, conversations: 14 },
    { name: 'Sáb', messages: 25, conversations: 8 },
    { name: 'Dom', messages: 15, conversations: 5 }
  ]);

  const [hourlyData, setHourlyData] = useState([
    { hour: '00:00', messages: 2 },
    { hour: '01:00', messages: 1 },
    { hour: '02:00', messages: 0 },
    { hour: '03:00', messages: 0 },
    { hour: '04:00', messages: 1 },
    { hour: '05:00', messages: 2 },
    { hour: '06:00', messages: 5 },
    { hour: '07:00', messages: 8 },
    { hour: '08:00', messages: 15 },
    { hour: '09:00', messages: 22 },
    { hour: '10:00', messages: 28 },
    { hour: '11:00', messages: 25 },
    { hour: '12:00', messages: 20 },
    { hour: '13:00', messages: 18 },
    { hour: '14:00', messages: 24 },
    { hour: '15:00', messages: 30 },
    { hour: '16:00', messages: 28 },
    { hour: '17:00', messages: 22 },
    { hour: '18:00', messages: 15 },
    { hour: '19:00', messages: 12 },
    { hour: '20:00', messages: 8 },
    { hour: '21:00', messages: 5 },
    { hour: '22:00', messages: 3 },
    { hour: '23:00', messages: 2 }
  ]);

  const [aiPerformance, setAiPerformance] = useState([
    { name: 'Resolução Automática', value: 78, color: '#22c55e' },
    { name: 'Transferência Humana', value: 22, color: '#3b82f6' }
  ]);

  const [conversationTypes, setConversationTypes] = useState([
    { name: 'Suporte', value: 45, color: '#ef4444' },
    { name: 'Informações', value: 30, color: '#f59e0b' },
    { name: 'Vendas', value: 15, color: '#10b981' },
    { name: 'Outros', value: 10, color: '#6b7280' }
  ]);

  const [responseTimeData, setResponseTimeData] = useState([
    { name: 'Seg', avgTime: 2.1 },
    { name: 'Ter', avgTime: 2.3 },
    { name: 'Qua', avgTime: 1.9 },
    { name: 'Qui', avgTime: 2.5 },
    { name: 'Sex', avgTime: 2.2 },
    { name: 'Sáb', avgTime: 2.8 },
    { name: 'Dom', avgTime: 3.2 }
  ]);

  const MetricCard = ({ title, value, icon: Icon, color, trend, trendValue }) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`p-3 rounded-lg ${color}`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
          </div>
        </div>
        {trend && (
          <div className={`flex items-center text-sm ${
            trend === 'up' ? 'text-green-600' : 'text-red-600'
          }`}>
            {trend === 'up' ? (
              <TrendingUp className="h-4 w-4 mr-1" />
            ) : (
              <TrendingDown className="h-4 w-4 mr-1" />
            )}
            {trendValue}
          </div>
        )}
      </div>
    </div>
  );

  const COLORS = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Métricas e insights da plataforma</p>
        </div>
        <div className="flex items-center space-x-3">
          <select
            className="input-field"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="24h">Últimas 24h</option>
            <option value="7d">Últimos 7 dias</option>
            <option value="30d">Últimos 30 dias</option>
            <option value="90d">Últimos 90 dias</option>
          </select>
          <button className="btn-secondary flex items-center">
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MetricCard
          title="Total de Mensagens"
          value={metrics.totalMessages.toLocaleString()}
          icon={MessageSquare}
          color="bg-primary-500"
          trend="up"
          trendValue="+12%"
        />
        <MetricCard
          title="Total de Conversas"
          value={metrics.totalConversations}
          icon={Users}
          color="bg-whatsapp-500"
          trend="up"
          trendValue="+8%"
        />
        <MetricCard
          title="Tempo de Resposta Médio"
          value={metrics.avgResponseTime}
          icon={Clock}
          color="bg-purple-500"
          trend="down"
          trendValue="-5%"
        />
        <MetricCard
          title="Satisfação do Cliente"
          value={metrics.satisfaction}
          icon={CheckCircle}
          color="bg-green-500"
          trend="up"
          trendValue="+2%"
        />
        <MetricCard
          title="Taxa de Resolução IA"
          value={metrics.aiResolutionRate}
          icon={BarChart3}
          color="bg-indigo-500"
          trend="up"
          trendValue="+3%"
        />
        <MetricCard
          title="Usuários Ativos"
          value={metrics.activeUsers}
          icon={Activity}
          color="bg-blue-500"
          trend="up"
          trendValue="+15%"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Messages Over Time */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Mensagens por Dia</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={messageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="messages" 
                stroke="#0ea5e9" 
                fill="#0ea5e9"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* AI Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance da IA</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={aiPerformance}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {aiPerformance.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {aiPerformance.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center">
                  <div 
                    className="w-3 h-3 rounded-full mr-2"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-gray-700">{item.name}</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Hourly Activity */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividade por Hora</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={hourlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="messages" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Response Time */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tempo de Resposta</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={responseTimeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="avgTime" 
                stroke="#f59e0b" 
                strokeWidth={2}
                dot={{ fill: '#f59e0b' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 3 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Conversation Types */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tipos de Conversa</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={conversationTypes}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {conversationTypes.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {conversationTypes.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center">
                  <div 
                    className="w-3 h-3 rounded-full mr-2"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-gray-700">{item.name}</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Conversations vs Messages */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversas vs Mensagens</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={messageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="conversations" fill="#0ea5e9" />
              <Bar dataKey="messages" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights Automáticos</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              <span className="text-sm font-medium text-green-800">
                Performance Excelente
              </span>
            </div>
            <p className="text-sm text-green-700 mt-1">
              A taxa de resolução automática aumentou 3% esta semana.
            </p>
          </div>
          
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center">
              <TrendingUp className="h-5 w-5 text-blue-600 mr-2" />
              <span className="text-sm font-medium text-blue-800">
                Crescimento Consistente
              </span>
            </div>
            <p className="text-sm text-blue-700 mt-1">
              O volume de mensagens cresceu 12% comparado à semana anterior.
            </p>
          </div>
          
          <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
            <div className="flex items-center">
              <Clock className="h-5 w-5 text-yellow-600 mr-2" />
              <span className="text-sm font-medium text-yellow-800">
                Horário de Pico
              </span>
            </div>
            <p className="text-sm text-yellow-700 mt-1">
              Maior atividade entre 10h e 16h. Considere ajustar recursos.
            </p>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="flex items-center">
              <Users className="h-5 w-5 text-purple-600 mr-2" />
              <span className="text-sm font-medium text-purple-800">
                Novos Usuários
              </span>
            </div>
            <p className="text-sm text-purple-700 mt-1">
              15 novos usuários cadastrados esta semana.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
