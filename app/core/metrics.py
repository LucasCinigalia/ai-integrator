"""Sistema de métricas básico para monitoramento."""

import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List


class Metrics:
    """
    Coleta métricas básicas da aplicação.

    Rastreia chamadas de API, erros e latências.
    """

    def __init__(self) -> None:
        """Inicializa o sistema de métricas."""
        self.api_calls: Dict[str, int] = defaultdict(int)
        self.api_errors: Dict[str, int] = defaultdict(int)
        self.api_latencies: List[float] = []
        self.start_time = datetime.now()

    def record_call(self, endpoint: str, duration_ms: float, success: bool) -> None:
        """
        Registra uma chamada de API.

        Args:
            endpoint: Endpoint chamado
            duration_ms: Duração da chamada em milissegundos
            success: Se a chamada foi bem-sucedida
        """
        self.api_calls[endpoint] += 1
        if not success:
            self.api_errors[endpoint] += 1
        self.api_latencies.append(duration_ms)

    def get_stats(self) -> Dict:
        """
        Retorna estatísticas agregadas.

        Returns:
            Dict: Estatísticas de métricas
        """
        total_calls = sum(self.api_calls.values())
        total_errors = sum(self.api_errors.values())
        avg_latency = sum(self.api_latencies) / len(self.api_latencies) if self.api_latencies else 0
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "uptime_seconds": uptime,
            "total_calls": total_calls,
            "total_errors": total_errors,
            "error_rate": total_errors / total_calls if total_calls > 0 else 0,
            "avg_latency_ms": round(avg_latency, 2),
            "calls_by_endpoint": dict(self.api_calls),
            "errors_by_endpoint": dict(self.api_errors),
        }

    def reset(self) -> None:
        """Reseta todas as métricas."""
        self.api_calls.clear()
        self.api_errors.clear()
        self.api_latencies.clear()
        self.start_time = datetime.now()


metrics = Metrics()
