from enum import Enum

# Limites Operacionais (Thresholds) - Definidos como constantes para fácil calibração
LIMIT_EGT_MAX = 950.0        # Celsius
LIMIT_EGT_CRITICAL = 960.0   # Celsius
LIMIT_VIB_NORMAL = 1.5       # Units (mils)
LIMIT_VIB_MAX = 2.0          # Units
LIMIT_OIL_MIN = 40.0         # PSI
LIMIT_CYCLES_LIFE = 20000    # Flight Cycles

# Enum para status de manutenção, garantindo consistência nos retornos
class MaintenanceStatus(str, Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING (MONITOR)"
    PREVENTIVE = "PREVENTIVE MAINT"
    CRITICAL = "CRITICAL (AOG)"
    SENSOR_FAULT = "SENSOR FAULT (INVALID DATA)"
    DATA_ERROR = "ERRO DE DADOS"
    SYSTEM_ERROR = "ERRO DE SISTEMA"
