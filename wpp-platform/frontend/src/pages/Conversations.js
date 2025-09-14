import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  MessageSquare, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Send,
  Phone,
  Mail,
  MoreVertical
} from 'lucide-react';

const Conversations = () => {
  const [conversations, setConversations] = useState([
    {
      id: 'conv-001',
      phone: '+5585987049663',
      name: 'Cliente Teste',
      email: 'cliente@teste.com',
      status: 'active',
      lastMessage: 'Olá, preciso de ajuda com meu pedido',
      lastActivity: '2024-01-15T10:30:00Z',
      messageCount: 5,
      unreadCount: 2,
      tags: ['suporte', 'pedido']
    },
    {
      id: 'conv-002',
      phone: '+5585999999999',
      name: 'João Silva',
      email: 'joao@email.com',
      status: 'pending',
      lastMessage: 'Qual o horário de funcionamento da loja?',
      lastActivity: '2024-01-15T09:15:00Z',
      messageCount: 3,
      unreadCount: 1,
      tags: ['informação']
    },
    {
      id: 'conv-003',
      phone: '+5585888888888',
      name: 'Maria Santos',
      email: 'maria@email.com',
      status: 'resolved',
      lastMessage: 'Obrigado pela ajuda! Problema resolvido.',
      lastActivity: '2024-01-15T08:45:00Z',
      messageCount: 8,
      unreadCount: 0,
      tags: ['resolvido']
    },
    {
      id: 'conv-004',
      phone: '+5585777777777',
      name: 'Pedro Costa',
      email: 'pedro@email.com',
      status: 'active',
      lastMessage: 'Preciso falar com o suporte técnico',
      lastActivity: '2024-01-15T11:20:00Z',
      messageCount: 2,
      unreadCount: 1,
      tags: ['suporte', 'técnico']
    }
  ]);

  const [selectedConversation, setSelectedConversation] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [messages, setMessages] = useState([]);

  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = conv.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         conv.phone.includes(searchTerm) ||
                         conv.lastMessage.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || conv.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'resolved': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return 'Ativa';
      case 'pending': return 'Pendente';
      case 'resolved': return 'Resolvida';
      default: return 'Desconhecido';
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) return `${minutes} min atrás`;
    if (hours < 24) return `${hours}h atrás`;
    return `${days} dias atrás`;
  };

  const ConversationItem = ({ conversation }) => (
    <div 
      className={`p-4 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors ${
        selectedConversation?.id === conversation.id ? 'bg-primary-50 border-primary-200' : ''
      }`}
      onClick={() => setSelectedConversation(conversation)}
    >
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
            <MessageSquare className="h-5 w-5 text-primary-600" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <p className="text-sm font-medium text-gray-900 truncate">
                {conversation.name}
              </p>
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(conversation.status)}`}>
                {getStatusText(conversation.status)}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              {conversation.unreadCount > 0 && (
                <span className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-red-500 text-xs font-medium text-white">
                  {conversation.unreadCount}
                </span>
              )}
              <span className="text-xs text-gray-500">{formatTime(conversation.lastActivity)}</span>
            </div>
          </div>
          <p className="text-sm text-gray-600 truncate mt-1">{conversation.lastMessage}</p>
          <div className="flex items-center space-x-4 mt-2">
            <div className="flex items-center text-xs text-gray-500">
              <Phone className="h-3 w-3 mr-1" />
              {conversation.phone}
            </div>
            <div className="flex items-center text-xs text-gray-500">
              <MessageSquare className="h-3 w-3 mr-1" />
              {conversation.messageCount} mensagens
            </div>
          </div>
          <div className="flex items-center space-x-1 mt-2">
            {conversation.tags.map((tag, index) => (
              <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const MessageItem = ({ message }) => (
    <div className={`flex ${message.fromCustomer ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        message.fromCustomer 
          ? 'bg-gray-200 text-gray-900' 
          : 'bg-primary-600 text-white'
      }`}>
        <p className="text-sm">{message.content}</p>
        <p className={`text-xs mt-1 ${
          message.fromCustomer ? 'text-gray-500' : 'text-primary-100'
        }`}>
          {formatTime(message.timestamp)}
        </p>
      </div>
    </div>
  );

  return (
    <div className="h-full flex">
      {/* Conversations List */}
      <div className="w-1/3 border-r border-gray-200 bg-white">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversas</h2>
          
          {/* Search and Filter */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar conversas..."
                className="input-field pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <select
              className="input-field"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">Todas as conversas</option>
              <option value="active">Ativas</option>
              <option value="pending">Pendentes</option>
              <option value="resolved">Resolvidas</option>
            </select>
          </div>
        </div>

        {/* Conversations List */}
        <div className="overflow-y-auto h-full">
          {filteredConversations.map((conversation) => (
            <ConversationItem key={conversation.id} conversation={conversation} />
          ))}
        </div>
      </div>

      {/* Conversation Detail */}
      <div className="flex-1 flex flex-col">
        {selectedConversation ? (
          <>
            {/* Conversation Header */}
            <div className="p-4 border-b border-gray-200 bg-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <MessageSquare className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {selectedConversation.name}
                    </h3>
                    <p className="text-sm text-gray-600">{selectedConversation.phone}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedConversation.status)}`}>
                    {getStatusText(selectedConversation.status)}
                  </span>
                  <button className="p-2 text-gray-400 hover:text-gray-600">
                    <MoreVertical className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
              <div className="space-y-4">
                {selectedConversation.id === 'conv-001' && (
                  <>
                    <MessageItem 
                      message={{
                        content: "Olá, preciso de ajuda com meu pedido",
                        fromCustomer: true,
                        timestamp: "2024-01-15T10:30:00Z"
                      }}
                    />
                    <MessageItem 
                      message={{
                        content: "Olá! 👋 Bem-vindo ao nosso atendimento automático!\n\nComo posso ajudá-lo hoje?",
                        fromCustomer: false,
                        timestamp: "2024-01-15T10:30:15Z"
                      }}
                    />
                    <MessageItem 
                      message={{
                        content: "Meu pedido não chegou ainda, pode verificar?",
                        fromCustomer: true,
                        timestamp: "2024-01-15T10:32:00Z"
                      }}
                    />
                    <MessageItem 
                      message={{
                        content: "Claro! Vou verificar o status do seu pedido. Pode me informar o número do pedido?",
                        fromCustomer: false,
                        timestamp: "2024-01-15T10:32:30Z"
                      }}
                    />
                  </>
                )}
              </div>
            </div>

            {/* Message Input */}
            <div className="p-4 border-t border-gray-200 bg-white">
              <div className="flex items-center space-x-3">
                <input
                  type="text"
                  placeholder="Digite sua mensagem..."
                  className="flex-1 input-field"
                />
                <button className="btn-primary">
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Selecione uma conversa
              </h3>
              <p className="text-gray-600">
                Escolha uma conversa da lista para ver as mensagens
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Conversations;
