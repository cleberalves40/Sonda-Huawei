# Sonda de Latência Huawei (VRP)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Huawei%20VRP-red.svg)](https://e.huawei.com/)
[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.1.0-green.svg)](https://github.com/cleberalves40/Sonda-Huawei/releases)

Sonda de testes de latência e perda de pacotes para dispositivos de borda **Huawei** (VRPv5 / VRPv8, NE40E, NetEngine, CloudEngine, AR routers), permitindo originar testes a partir de **até 5 endereços IP diferentes**.

Especialmente útil em cenários de **Borda Multihoming (BGP)** para comparar em tempo real a qualidade e a latência de trânsitos IP, PTT / IX e operadoras distintas.

---

## 🌐 Cenário de Uso (Multihoming Edge)

```text
               ┌───────────────┐
               │ Roteador Borda│
               │  Huawei VRP   │
               └───────┬───────┘
                       │
       ┌───────────────┼───────────────┐
       │ (IP Origem 1) │ (IP Origem 2) │ (IP Origem 3)
       ▼               ▼               ▼
 ┌───────────┐   ┌───────────┐   ┌───────────┐
 │ Operadora │   │ Operadora │   │  IX / PTT │
 │  Alpha    │   │   Beta    │   │   Brasil  │
 └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
       └───────────────┼───────────────┘
                       ▼
                 [ Alvo / CDN ]
```

Ao forçar o IP de origem em cada teste (`ping -a <source_ip>`), o roteador comuta o tráfego de saída pela política ou tabela correspondente a cada bloco, permitindo identificar com precisão oscilações ou degradação em cada caminho.

---

## 🛠️ Instalação

### Opção A: macOS / Linux via Homebrew

```bash
brew install cleberalves40/tap/sonda-huawei
```

### Opção B: FreeBSD (Ports)

```bash
cd /usr/ports/net-mgmt/sonda-huawei   # ou usando a pasta freebsd/ deste repositório
make install clean
```

### Opção C: Python Virtualenv / Pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## 🚀 Execução via CLI (`sonda-huawei`)

Com o pacote instalado, utilize diretamente o utilitário de linha de comando:

```bash
sonda-huawei \
  --host 192.168.1.1 \
  -u admin \
  -p MinhaSenha123 \
  --target 8.8.8.8 \
  --sources 200.1.1.1 200.2.2.2 200.3.3.3 \
  --count 5
```

> **Nota de Compatibilidade:** Você também pode executar diretamente via módulo (`python3 -m sonda_huawei`) ou pelo script de compatibilidade (`python3 sonda_huawei.py`).

### Exemplo de Saída Formatada:

```text
+---------------+--------------+-------------+-------------+---------------+
| IP Origem     | IP Destino   | Perda (%)   | RTT Médio   | RTT Mín / Máx |
+===============+==============+=============+=============+===============+
| 200.1.1.1     | 8.8.8.8      | 0.0%        | 12.4 ms     | 11.2 / 14.1 ms|
| 200.2.2.2     | 8.8.8.8      | 0.0%        | 18.2 ms     | 17.5 / 21.0 ms|
| 200.3.3.3     | 8.8.8.8      | 20.0%       | 35.1 ms     | 31.0 / 42.0 ms|
+---------------+--------------+-------------+-------------+---------------+
```

Para integrar a scripts ou dashboards, passe a flag `--json`:

```bash
sonda-huawei --host 192.168.1.1 -u admin -p MinhaSenha123 --target 8.8.8.8 --sources 200.1.1.1 200.2.2.2 --json
```

---

## ⚙️ Monitoramento Contínuo com NQA

Caso prefira deixar o próprio roteador testando continuamente sem necessidade de um script externo rodando periodicamente, utilize o modelo de configuração NQA incluído em [`huawei_nqa_template.cfg`](huawei_nqa_template.cfg).

---

## 📄 Licença

Distribuído sob a licença [BSD 2-Clause](LICENSE).
