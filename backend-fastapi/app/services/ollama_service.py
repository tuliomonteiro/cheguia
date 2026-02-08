import ollama
from typing import Dict, List, Any
from app.core.config import settings

class OllamaService:
    """Service for interacting with Ollama local LLM"""
    
    def __init__(self):
        # Ollama client handling
        # standard client relies on OLLAMA_HOST env var by default
        self.host = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        try:
             self.client = ollama.Client(host=self.host)
        except Exception:
             print(f"Warning: Could not connect to Ollama at {self.host}")
             self.client = None

        self.system_prompt = self._get_paraguay_system_prompt()
    
    def _get_paraguay_system_prompt(self) -> str:
        """Get the system prompt for Paraguay assistant"""
        return """Eres un asistente especializado en ayudar a brasileños que quieren establecerse en Paraguay. 
Tu conocimiento incluye:
- Trámites de inmigración y residencia
- Documentos necesarios para vivir en Paraguay
- Información sobre SET (impuestos), ANDE (luz), bancos
- Procesos para obtener RUC, abrir cuentas bancarias
- Información sobre ciudades como Ciudad del Este, Asunción

Responde siempre en español paraguayo, pero si el usuario pregunta en portugués, puedes responder en portugués también.
Sé preciso, útil y amigable. Si no sabes algo específico, admítelo y sugiere dónde pueden encontrar más información.
Mantén las respuestas concisas pero completas."""

    async def chat(self, user_message: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send a chat message to Ollama and get response
        """
        if not self.client:
             return {
                'message': "Error: Servicio de IA no disponible.",
                'error': "Client not initialized"
            }

        try:
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if chat_history:
                for msg in chat_history[-10:]:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": user_message})
            
            # Call Ollama (sync for now, as the library is sync)
            # In a real high-perf scenario, we might want to run this in a threadpool
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                }
            )
            
            ai_response = response['message']['content']
            
            return {
                'message': ai_response,
                'sources': [],
                'model_used': self.model,
            }
            
        except Exception as e:
            return {
                'message': f"Lo siento, hubo un error procesando tu consulta: {str(e)}",
                'error': str(e)
            }
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        if not self.client:
            return []
        try:
            models_response = self.client.list()
            # The structure of response might vary by version, adapting to object access
            return [model['name'] for model in models_response.get('models', [])]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def is_model_available(self) -> bool:
        """Check if the configured model is available"""
        if not self.client:
            return False
        try:
            # Simple health check essentially
            self.client.list()
            return True
        except Exception:
            return False

ollama_service = OllamaService()
