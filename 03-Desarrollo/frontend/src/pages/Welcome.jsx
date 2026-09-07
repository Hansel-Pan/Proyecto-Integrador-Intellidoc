import { Link } from 'react-router-dom';

function Welcome() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-4xl font-bold text-gray-900">IntelliDoc</h1>
        <p className="mt-2 text-center text-lg text-gray-600">
          Sistema Inteligente de Gestión y Análisis Documental
        </p>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="space-y-6">
            <div className="text-center">
              <div className="mx-auto h-16 w-16 bg-indigo-100 rounded-full flex items-center justify-center">
                <svg className="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 className="mt-4 text-2xl font-bold text-gray-900">Bienvenido a IntelliDoc</h2>
              <p className="mt-2 text-gray-600">
                Sube documentos (PDF, DOCX, TXT), procésalos con IA, búscalos por contenido
                y haz preguntas en lenguaje natural con respuestas basadas en tus documentos.
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Funcionalidades principales</h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Gestión de repositorios y documentos
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Extracción automática de texto
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Clasificación, resumen y extracción de campos con IA
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Búsqueda por palabra clave y semántica (RAG)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Chat con citación de fuentes
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></span>
                  Dashboard con indicadores
                </li>
              </ul>
            </div>

            {/* Botones de acción */}
            <div className="space-y-4 pt-4 border-t border-gray-200">
              <Link
                to="/login"
                className="block w-full py-3 px-4 bg-indigo-600 text-white text-center font-medium rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Iniciar sesión
              </Link>
              <Link
                to="/register"
                className="block w-full py-3 px-4 border border-indigo-600 text-indigo-600 text-center font-medium rounded-lg hover:bg-indigo-50 transition-colors"
              >
                Crear cuenta gratis
              </Link>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-500">
                Proyecto Integrador — Desarrollo de Aplicaciones Empresariales (VI semestre)
              </p>
              <p className="text-sm text-gray-500 mt-1">
                UTS — Docente: Wilson Castaño Galviz
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Welcome