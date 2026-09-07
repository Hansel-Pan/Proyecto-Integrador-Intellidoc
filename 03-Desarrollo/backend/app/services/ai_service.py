import json
import logging
from typing import Dict, Any, List, Optional
import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIServiceError(RuntimeError):
    """Raised when the configured LLM cannot process a request."""

CATEGORIAS = ["Contrato", "Factura", "Informe", "Otro"]

PROMPT_CLASIFICACION = """
Clasifica el siguiente documento en UNA de estas categorías: {categorias}

Documento:
{texto}

Responde SOLO con el nombre de la categoría (ej: Contrato, Factura, Informe, Otro).
"""

PROMPT_RESUMEN = """
Genera un resumen conciso (máximo 3 párrafos) del siguiente documento.
Enfócate en la información clave: propósito, partes involucradas, fechas importantes, montos, conclusiones.

Documento:
{texto}

Resumen:
"""

PROMPT_EXTRACCION_CAMPOS = """
Extrae los campos clave estructurados del siguiente documento según su tipo.
El documento parece ser de tipo: {tipo_documento}

Devuelve SOLO un JSON válido con los campos extraídos. Si un campo no se encuentra, usa null.

Para FACTURA: {{"numero_factura": "", "fecha": "", "proveedor": "", "cliente": "", "total": "", "impuestos": "", "moneda": ""}}
Para CONTRATO: {{"numero_contrato": "", "fecha_inicio": "", "fecha_fin": "", "partes": [], "objeto": "", "valor": "", "moneda": ""}}
Para INFORME: {{"titulo": "", "autor": "", "fecha": "", "tema": "", "conclusiones_principales": [], "recomendaciones": []}}
Para OTRO: {{"campos_detectados": {{}}}}

Documento:
{texto}

JSON:
"""

PROMPT_RAG = """
Eres un asistente que responde preguntas basándote ÚNICAMENTE en los documentos proporcionados.
Si la información no está en los documentos, responde: "No encontré información suficiente en los documentos para responder a esta pregunta."

NO inventes información. Cita siempre la fuente indicando el nombre del documento.

Pregunta: {pregunta}

Documentos de referencia:
{contexto}

Respuesta:
"""


class AIService:
    def __init__(self):
        self.model = None
        self._initialize()

    def _initialize(self):
        if settings.LLM_API_KEY:
            try:
                genai.configure(api_key=settings.LLM_API_KEY)
                self.model = genai.GenerativeModel(settings.LLM_MODEL)
                logger.info(f"AIService inicializado con modelo: {settings.LLM_MODEL}")
            except Exception as e:
                logger.error(f"Error inicializando Gemini: {e}")
                self.model = None
        else:
            logger.warning("LLM_API_KEY no configurada. AIService no funcional.")

    def _call_llm(self, prompt: str) -> str:
        if not self.model:
            raise AIServiceError("Gemini no está configurado. Revisa LLM_API_KEY en el archivo .env.")
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            raise AIServiceError("Gemini devolvió una respuesta vacía.")
        except Exception as e:
            logger.error(f"Error llamando a Gemini: {e}")
            error_text = str(e)
            if "SERVICE_DISABLED" in error_text or "does not have permission" in error_text:
                raise AIServiceError(
                    "Gemini no está habilitado para el proyecto de la API key. "
                    "Activa generativelanguage.googleapis.com en Google Cloud y configura una clave nueva."
                ) from e
            if "401" in error_text or "API key" in error_text:
                raise AIServiceError(
                    "La API key de Gemini es inválida o no tiene permisos para usar el modelo configurado."
                ) from e
            if "429" in error_text or "quota" in error_text.lower():
                raise AIServiceError(
                    "Se agotó la cuota de Gemini. Espera unos minutos o usa un proyecto con cuota disponible."
                ) from e
            raise AIServiceError(f"Gemini no pudo procesar la solicitud: {error_text}") from e

    def clasificar(self, texto: str) -> str:
        """Clasificar documento en una de las categorías predefinidas."""
        if not self.model:
            return "Otro"
        try:
            prompt = PROMPT_CLASIFICACION.format(
                categorias=", ".join(CATEGORIAS),
                texto=texto[:8000]
            )
            resultado = self._call_llm(prompt)
            for cat in CATEGORIAS:
                if cat.lower() in resultado.lower():
                    return cat
            return "Otro"
        except AIServiceError:
            raise
        except Exception as e:
            logger.error(f"Error clasificando: {e}")
            return "Otro"

    def resumir(self, texto: str) -> str:
        """Generar resumen del documento."""
        if not self.model:
            return "Resumen no disponible (IA no configurada)"
        try:
            prompt = PROMPT_RESUMEN.format(texto=texto[:12000])
            return self._call_llm(prompt)
        except AIServiceError:
            raise
        except Exception as e:
            logger.error(f"Error resumiendo: {e}")
            return "Error generando resumen"

    def extraer_campos(self, texto: str, categoria: str) -> Dict[str, Any]:
        """Extraer campos clave según el tipo de documento."""
        if not self.model:
            return {"error": "IA no configurada"}
        try:
            prompt = PROMPT_EXTRACCION_CAMPOS.format(
                tipo_documento=categoria,
                texto=texto[:12000]
            )
            respuesta = self._call_llm(prompt)
            
            try:
                start = respuesta.find("{")
                end = respuesta.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = respuesta[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.warning(f"No se pudo parsear JSON de extracción: {e}")
            
            return {"error": "No se pudo extraer campos estructurados", "raw": respuesta}
        except AIServiceError:
            raise
        except Exception as e:
            logger.error(f"Error extrayendo campos: {e}")
            return {"error": str(e)}

    def responder_pregunta(self, pregunta: str, fragmentos: List[Dict[str, Any]]) -> str:
        """Responder pregunta usando RAG con los fragmentos recuperados."""
        if not self.model:
            return "Error: IA no configurada - verifica LLM_API_KEY"
        
        if not fragmentos:
            return "No encontré información suficiente en los documentos para responder a esta pregunta."
        
        try:
            contexto_parts = []
            for i, frag in enumerate(fragmentos):
                doc_name = frag.get("nombre_archivo", f"Documento {frag.get('documento_id', 'desconocido')}")
                texto = frag.get("texto", "")[:1500]
                contexto_parts.append(f"[Fuente {i+1}: {doc_name}]\n{texto}")
            
            contexto = "\n\n---\n\n".join(contexto_parts)
            prompt = PROMPT_RAG.format(pregunta=pregunta, contexto=contexto)
            return self._call_llm(prompt)
        except AIServiceError:
            raise
        except Exception as e:
            logger.error(f"Error en RAG: {e}")
            return f"Error procesando pregunta: {str(e)}"