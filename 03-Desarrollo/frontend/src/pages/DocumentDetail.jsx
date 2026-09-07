import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { documentsApi } from '../services/api';

function DocumentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDocument();
  }, [id]);

  const loadDocument = async () => {
    try {
      setLoading(true);
      const response = await documentsApi.get(id);
      setDocument(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar documento');
    } finally {
      setLoading(false);
    }
  };

  const downloadDocument = async () => {
    if (!document) return;
    try {
      const response = await documentsApi.download(id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', document.nombre_archivo);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Error al descargar');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`¿Eliminar "${document.nombre_archivo}"?`)) return;
    
    try {
      await documentsApi.delete(id);
      navigate('/repositories');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al eliminar');
    }
  };

  const getEstadoBadge = (estado) => {
    const styles = {
      pendiente: 'bg-gray-100 text-gray-800',
      procesando: 'bg-blue-100 text-blue-800',
      procesado: 'bg-green-100 text-green-800',
      error: 'bg-red-100 text-red-800',
    };
    return styles[estado] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!document) {
    return <div className="text-center py-12">Documento no encontrado</div>;
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <Link
            to={`/repositories/${document.repositorio_id}`}
            className="text-sm text-gray-500 hover:text-gray-700 mb-2 inline-block"
          >
            ← Volver al repositorio
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">{document.nombre_archivo}</h1>
          <p className="text-sm text-gray-500">
            Subido: {new Date(document.creado_en).toLocaleDateString()}
            {document.procesado_en && ` · Procesado: ${new Date(document.procesado_en).toLocaleDateString()}`}
          </p>
        </div>
        <div className="flex gap-2">
          <button onClick={downloadDocument} className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
            Descargar
          </button>
          <button onClick={handleDelete} className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            Eliminar
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
          {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Status & Meta */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Información general</h2>
            <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt className="text-sm text-gray-500">Estado</dt>
                <dd className="mt-1">
                  <span className={`px-3 py-1 text-sm rounded-full ${getEstadoBadge(document.estado)}`}>
                    {document.estado}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">Formato</dt>
                <dd className="mt-1 text-sm text-gray-900">{document.formato.toUpperCase()}</dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">Categoría</dt>
                <dd className="mt-1 text-sm text-gray-900">{document.categoria || 'Sin clasificar'}</dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">Repositorio</dt>
                <dd className="mt-1 text-sm text-gray-900">ID: {document.repositorio_id}</dd>
              </div>
            </dl>
          </div>

          {/* Resumen */}
          {document.resumen && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Resumen</h2>
              <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                {document.resumen}
              </div>
            </div>
          )}

          {/* Campos extraídos */}
          {document.campos_extraidos && Object.keys(document.campos_extraidos).length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Campos extraídos</h2>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(document.campos_extraidos).map(([key, value]) => (
                  <div key={key}>
                    <dt className="text-sm text-gray-500 capitalize">{key.replace(/_/g, ' ')}</dt>
                    <dd className="mt-1 text-sm text-gray-900 font-mono">{value !== null ? String(value) : 'No detectado'}</dd>
                  </div>
                ))}
              </dl>
            </div>
          )}

          {/* Logs de procesamiento */}
          {document.logs && document.logs.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Log de procesamiento</h2>
              <div className="space-y-2">
                {document.logs.map((log, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded border-l-4 border-indigo-500">
                    <p className="text-sm font-medium text-gray-900">{log.tipo}</p>
                    <p className="text-sm text-gray-600 mt-1">{log.mensaje}</p>
                    <p className="text-xs text-gray-400 mt-1">{new Date(log.creado_en).toLocaleString()}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Acciones</h3>
            <div className="space-y-2">
              <button
                onClick={downloadDocument}
                className="w-full px-4 py-2 text-left bg-green-50 text-green-700 rounded hover:bg-green-100 transition"
              >
                📥 Descargar original
              </button>
              <Link
                to={`/chat?repo=${document.repositorio_id}`}
                className="block px-4 py-2 text-left bg-indigo-50 text-indigo-700 rounded hover:bg-indigo-100 transition"
              >
                💬 Preguntar sobre este documento
              </Link>
              {document.estado === 'error' && (
                <button className="w-full px-4 py-2 text-left bg-orange-50 text-orange-700 rounded hover:bg-orange-100 transition">
                  🔄 Reprocesar
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DocumentDetail;