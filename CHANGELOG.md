# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

O formato segue as diretrizes do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [0.1.0] - 2026-10-31

### Adicionado
- Estruturação do projeto como pacote Python oficial (`PEP 621`) via `pyproject.toml`.
- Ponto de entrada CLI executável: `sonda-huawei`.
- Módulo `sonda_huawei` contendo `HuaweiProbe` e rotinas de parsing de ICMP para VRPv5/VRPv8.
- Opção `--version` / `-V` exibindo a versão corrente.
- Opção `--json` para exportação limpa de resultados para automações/dashboards.
- Suporte a fallback de formatação quando `tabulate` não estiver instalado.
- Suite de testes unitários em `tests/test_probe.py` cobrindo cenários de parsing e argumentos CLI.
- Pipeline de integração contínua (CI) em `.github/workflows/test.yml` cobrindo Python 3.8 a 3.12.
- Estrutura oficial do **FreeBSD Port** em `freebsd/` (`Makefile`, `distinfo`, `pkg-descr`).
- Fórmula para **Homebrew Tap** em `Formula/sonda-huawei.rb` no repositório `cleberalves40/homebrew-tap`.
- Documentação atualizada de instalação para Homebrew, FreeBSD Ports e Python venv no `README.md`.
