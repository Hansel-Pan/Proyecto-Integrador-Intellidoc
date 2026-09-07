import { useState, useEffect } from 'react';
import { dashboardApi } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const [summaryRes, logsRes] = await Promise.all([
        dashboardApi.summary(),
        dashboardApi.logs({ limit: 20 }),
      ]);
      setStats(summaryRes.data);
      setLogs(logsRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!stats) {
    return <div className="text-center py-12">No hay datos disponibles</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-4" aria-label="Tabs">
          <button
            onClick={() => setActiveTab('summary')}
            className={`py-2 px-4 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'summary'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Resumen
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            className={`py-2 px-4 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'logs'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Logs de errores
          </button>
        </nav>
      </div>

      {activeTab === 'summary' && (
        <div className="space-y-6">
          {/* Key metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Total repositorios"
              value={stats.total_repositorios}
              icon={FolderIcon}
              color="indigo"
            />
            <MetricCard
              title="Total documentos"
              value={stats.total_documentos}
              icon={FileIcon}
              color="green"
            />
            <MetricCard
              title="Usuarios"
              value={stats.total_usuarios}
              icon={UsersIcon}
              color="blue"
            />
            <MetricCard
              title="Errores recientes"
              value={stats.errores_recientes.length}
              icon={AlertIcon}
              color="red"
            />
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Documentos por categoría" data={stats.documentos_por_categoria}>
              <CategoryChart data={stats.documentos_por_categoria} />
            </ChartCard>
            <ChartCard title="Documentos por estado" data={stats.documentos_por_estado}>
              <StatusChart data={stats.documentos_por_estado} />
            </ChartCard>
          </div>

          {/* Recent errors */}
          {stats.errores_recientes.length > 0 && (
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Errores recientes</h2>
              </div>
              <div className="divide-y divide-gray-200">
                {stats.errores_recientes.map((err, i) => (
                  <div key={i} className="px-6 py-4 hover:bg-gray-50">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{err.nombre_archivo}</p>
                        <p className="text-sm text-gray-600 mt-1">{err.mensaje}</p>
                        <p className="text-xs text-gray-400 mt-1">
                          {new Date(err.creado_en).toLocaleString()} · {err.tipo}
                        </p>
                      </div>
                      <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded">
                        {err.tipo}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'logs' && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Logs de procesamiento</h2>
          </div>
          {logs.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p className="mt-2">No hay logs de error registrados</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Documento</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Mensaje</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {logs.map((log, i) => (
                    <tr key={i} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm text-gray-900">{log.nombre_archivo}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded">{log.tipo}</span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 max-w-md truncate">{log.mensaje}</td>
                      <td className="px-6 py-4 text-sm text-gray-500">{new Date(log.creado_en).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Components
function MetricCard({ title, value, icon: Icon, color }) {
  const colors = {
    indigo: 'bg-indigo-50 text-indigo-600 border-indigo-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    red: 'bg-red-50 text-red-600 border-red-200',
  };
  
  return (
    <div className={`bg-white rounded-lg shadow p-6 border ${colors[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <Icon className={`h-12 w-12 ${colors[color].split(' ')[1]}`} />
      </div>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="h-64">{children}</div>
    </div>
  );
}

function CategoryChart({ data }) {
  const entries = Object.entries(data || {});
  const max = Math.max(...entries.map(([, v]) => v), 1);
  
  return (
    <div className="flex items-end justify-center gap-4 h-full">
      {entries.map(([cat, count]) => (
        <div key={cat} className="flex flex-col items-center flex-1">
          <div
            className="w-full bg-indigo-500 rounded-t transition-all duration-500"
            style={{ height: `${(count / max) * 100}%`, minHeight: '4px' }}
          />
          <span className="text-xs text-gray-600 mt-2 text-center truncate w-20">{cat}</span>
          <span className="text-sm font-medium text-gray-900">{count}</span>
        </div>
      ))}
    </div>
  );
}

function StatusChart({ data }) {
  const entries = Object.entries(data || {});
  const colors = {
    procesado: 'bg-green-500',
    procesando: 'bg-blue-500',
    pendiente: 'bg-gray-400',
    error: 'bg-red-500',
  };
  const max = Math.max(...entries.map(([, v]) => v), 1);
  
  return (
    <div className="flex items-end justify-center gap-4 h-full">
      {entries.map(([status, count]) => (
        <div key={status} className="flex flex-col items-center flex-1">
          <div
            className={`w-full rounded-t transition-all duration-500 ${colors[status] || 'bg-gray-400'}`}
            style={{ height: `${(count / max) * 100}%`, minHeight: '4px' }}
          />
          <span className="text-xs text-gray-600 mt-2 text-center capitalize">{status}</span>
          <span className="text-sm font-medium text-gray-900">{count}</span>
        </div>
      ))}
    </div>
  );
}

// Icons
function FolderIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
    </svg>
  );
}

function FileIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
    </svg>
  );
}

function UsersIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  );
}

function AlertIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  );
}

export default Dashboard;