# Huawei Latency Probe (VRP)

[Português](README.md) | **English**

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Huawei%20VRP-red.svg)](https://e.huawei.com/)
[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.1.1-green.svg)](https://github.com/cleberalves40/Sonda-Huawei/releases)

A latency and packet-loss testing tool for **Huawei** edge devices (VRPv5 / VRPv8, NE40E, NetEngine, CloudEngine, and AR routers). It can originate tests from **up to five different IP addresses**.

Especially useful in **BGP multihoming edge** environments to compare the quality and latency of different IP transits, IXPs, and carriers in real time.

## Multihoming edge scenario

```text
               +---------------+
               |  Edge Router  |
               |  Huawei VRP   |
               +-------+-------+
                       |
       +---------------+---------------+
       | (Source IP 1) | (Source IP 2) | (Source IP 3)
       v               v               v
 +-----------+   +-----------+   +-----------+
 | Carrier   |   | Carrier   |   | IXP       |
 | Alpha     |   | Beta      |   | Brazil    |
 +-----+-----+   +-----+-----+   +-----+-----+
       +---------------+---------------+
                       v
                 [ Target / CDN ]
```

By setting the source IP for each test (`ping -a <source_ip>`), the router sends outbound traffic according to the policy or routing table associated with each address block, helping identify variation or degradation on each path.

## Installation

### Option A: macOS / Linux with Homebrew

```sh
brew install cleberalves40/tap/sonda-huawei
```

### Option B: FreeBSD (Ports)

```sh
cd /usr/ports/net-mgmt/sonda-huawei   # or use this repository's freebsd/ directory
make install clean
```

### Option C: Python virtual environment / pip

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install .
```

## Run from the CLI (`sonda-huawei`)

After installing the package, invoke the command-line utility directly. Supply credentials securely for your environment; avoid placing real passwords in shell history or shared scripts.

```sh
sonda-huawei \
  --host 192.168.1.1 \
  --username admin \
  --password '<router-password>' \
  --port 22 \
  --target 8.8.8.8 \
  --sources 200.1.1.1 200.2.2.2 200.3.3.3 \
  --count 5
```

> **Tip:** Set the SSH TCP port with `-P` or `--port` (default: `22`). This is useful when the router uses an alternate management port, for example `-P 2222`.

> **Compatibility:** You can also run the package as a module (`python3 -m sonda_huawei`) or use the compatibility script (`python3 sonda_huawei.py`).

### Main CLI parameters

| Parameter | Alias | Required | Default | Description |
|:---|:---:|:---:|:---:|:---|
| `--host` | | Yes | - | Huawei router IP address or hostname |
| `--username` | `-u` | Yes | - | SSH username |
| `--password` | `-p` | Yes | - | SSH password |
| `--port` | `-P` | No | `22` | SSH TCP port (for example, `-P 2222`) |
| `--target` | `-t` | Yes | - | Destination IP address for ICMP tests |
| `--sources` | `-s` | Yes | - | Up to five source IP addresses configured on the router |
| `--count` | `-c` | No | `5` | ICMP packets per test |
| `--size` | | No | `64` | Packet size in bytes |
| `--timeout` | | No | `30` | SSH connection timeout in seconds |
| `--json` | | No | - | Export results as JSON |
| `--version` | `-V` | No | - | Show the installed version |

### Example formatted output

```text
+---------------+--------------+-------------+-------------+---------------+
| Source IP     | Target IP    | Loss (%)    | Avg RTT     | Min / Max RTT |
+===============+==============+=============+=============+===============+
| 200.1.1.1     | 8.8.8.8      | 0.0%        | 12.4 ms     | 11.2 / 14.1 ms|
| 200.2.2.2     | 8.8.8.8      | 0.0%        | 18.2 ms     | 17.5 / 21.0 ms|
| 200.3.3.3     | 8.8.8.8      | 20.0%       | 35.1 ms     | 31.0 / 42.0 ms|
+---------------+--------------+-------------+-------------+---------------+
```

For integration with scripts or dashboards, pass the `--json` flag:

```sh
sonda-huawei --host 192.168.1.1 -u admin -p '<router-password>' --target 8.8.8.8 --sources 200.1.1.1 200.2.2.2 --json
```

## Continuous monitoring with NQA

To let the router perform continuous tests without an external script running periodically, use the NQA configuration template at [`huawei_nqa_template.cfg`](huawei_nqa_template.cfg).

## License

Distributed under the [BSD 2-Clause](LICENSE) license.
