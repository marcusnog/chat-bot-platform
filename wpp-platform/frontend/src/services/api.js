/**
 * Serviço de API para conectar frontend com backend
 */
class ApiService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  }

  // Método genérico para fazer requisições
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = localStorage.getItem('token');
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    };

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Autenticação
  async login(email, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async verifyToken() {
    return this.request('/auth/verify-token');
  }

  // Usuários
  async getUsers(params = {}) {
    const queryParams = new URLSearchParams(params);
    return this.request(`/users?${queryParams}`);
  }

  async getUser(userId) {
    return this.request(`/users/${userId}`);
  }

  async createUser(userData) {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(userId, userData) {
    return this.request(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(userId) {
    return this.request(`/users/${userId}`, {
      method: 'DELETE',
    });
  }

  async getUserStats() {
    return this.request('/users/stats');
  }

  // Conversas
  async getConversations(params = {}) {
    const queryParams = new URLSearchParams(params);
    return this.request(`/conversations?${queryParams}`);
  }

  async getConversation(conversationId) {
    return this.request(`/conversations/${conversationId}`);
  }

  async createConversation(conversationData) {
    return this.request('/conversations', {
      method: 'POST',
      body: JSON.stringify(conversationData),
    });
  }

  async updateConversation(conversationId, conversationData) {
    return this.request(`/conversations/${conversationId}`, {
      method: 'PUT',
      body: JSON.stringify(conversationData),
    });
  }

  async deleteConversation(conversationId) {
    return this.request(`/conversations/${conversationId}`, {
      method: 'DELETE',
    });
  }

  async getConversationStats() {
    return this.request('/conversations/stats');
  }

  // Mensagens
  async getMessages(params = {}) {
    const queryParams = new URLSearchParams(params);
    return this.request(`/messages?${queryParams}`);
  }

  async getMessage(messageId) {
    return this.request(`/messages/${messageId}`);
  }

  async createMessage(messageData) {
    return this.request('/messages', {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }

  async updateMessage(messageId, messageData) {
    return this.request(`/messages/${messageId}`, {
      method: 'PUT',
      body: JSON.stringify(messageData),
    });
  }

  async deleteMessage(messageId) {
    return this.request(`/messages/${messageId}`, {
      method: 'DELETE',
    });
  }

  async getMessageStats() {
    return this.request('/messages/stats');
  }

  // Analytics
  async getAnalyticsOverview() {
    return this.request('/analytics/overview');
  }

  async getMessageTrends(days = 7) {
    return this.request(`/analytics/message-trends?days=${days}`);
  }

  async getUserActivity(days = 7) {
    return this.request(`/analytics/user-activity?days=${days}`);
  }

  async getConversationMetrics() {
    return this.request('/analytics/conversation-metrics');
  }

  async getResponseTimes() {
    return this.request('/analytics/response-times');
  }

  // Configurações
  async getSettings() {
    return this.request('/settings');
  }

  async updateSettings(settingsData) {
    return this.request('/settings', {
      method: 'PUT',
      body: JSON.stringify(settingsData),
    });
  }

  async testAI(testData) {
    return this.request('/settings/test-ai', {
      method: 'POST',
      body: JSON.stringify(testData),
    });
  }

  async testWhatsApp(testData) {
    return this.request('/settings/test-whatsapp', {
      method: 'POST',
      body: JSON.stringify(testData),
    });
  }

  async getHealthCheck() {
    return this.request('/settings/health');
  }

  async resetDatabase() {
    return this.request('/settings/reset-database', {
      method: 'POST',
    });
  }
}

// Instância singleton
const apiService = new ApiService();
export default apiService;
