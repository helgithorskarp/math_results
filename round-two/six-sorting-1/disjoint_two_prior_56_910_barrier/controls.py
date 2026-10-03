"""Optional external operations barrier; not a mathematical premise.

Set RESEARCH_OPERATIONS_STATE when running within a monitored campaign.
No host configuration, account, credentials, or barrier is modified here.
"""
import json
import os
from pathlib import Path


def operations_allow():
    name = os.environ.get('RESEARCH_OPERATIONS_STATE')
    if not name:
        return
    root = Path(name)
    for directory in (root, root/'monitor'):
        for marker in ('PAUSED', 'PAUSED.json'):
            if (directory/marker).exists():
                raise ValueError('Operations pause: no new computation')
        handover = directory/'HANDOVER.json'
        if handover.exists() and json.loads(handover.read_text()).get('phase') != 'completed':
            raise ValueError('Incomplete handover: no new computation')
    health = json.loads((root/'monitor/health.json').read_text())
    if health['credit_budget']['status'] != 'authorized':
        raise ValueError('Operations budget barrier: no new computation')


def operations_blocked():
    try:
        operations_allow()
    except ValueError:
        return True
    return False
