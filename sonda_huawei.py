#!/usr/bin/env python3
"""
Sonda de Testes de Latência para Dispositivos Huawei (VRP).
Origina testes de ping/latência a partir de até 5 IPs de origem diferentes em bordas Multihoming.
"""

import argparse
import json
import re
import sys
import time
from typing import Dict, List, Optional

try:
    from netmiko import ConnectHandler
    from tabulate import tabulate
except ImportError:
    pass


class HuaweiProbe:
    """Classe controladora para execução de testes de latência em roteadores Huawei VRP."""

    def __init__(self, host: str, username: str, password: str, port: int = 22, timeout: int = 30):
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
        connection,
        target: str,
        source_ip: str,
        count: int = 5,
        packet_size: int = 64
    ) -> Dict[str, Optional[float]]:
        """
        Executa comando de ping originando a partir de um IP de origem específico no Huawei VRP:
        ping -a <source_ip> -c <count> -s <packet_size> <target>
        """
        cmd = f"ping -a {source_ip} -c {count} -s {packet_size} {target}"
        output = connection.send_command(cmd)

        # Regex para extrair estatísticas de perda de pacote
        # Exemplo VRP: "0.00% packet loss" ou "20.00% packet loss"
        loss_match = re.search(r"(\d+(\.\d+)?)%\s+packet\s+loss", output, re.IGNORECASE)
        packet_loss = float(loss_match.group(1)) if loss_match else None

        # Regex para extrair RTT: min/avg/max = 12/15/22 ms
        rtt_match = re.search(r"min/avg/max\s*=\s*(\d+(\.\d+)?)/(\d+(\.\d+)?)/(\d+(\.\d+)?)", output, re.IGNORECASE)
        if rtt_match:
            rtt_min = float(rtt_match.group(1))
            rtt_avg = float(rtt_match.group(3))
            rtt_max = float(rtt_match.group(5))
        else:
            # Fallback para outro formato VRP: "round-trip min/avg/max = 10/12/15 ms"
            rtt_match_alt = re.search(r"(\d+)/(\d+)/(\d+)\s*ms", output)
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
            "raw_output": output
        }

    def run_multi_source_test(
        self,
        target: str,
        source_ips: List[str],
        count: int = 5,
        packet_size: int = 64
    ) -> List[Dict]:
        """Executa a sequência de testes para todos os IPs de origem (máx. 5)."""
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


def main():
    parser = argparse.ArgumentParser(
        description="Sonda Huawei - Testes de Latência Multi-Origem em Bordas Multihoming"
    )
    parser.add_argument("--host", required=True, help="IP ou hostname do roteador Huawei")
    parser.add_argument("--username", "-u", required=True, help="Usuário de acesso SSH")
    parser.add_argument("--password", "-p", required=True, help="Senha de acesso SSH")
    parser.add_argument("--target", "-t", required=True, help="IP de destino do teste de latência")
    parser.add_argument(
        "--sources", "-s", nargs="+", required=True,
        help="Lista de até 5 IPs de origem (ex: -s 200.1.1.1 200.2.2.2 200.3.3.3)"
    )
    parser.add_argument("--count", "-c", type=int, default=5, help="Quantidade de pacotes ICMP (padrão: 5)")
    parser.add_argument("--size", type=int, default=64, help="Tamanho do pacote em bytes (padrão: 64)")
    parser.add_argument("--json", action="store_true", help="Exibir saída no formato JSON")

    args = parser.parse_args()

    # Checar dependências
    if "ConnectHandler" not in globals():
        print("Erro: A biblioteca 'netmiko' é necessária. Instale com: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    probe = HuaweiProbe(host=args.host, username=args.username, password=args.password)
    try:
        results = probe.run_multi_source_test(
            target=args.target,
            source_ips=args.sources,
            count=args.count,
            packet_size=args.size
        )
    except Exception as e:
        print(f"[ERRO] Falha na execução da sonda: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # Remover raw_output para JSON limpo
        clean_results = [{k: v for k, v in r.items() if k != "raw_output"} for r in results]
        print(json.dumps(clean_results, indent=2))
    else:
        table_data = []
        for r in results:
            loss = f"{r['packet_loss_pct']}%" if r['packet_loss_pct'] is not None else "N/A"
            avg = f"{r['rtt_avg_ms']} ms" if r['rtt_avg_ms'] is not None else "N/A"
            min_max = f"{r['rtt_min_ms']} / {r['rtt_max_ms']} ms" if r['rtt_min_ms'] is not None else "N/A"
            table_data.append([r["source_ip"], r["target"], loss, avg, min_max])

        headers = ["IP Origem", "IP Destino", "Perda (%)", "RTT Médio", "RTT Mín / Máx"]
        if "tabulate" in globals():
            print("\n" + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("\n" + "\t".join(headers))
            for row in table_data:
                print("\t".join(row))


if __name__ == "__main__":
    main()
