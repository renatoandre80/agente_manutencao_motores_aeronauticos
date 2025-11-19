from pydantic import BaseModel, Field

class EngineTelemetry(BaseModel):
    """Modelo de dados com validação física de limites (Physics-Informed)."""
    egt: float = Field(..., ge=-50, le=2000, description="EGT em Celsius. Faixa física válida: -50 a 2000.")
    vibration: float = Field(..., ge=0, le=10, description="Vibração N1. Faixa física válida: 0 a 10.")
    oil_pressure: float = Field(..., ge=0, le=200, description="Pressão de óleo em PSI. Faixa física válida: 0 a 200.")
    cycles: int = Field(..., ge=0, description="Ciclos acumulados não podem ser negativos.")
