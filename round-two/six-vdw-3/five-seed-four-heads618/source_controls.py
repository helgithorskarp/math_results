#!/usr/bin/env python3
"""Damage tests for the complete four-head cover and written-premise domain."""
import argparse
import json
from pathlib import Path
import cover_check


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    result=cover_check.controls(p.parse_args().cover)
    print(json.dumps({'positive_complete_cover':result['positive_control'],
                      'damaged_source_records_rejected':result['damaged_certificates_rejected']}))
