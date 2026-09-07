import { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { chatApi, repositoriesApi } from '../services/api';

function Chat() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState(searchParams.get('repo') || '');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingChat, setLoadingChat] = useState(true);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadChat();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChat = async () => {
    setLoadingChat(true);
    try {
      const [repositoriesResponse, historyResponse] = await Promise.all([
        repositoriesApi.list(),
        chatApi.history({ limit: 20 }),
      ]);
      setRepositories(repositoriesResponse.data);
      if (!selectedRepo && repositoriesResponse.data.length > 0) {
        setSelectedRepo(repositoriesResponse.data[0].id);
      }
      const history = [...historyResponse.data].reverse();
      setMessages(history.flatMap((item) => [
        {
          type: 'user',
          content: item.pregunta,
          timestamp: new Date(item.creado_en),
        },
        {
          type: 'assistant',
          content: item.respuesta,
          fuentes: item.documentos_fuente || [],
          timestamp: new Date(item.creado_en),
        },
      ]));
    } catch (err) {
      setError(err.response?.data?.detail || 'No se pudo cargar el chat');
    } finally {
      setLoadingChat(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loadingChat || loading) return;

    const userMessage = { type: 'user', content: input, timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await chatApi.ask({
        pregunta: currentInput,
        repositorio_id: selectedRepo,
      });

      const assistantMessage = {
        type: 'assistant',
        content: response.data.respuesta,
        fuentes: response.data.fuentes,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al enviar pregunta');
      setMessages((prev) => prev.slice(0, -1)); // Remove user message on error
    } finally {
      setLoading(false);
    }
  };

  const handleRepoChange = (repoId) => {
    setSelectedRepo(repoId);
    setSearchParams({ repo: repoId });
    setMessages([]);
  };

  return (
    <div className="h-[calc(100vh-200px)] flex flex-col">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Chat RAG</h1>
        <div className="flex items-center gap-4">
          <label className="text-sm text-gray-700">Repositorio:</label>
          <select
            value={selectedRepo}
            onChange={(e) => handleRepoChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {repositories.length === 0 && <option value="">Sin repositorios disponibles</option>}
            {repositories.map((repo) => (
              <option key={repo.id} value={repo.id}>
                {repo.nombre} ({repo.total_documentos || 0} docs)
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-white rounded-lg shadow p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p className="mt-2">Selecciona un repositorio y haz una pregunta</p>
            <p className="text-sm mt-1">La IA responderá basándose solo en tus documentos</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] ${msg.type === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-900'} rounded-lg px-4 py-2`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
              <p className={`text-xs mt-1 ${msg.type === 'user' ? 'text-indigo-100' : 'text-gray-500'}`}>
                {msg.timestamp.toLocaleTimeString()}
              </p>
              
              {msg.fuentes && msg.fuentes.length > 0 && (
                <div className="mt-3 border-t border-gray-200 pt-2">
                  <p className="text-xs font-medium text-gray-500 mb-1">Fuentes:</p>
                  <ul className="text-xs text-gray-600 space-y-1">
                    {msg.fuentes.map((fuente, i) => (
                      <li key={i} className="flex items-start gap-1">
                        <span className="font-mono bg-gray-200 px-1 rounded">[{i + 1}]</span>
                        <span>{fuente.nombre_archivo}</span>
                        <span className="text-gray-400">(similitud: {(fuente.similitud * 100).toFixed(1)}%)</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu pregunta sobre los documentos..."
          disabled={loading || loadingChat || repositories.length === 0}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-50"
        />
        <button
          type="submit"
          disabled={loading || loadingChat || !input.trim() || repositories.length === 0}
          className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Pensando...' : 'Enviar'}
        </button>
      </form>
    </div>
  );
}

export default Chat;