#!/usr/bin/env python3
"""Intentional hanging fixture for eval harness timeout checks."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import time


while True:
    time.sleep(60)
