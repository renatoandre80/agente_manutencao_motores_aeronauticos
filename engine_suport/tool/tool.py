import logging
from typing import Dict, Any
from pydantic import ValidationError

from ..schema.schemas import EngineTelemetry
from .constants import (
    MaintenanceStatus,
    LIMIT_EGT_MAX,
    LIMIT_EGT_CRITICAL,
    LIMIT_VIB_MAX,
    LIMIT_CYCLES_LIFE,
    LIMIT_OIL_MIN,
)

def analyze_engine_health(egt: float, vibration: float, oil_pressure: float, cycles: int) -> Dict[str, Any]:
    """
    Analisa a telemetria do motor seguindo protocolos de manutenção.
    Realiza validação de sanidade dos sensores antes do diagnóstico.

    Args:
        egt (float): Temperatura de Exaustão de Gás (EGT) em Celsius.
        vibration (float): Vibração do eixo N1 (mils).
        oil_pressure (float): Pressão do óleo (PSI).
        cycles (int): Ciclos totais acumulados.

    Returns:
        dict: Diagnóstico estruturado contendo status, ATA Chapter e ação recomendada.
    """
    try:
        # 1. Validação de Entrada (Engenharia de Software)
        telemetry = EngineTelemetry(
            egt=egt, vibration=vibration, oil_pressure=oil_pressure, cycles=cycles
        )
        logging.info(f"Análise solicitada: {telemetry.model_dump()}")

        # 2. Lógica de Diagnóstico Hierárquica
        if telemetry.vibration > LIMIT_VIB_MAX or \
           (telemetry.vibration > 1.6 and telemetry.egt > LIMIT_EGT_CRITICAL):
            return {
                "status": MaintenanceStatus.CRITICAL,
                "action": "INTERDIÇÃO DE VOO (AOG). Boroscopia mandatória e possível troca.",
                "reason": f"Assinatura de falha mecânica severa. Vibração {telemetry.vibration} / EGT {telemetry.egt}",
                "ata_chapter": "72-00-00",
                "confidence": "Alta"
            }

        if telemetry.cycles > LIMIT_CYCLES_LIFE:
            return {
                "status": MaintenanceStatus.PREVENTIVE,
                "action": "Planejar remoção do motor para Overhaul.",
                "reason": f"Limite de Hard Time excedido ({telemetry.cycles} ciclos).",
                "ata_chapter": "05-10-00",
                "confidence": "Absoluta"
            }

        warnings = []
        ata_chapter = "72-00-00" # Default ATA
        if telemetry.oil_pressure < LIMIT_OIL_MIN:
            warnings.append(f"Pressão de óleo baixa ({telemetry.oil_pressure} PSI).")
            ata_chapter = "79-00-00" # Oil System

        if LIMIT_EGT_MAX < telemetry.egt <= LIMIT_EGT_CRITICAL:
            warnings.append(f"EGT acima do nominal ({telemetry.egt} C). Trend Monitoring sugerido.")

        if warnings:
            return {
                "status": MaintenanceStatus.WARNING,
                "action": "Realizar testes de solo e verificar filtros.",
                "reason": "; ".join(warnings),
                "ata_chapter": ata_chapter,
                "confidence": "Média"
            }

        logging.info("Diagnóstico: Motor Operacional.")
        return {
            "status": MaintenanceStatus.NORMAL,
            "action": "Liberado para serviço.",
            "details": "Parâmetros nominais.",
            "confidence": "Alta"
        }

    except ValidationError as e:
        logging.error(f"Erro de validação de dados: {e}")
        return {
            "status": MaintenanceStatus.DATA_ERROR,
            "action": "Verificar entrada de dados.",
            "details": str(e)
        }
    except Exception as e:
        logging.error(f"Erro inesperado na ferramenta: {e}", exc_info=True)
        return {
            "status": MaintenanceStatus.SYSTEM_ERROR,
            "action": "Contatar suporte de TI.",
            "details": "Falha interna na ferramenta de análise."
        }
