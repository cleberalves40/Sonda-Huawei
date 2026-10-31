"""
Sonda Huawei - Latency and packet loss probe for Huawei VRP edge devices.
"""

__version__ = "0.1.0"

from sonda_huawei.probe import HuaweiProbe, parse_ping_output

__all__ = ["__version__", "HuaweiProbe", "parse_ping_output"]

