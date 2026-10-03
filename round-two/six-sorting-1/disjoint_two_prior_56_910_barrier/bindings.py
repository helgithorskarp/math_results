"""Inputs are newly reconstructed, never a previous branch's negative corpus."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def selected_offsets(first, last):
    preparation = json.loads((ROOT/'work/preparation-phase-complete.json').read_text())
    previous = json.loads((ROOT/'work/reserve-phase-complete.json').read_text())
    for row in (preparation, previous):
        need(digest(row['finite']) == row['finite_sha256'], 'Changed fresh phase binding')
        need(row['finite'].get('entire_normal_O_records_equal',
             row['finite'].get('entire_normal_O_finite_records_equal')), 'Full normal/O phase comparison absent')
    normal = json.loads((ROOT/'work/reserve-preparations-checked.json').read_text())
    optimized = json.loads((ROOT/'work/reserve-preparations-checked-O.json').read_text())
    need(normal['finite'] == optimized['finite'] and
         normal['finite_sha256'] == previous['finite']['preparation_reserve_scalar_finite_sha256'],
         'Fresh original reserve classifications not checked')
    offsets = previous['finite']['remaining_retained_offsets']
    need(0 <= first < last <= len(offsets) and last-first <= 128, 'Bounded new open-function interval required')
    universal = json.loads((ROOT/'universal-10060.json').read_text())
    need(universal['graph_height'] == 10060 and universal['prior_HIGH_merges'] == [[5,6],[9,10]] and
         universal['dead_preparation_ports'] == [2,3,4,5,8,9] and universal['conditional_input'] == 40,
         'The literal published10060 route is different')
    return offsets[first:last], previous, universal, universal['graph_ref']
