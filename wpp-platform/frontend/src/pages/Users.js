import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import { 
  Search, 
  Filter, 
  Users as UsersIcon, 
  Phone, 
  Mail, 
  Calendar,
  Activity,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Plus,
  MessageSquare
} from 'lucide-react';

const Users = () => {
  const { getAuthHeaders } = useAuth();
  const [users, setUsers] = useState([
    {
      id: 'user-001',
      name: 'Cliente Teste',
      phone: '+5585987049663',
      email: 'cliente@teste.com',
      isActive: true,
      createdAt: '2024-01-10T10:30:00Z',
      lastActivity: '2024-01-15T10:30:00Z',
      conversationCount: 5,
      totalMessages: 25
    },
    {
      id: 'user-002',
      name: 'João Silva',
      phone: '+5585999999999',
      email: 'joao@email.com',
      isActive: true,
      createdAt: '2024-01-12T14:20:00Z',
      lastActivity: '2024-01-15T09:15:00Z',
      conversationCount: 3,
      totalMessages: 12
    },
    {
      id: 'user-003',
      name: 'Maria Santos',
      phone: '+5585888888888',
      email: 'maria@email.com',
      isActive: false,
      createdAt: '2024-01-08T16:45:00Z',
      lastActivity: '2024-01-14T08:45:00Z',
      conversationCount: 8,
      totalMessages: 35
    },
    {
      id: 'user-004',
      name: 'Pedro Costa',
      phone: '+5585777777777',
      email: 'pedro@email.com',
      isActive: true,
      createdAt: '2024-01-13T11:20:00Z',
      lastActivity: '2024-01-15T11:20:00Z',
      conversationCount: 2,
      totalMessages: 8
    },
    {
      id: 'user-005',
      name: 'Ana Oliveira',
      phone: '+5585666666666',
      email: 'ana@email.com',
      isActive: true,
      createdAt: '2024-01-14T09:30:00Z',
      lastActivity: '2024-01-15T12:15:00Z',
      conversationCount: 1,
      totalMessages: 4
    }
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedUser, setSelectedUser] = useState(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar dados dos usuários
  useEffect(() => {
    const loadUsers = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const usersData = await apiService.getUsers({
          skip: 0,
          limit: 100
        });
        
        // Converter dados da API para o formato esperado
        const formattedUsers = usersData.map(user => ({
          id: user.id,
          name: user.name,
          phone: user.phone,
          email: user.email,
          isActive: user.is_active,
          createdAt: user.created_at,
          lastActivity: user.last_activity,
          conversationCount: user.conversation_count,
          totalMessages: user.total_messages
        }));
        
        setUsers(formattedUsers);
      } catch (err) {
        setError('Erro ao carregar usuários');
        console.error('Erro ao carregar usuários:', err);
        // Manter dados mockados em caso de erro
      } finally {
        setIsLoading(false);
      }
    };
    
    loadUsers();
  }, []);

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.phone.includes(searchTerm) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || 
                         (statusFilter === 'active' && user.isActive) ||
                         (statusFilter === 'inactive' && !user.isActive);
    return matchesSearch && matchesStatus;
  });

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('pt-BR');
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

  const handleUserClick = (user) => {
    setSelectedUser(user);
    setShowUserModal(true);
  };

  const UserCard = ({ user }) => (
    <div className="card hover:shadow-md transition-shadow cursor-pointer" onClick={() => handleUserClick(user)}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <div className="h-12 w-12 bg-primary-100 rounded-full flex items-center justify-center">
            <UsersIcon className="h-6 w-6 text-primary-600" />
          </div>
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <h3 className="text-lg font-semibold text-gray-900">{user.name}</h3>
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                user.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {user.isActive ? 'Ativo' : 'Inativo'}
              </span>
            </div>
            <div className="mt-2 space-y-1">
              <div className="flex items-center text-sm text-gray-600">
                <Phone className="h-4 w-4 mr-2" />
                {user.phone}
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <Mail className="h-4 w-4 mr-2" />
                {user.email}
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <Calendar className="h-4 w-4 mr-2" />
                Cadastrado em {formatDate(user.createdAt)}
              </div>
            </div>
            <div className="mt-3 flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center">
                <MessageSquare className="h-4 w-4 mr-1" />
                {user.conversationCount} conversas
              </div>
              <div className="flex items-center">
                <Activity className="h-4 w-4 mr-1" />
                {user.totalMessages} mensagens
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Última atividade: {formatTime(user.lastActivity)}
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <Eye className="h-4 w-4" />
          </button>
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <Edit className="h-4 w-4" />
          </button>
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <MoreVertical className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );

  const UserModal = ({ user, isOpen, onClose }) => {
    if (!isOpen || !user) return null;

    return (
      <div className="fixed inset-0 z-50 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>
          
          <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <div className="h-12 w-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <UsersIcon className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{user.name}</h3>
                  <p className="text-sm text-gray-600">{user.email}</p>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center text-sm">
                  <Phone className="h-4 w-4 mr-2 text-gray-400" />
                  <span className="text-gray-900">{user.phone}</span>
                </div>
                <div className="flex items-center text-sm">
                  <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                  <span className="text-gray-900">Cadastrado em {formatDate(user.createdAt)}</span>
                </div>
                <div className="flex items-center text-sm">
                  <Activity className="h-4 w-4 mr-2 text-gray-400" />
                  <span className="text-gray-900">Última atividade: {formatTime(user.lastActivity)}</span>
                </div>
                <div className="flex items-center text-sm">
                  <MessageSquare className="h-4 w-4 mr-2 text-gray-400" />
                  <span className="text-gray-900">{user.conversationCount} conversas, {user.totalMessages} mensagens</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="button"
                className="btn-primary w-full sm:w-auto sm:ml-3"
                onClick={onClose}
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Usuários</h1>
          <p className="text-gray-600">Gerencie todos os usuários da plataforma</p>
        </div>
        <button className="btn-primary flex items-center">
          <Plus className="h-5 w-5 mr-2" />
          Novo Usuário
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-primary-500">
              <UsersIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total de Usuários</p>
              <p className="text-2xl font-semibold text-gray-900">{users.length}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-500">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Usuários Ativos</p>
              <p className="text-2xl font-semibold text-gray-900">
                {users.filter(u => u.isActive).length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-500">
              <MessageSquare className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total de Conversas</p>
              <p className="text-2xl font-semibold text-gray-900">
                {users.reduce((sum, user) => sum + user.conversationCount, 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
          <div className="flex-1 max-w-lg">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar usuários..."
                className="input-field pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <select
              className="input-field"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">Todos os usuários</option>
              <option value="active">Ativos</option>
              <option value="inactive">Inativos</option>
            </select>
            <button className="btn-secondary flex items-center">
              <Filter className="h-4 w-4 mr-2" />
              Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="card text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando usuários...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="card bg-red-50 border-red-200">
          <div className="flex items-center">
            <div className="text-red-600 mr-3">
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      {/* Users Grid */}
      {!isLoading && !error && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredUsers.length > 0 ? (
            filteredUsers.map((user) => (
              <UserCard key={user.id} user={user} />
            ))
          ) : (
            <div className="col-span-full card text-center py-12">
              <UsersIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum usuário encontrado</h3>
              <p className="text-gray-600">Tente ajustar os filtros de busca.</p>
            </div>
          )}
        </div>
      )}

      {/* User Modal */}
      <UserModal 
        user={selectedUser} 
        isOpen={showUserModal} 
        onClose={() => setShowUserModal(false)} 
      />
    </div>
  );
};

export default Users;
