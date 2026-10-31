"""
CLI interface for sonda-huawei.
"""

import argparse
import json
import sys
from typing import List, Optional

from sonda_huawei import __version__
from sonda_huawei.probe import HuaweiProbe

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def format_table(results: List[dict]) -> str:
    """Format probe results as a human-readable table."""
    table_data = []
    for r in results:
        loss = f"{r['packet_loss_pct']}%" if r.get("packet_loss_pct") is not None else "N/A"
        avg = f"{r['rtt_avg_ms']} ms" if r.get("rtt_avg_ms") is not None else "N/A"
        min_max = (
            f"{r['rtt_min_ms']} / {r['rtt_max_ms']} ms"
            if r.get("rtt_min_ms") is not None
            else "N/A"
        )
        table_data.append([r["source_ip"], r["target"], loss, avg, min_max])

    headers = ["IP Origem", "IP Destino", "Perda (%)", "RTT Médio", "RTT Mín / Máx"]
    if tabulate is not None:
        return tabulate(table_data, headers=headers, tablefmt="fancy_grid")

    lines = ["\t".join(headers)]
    for row in table_data:
        lines.append("\t".join(row))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="sonda-huawei",
        description="Sonda Huawei - Testes de Latência Multi-Origem em Bordas Multihoming",
    )
    parser.add_argument(
        "--version", "-V", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--host", required=True, help="IP ou hostname do roteador Huawei")
    parser.add_argument("--username", "-u", required=True, help="Usuário de acesso SSH")
    parser.add_argument("--password", "-p", required=True, help="Senha de acesso SSH")
    parser.add_argument("--port", type=int, default=22, help="Porta SSH (padrão: 22)")
    parser.add_argument("--target", "-t", required=True, help="IP de destino do teste de latência")
    parser.add_argument(
        "--sources",
        "-s",
        nargs="+",
        required=True,
        help="Lista de até 5 IPs de origem (ex: -s 200.1.1.1 200.2.2.2 200.3.3.3)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=5,
        help="Quantidade de pacotes ICMP (padrão: 5)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=64,
        help="Tamanho do pacote em bytes (padrão: 64)",
    )
    parser.add_argument("--timeout", type=int, default=30, help="Timeout de conexão SSH em segundos (padrão: 30)")
    parser.add_argument("--json", action="store_true", help="Exibir saída no formato JSON")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    probe = HuaweiProbe(
        host=args.host,
        username=args.username,
        password=args.password,
        port=args.port,
        timeout=args.timeout,
    )
    try:
        results = probe.run_multi_source_test(
            target=args.target,
            source_ips=args.sources,
            count=args.count,
            packet_size=args.size,
        )
    except Exception as e:
        print(f"[ERRO] Falha na execução da sonda: {e}", file=sys.stderr)
        return 1

    if args.json:
        clean_results = [{k: v for k, v in r.items() if k != "raw_output"} for r in results]
        print(json.dumps(clean_results, indent=2))
    else:
        print("\n" + format_table(results))

    return 0


if __name__ == "__main__":
    sys.exit(main())
