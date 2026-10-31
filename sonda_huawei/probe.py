"""
Core probe engine for Huawei VRP devices.
"""

import re
import sys
import time
from typing import Any, Dict, List, Optional

try:
    from netmiko import ConnectHandler
except ImportError:
    ConnectHandler = None


def parse_ping_output(output: str, source_ip: str, target: str) -> Dict[str, Any]:
    """Parse raw Huawei VRP ping output to extract loss percentage and RTT statistics."""
    # Regex para extrair estatísticas de perda de pacote:
    # Exemplo VRP: "0.00% packet loss" ou "20% packet loss" ou "100.00% packet loss"
    loss_match = re.search(r"(\d+(?:\.\d+)?)%\s+packet\s+loss", output, re.IGNORECASE)
    packet_loss = float(loss_match.group(1)) if loss_match else None

    # Regex para extrair RTT: min/avg/max = 12/15/22 ms (suporta inteiros e decimais)
    rtt_match = re.search(
        r"min/avg/max\s*=\s*(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)",
        output,
        re.IGNORECASE,
    )
    if rtt_match:
        rtt_min = float(rtt_match.group(1))
        rtt_avg = float(rtt_match.group(2))
        rtt_max = float(rtt_match.group(3))
    else:
        # Fallback para outro formato VRP: "10/12/15 ms"
        rtt_match_alt = re.search(
            r"(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)\s*ms",
            output,
            re.IGNORECASE,
        )
        if rtt_match_alt:
            rtt_min = float(rtt_match_alt.group(1))
            rtt_avg = float(rtt_match_alt.group(2))
            rtt_max = float(rtt_match_alt.group(3))
        else:
            rtt_min = rtt_avg = rtt_max = None

    return {
        "source_ip": source_ip,
        "target": target,
        "packet_loss_pct": packet_loss,
        "rtt_min_ms": rtt_min,
        "rtt_avg_ms": rtt_avg,
        "rtt_max_ms": rtt_max,
        "raw_output": output,
    }


class HuaweiProbe:
    """Classe controladora para execução de testes de latência em roteadores Huawei VRP."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 30,
    ):
        self.device_params = {
            "device_type": "huawei",
            "host": host,
            "username": username,
            "password": password,
            "port": port,
            "timeout": timeout,
            "global_delay_factor": 1.5,
        }

    def ping_from_source(
        self,
        connection: Any,
        target: str,
        source_ip: str,
        count: int = 5,
        packet_size: int = 64,
    ) -> Dict[str, Any]:
        """
        Executa comando de ping originando a partir de um IP de origem específico no Huawei VRP:
        ping -a <source_ip> -c <count> -s <packet_size> <target>
        """
        cmd = f"ping -a {source_ip} -c {count} -s {packet_size} {target}"
        output = connection.send_command(cmd)
        return parse_ping_output(output, source_ip=source_ip, target=target)

    def run_multi_source_test(
        self,
        target: str,
        source_ips: List[str],
        count: int = 5,
        packet_size: int = 64,
    ) -> List[Dict[str, Any]]:
        """Executa a sequência de testes para todos os IPs de origem (máx. 5)."""
        if ConnectHandler is None:
            raise RuntimeError(
                "A biblioteca 'netmiko' é necessária para conexões SSH. Instale com: pip install netmiko"
            )

        if len(source_ips) > 5:
            print("Aviso: Limitando a lista aos primeiros 5 IPs de origem.", file=sys.stderr)
            source_ips = source_ips[:5]

        results = []
        print(f"[*] Conectando ao roteador Huawei ({self.device_params['host']})...")
        with ConnectHandler(**self.device_params) as conn:
            conn.enable()
            for idx, src in enumerate(source_ips, 1):
                print(f"  [{idx}/{len(source_ips)}] Disparando teste originado de: {src} -> {target}...")
                res = self.ping_from_source(conn, target, src, count=count, packet_size=packet_size)
                results.append(res)
                time.sleep(1)

        return results

