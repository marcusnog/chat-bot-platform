import React, { useState } from 'react';
import { 
  Settings as SettingsIcon, 
  Save, 
  RefreshCw,
  MessageSquare,
  Bot,
  Shield,
  Bell,
  Globe,
  Key,
  Database,
  Zap
} from 'lucide-react';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    general: {
      platformName: 'WhatsApp Platform',
      timezone: 'America/Sao_Paulo',
      language: 'pt-BR',
      autoResponse: true
    },
    whatsapp: {
      token: 'seu_token_aqui',
      phoneNumberId: 'seu_phone_id_aqui',
      webhookVerifyToken: 'seu_verify_token_aqui',
      businessAccountId: 'seu_business_id_aqui'
    },
    ai: {
      openaiKey: 'sua_chave_openai_aqui',
      model: 'gpt-3.5-turbo',
      maxTokens: 150,
      temperature: 0.7
    },
    notifications: {
      emailNotifications: true,
      webhookNotifications: false,
      slackNotifications: false
    }
  });

  const tabs = [
    { id: 'general', name: 'Geral', icon: SettingsIcon },
    { id: 'whatsapp', name: 'WhatsApp', icon: MessageSquare },
    { id: 'ai', name: 'IA', icon: Bot },
    { id: 'notifications', name: 'Notificações', icon: Bell },
    { id: 'security', name: 'Segurança', icon: Shield }
  ];

  const handleSave = () => {
    // Implementar salvamento das configurações
    console.log('Configurações salvas:', settings);
  };

  const GeneralSettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Configurações Gerais</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome da Plataforma
            </label>
            <input
              type="text"
              className="input-field"
              value={settings.general.platformName}
              onChange={(e) => setSettings({
                ...settings,
                general: { ...settings.general, platformName: e.target.value }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fuso Horário
            </label>
            <select
              className="input-field"
              value={settings.general.timezone}
              onChange={(e) => setSettings({
                ...settings,
                general: { ...settings.general, timezone: e.target.value }
              })}
            >
              <option value="America/Sao_Paulo">São Paulo (UTC-3)</option>
              <option value="America/New_York">Nova York (UTC-5)</option>
              <option value="Europe/London">Londres (UTC+0)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Idioma
            </label>
            <select
              className="input-field"
              value={settings.general.language}
              onChange={(e) => setSettings({
                ...settings,
                general: { ...settings.general, language: e.target.value }
              })}
            >
              <option value="pt-BR">Português (Brasil)</option>
              <option value="en-US">English (US)</option>
              <option value="es-ES">Español</option>
            </select>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="autoResponse"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              checked={settings.general.autoResponse}
              onChange={(e) => setSettings({
                ...settings,
                general: { ...settings.general, autoResponse: e.target.checked }
              })}
            />
            <label htmlFor="autoResponse" className="ml-2 block text-sm text-gray-900">
              Resposta automática ativada
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  const WhatsAppSettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Configurações WhatsApp</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Token de Acesso
            </label>
            <input
              type="password"
              className="input-field"
              value={settings.whatsapp.token}
              onChange={(e) => setSettings({
                ...settings,
                whatsapp: { ...settings.whatsapp, token: e.target.value }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number ID
            </label>
            <input
              type="text"
              className="input-field"
              value={settings.whatsapp.phoneNumberId}
              onChange={(e) => setSettings({
                ...settings,
                whatsapp: { ...settings.whatsapp, phoneNumberId: e.target.value }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Webhook Verify Token
            </label>
            <input
              type="text"
              className="input-field"
              value={settings.whatsapp.webhookVerifyToken}
              onChange={(e) => setSettings({
                ...settings,
                whatsapp: { ...settings.whatsapp, webhookVerifyToken: e.target.value }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Business Account ID
            </label>
            <input
              type="text"
              className="input-field"
              value={settings.whatsapp.businessAccountId}
              onChange={(e) => setSettings({
                ...settings,
                whatsapp: { ...settings.whatsapp, businessAccountId: e.target.value }
              })}
            />
          </div>
        </div>
      </div>
    </div>
  );

  const AISettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Configurações de IA</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chave da OpenAI
            </label>
            <input
              type="password"
              className="input-field"
              value={settings.ai.openaiKey}
              onChange={(e) => setSettings({
                ...settings,
                ai: { ...settings.ai, openaiKey: e.target.value }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Modelo
            </label>
            <select
              className="input-field"
              value={settings.ai.model}
              onChange={(e) => setSettings({
                ...settings,
                ai: { ...settings.ai, model: e.target.value }
              })}
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4-turbo">GPT-4 Turbo</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Máximo de Tokens
            </label>
            <input
              type="number"
              className="input-field"
              value={settings.ai.maxTokens}
              onChange={(e) => setSettings({
                ...settings,
                ai: { ...settings.ai, maxTokens: parseInt(e.target.value) }
              })}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Temperatura (0.0 - 1.0)
            </label>
            <input
              type="number"
              step="0.1"
              min="0"
              max="1"
              className="input-field"
              value={settings.ai.temperature}
              onChange={(e) => setSettings({
                ...settings,
                ai: { ...settings.ai, temperature: parseFloat(e.target.value) }
              })}
            />
          </div>
        </div>
      </div>
    </div>
  );

  const NotificationSettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Notificações</h3>
        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="emailNotifications"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              checked={settings.notifications.emailNotifications}
              onChange={(e) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, emailNotifications: e.target.checked }
              })}
            />
            <label htmlFor="emailNotifications" className="ml-2 block text-sm text-gray-900">
              Notificações por Email
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="webhookNotifications"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              checked={settings.notifications.webhookNotifications}
              onChange={(e) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, webhookNotifications: e.target.checked }
              })}
            />
            <label htmlFor="webhookNotifications" className="ml-2 block text-sm text-gray-900">
              Notificações por Webhook
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="slackNotifications"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              checked={settings.notifications.slackNotifications}
              onChange={(e) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, slackNotifications: e.target.checked }
              })}
            />
            <label htmlFor="slackNotifications" className="ml-2 block text-sm text-gray-900">
              Notificações no Slack
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  const SecuritySettings = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Segurança</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Token de Autenticação
            </label>
            <input
              type="password"
              className="input-field"
              placeholder="admin-token-example"
              readOnly
            />
            <p className="text-sm text-gray-500 mt-1">
              Token atual usado para autenticação da API
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nova Senha
            </label>
            <input
              type="password"
              className="input-field"
              placeholder="Digite uma nova senha"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Nova Senha
            </label>
            <input
              type="password"
              className="input-field"
              placeholder="Confirme a nova senha"
            />
          </div>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'general': return <GeneralSettings />;
      case 'whatsapp': return <WhatsAppSettings />;
      case 'ai': return <AISettings />;
      case 'notifications': return <NotificationSettings />;
      case 'security': return <SecuritySettings />;
      default: return <GeneralSettings />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Configurações</h1>
          <p className="text-gray-600">Gerencie as configurações da plataforma</p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="btn-secondary flex items-center">
            <RefreshCw className="h-4 w-4 mr-2" />
            Resetar
          </button>
          <button className="btn-primary flex items-center" onClick={handleSave}>
            <Save className="h-4 w-4 mr-2" />
            Salvar
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <div className="lg:w-64">
          <nav className="space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Settings;
