import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { repositoriesApi, documentsApi } from '../services/api';

function RepositoryDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [repository, setRepository] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [filterEstado, setFilterEstado] = useState('');

  useEffect(() => {
    loadData();
  }, [id, filterEstado]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [repoRes, docsRes] = await Promise.all([
        repositoriesApi.get(id),
        documentsApi.list({ repositorio_id: id, estado: filterEstado || undefined }),
      ]);
      setRepository(repoRes.data);
      setDocuments(docsRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const allowedTypes = ['pdf', 'docx', 'txt'];
      const ext = file.name.split('.').pop().toLowerCase();
      if (!allowedTypes.includes(ext)) {
        setError('Tipo de archivo no permitido. Use PDF, DOCX o TXT');
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        setError('Archivo demasiado grande. Máximo 10 MB');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    
    setUploading(true);
    try {
      await documentsApi.upload(id, selectedFile);
      setShowUploadModal(false);
      setSelectedFile(null);
      loadData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al subir archivo');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId, docName) => {
    if (!window.confirm(`¿Eliminar "${docName}"?`)) return;
    
    try {
      await documentsApi.delete(docId);
      loadData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al eliminar');
    }
  };

  const downloadDocument = async (docId, docName) => {
    try {
      const response = await documentsApi.download(docId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', docName);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Error al descargar');
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

  if (!repository) {
    return <div className="text-center py-12">Repositorio no encontrado</div>;
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <Link
            to="/repositories"
            className="text-sm text-gray-500 hover:text-gray-700 mb-2 inline-block"
          >
            ← Volver a repositorios
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">{repository.nombre}</h1>
          <p className="text-sm text-gray-500">Creado: {new Date(repository.creado_en).toLocaleDateString()}</p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          Subir documento
        </button>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-500">Total documentos</p>
          <p className="text-2xl font-bold text-gray-900">{repository.total_documentos || 0}</p>
        </div>
        {Object.entries(repository.documentos_por_estado || {}).map(([estado, count]) => (
          <div key={estado} className="bg-white p-4 rounded-lg shadow">
            <p className="text-sm text-gray-500 capitalize">{estado}</p>
            <p className="text-2xl font-bold text-gray-900">{count}</p>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="mb-4 flex gap-4">
        <select
          value={filterEstado}
          onChange={(e) => setFilterEstado(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Todos los estados</option>
          <option value="pendiente">Pendiente</option>
          <option value="procesando">Procesando</option>
          <option value="procesado">Procesado</option>
          <option value="error">Error</option>
        </select>
      </div>

      {/* Documents Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {documents.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No hay documentos</h3>
            <p className="mt-1 text-sm text-gray-500">Sube tu primer documento para comenzar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Documento</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Formato</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoría</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <Link to={`/documents/${doc.id}`} className="text-indigo-600 hover:text-indigo-900 font-medium">
                        {doc.nombre_archivo}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 text-xs bg-indigo-100 text-indigo-800 rounded-full">{doc.formato.toUpperCase()}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs rounded-full ${getEstadoBadge(doc.estado)}`}>
                        {doc.estado}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {doc.categoria || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <Link to={`/documents/${doc.id}`} className="text-indigo-600 hover:text-indigo-900">Ver</Link>
                      <button
                        onClick={() => downloadDocument(doc.id, doc.nombre_archivo)}
                        className="text-green-600 hover:text-green-900"
                      >
                        Descargar
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id, doc.nombre_archivo)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={() => setShowUploadModal(false)} />
            <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Subir documento</h2>
              <form onSubmit={handleUpload}>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Archivo (PDF, DOCX, TXT - máx 10MB)</label>
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileSelect}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    required
                  />
                </div>
                <div className="flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setShowUploadModal(false)}
                    className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={uploading || !selectedFile}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {uploading ? 'Subiendo...' : 'Subir'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default RepositoryDetail;