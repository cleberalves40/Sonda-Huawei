#!/usr/bin/env python3
"""
Compatibilidade retroativa para execução direta: python3 sonda_huawei.py
"""

import sys
from sonda_huawei.cli import main

if __name__ == "__main__":
    sys.exit(main())
