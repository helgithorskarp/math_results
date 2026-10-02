"""Adapter reconstructing the sealed first record from the unchanged core.

Written after the seal. domains/propagate/common are byte-identical to the
three modules used before reading any author executable or certificate.
"""
import hashlib
import json
from pathlib import Path
from common import digest, require
from domains import profiles, exceptions, initial
from propagate import close


def main():
    base = Path(__file__).resolve().parent; seal = json.loads((base/'first-seal.json').read_text())
    for name, expected in seal['source_sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest() == expected, 'first core changed')
    record = {'profiles': [], 'cases': []}
    for index, profile in enumerate(profiles()):
        selected, raw = exceptions(profile)
        record['profiles'].append({'profile': profile, 'exception_tuples': selected, 'raw_symmetric_tuples': raw})
        for exception in selected:
            rows = initial(profile, exception); result = close(profile, rows)
            record['cases'].append({'profile': index, 'exception': exception, 'domain_sizes': [len(row) for row in rows],
                                    'whole_initial_sha256': digest(rows), 'initial_empty': result['initial_empty'],
                                    'closed': result['empty'], 'deletion_sha256': digest(result['batches']),
                                    'batches': len(result['batches']), 'support_tests': result['tests']})
    require(digest(record) == seal['whole_first_record_sha256'], 'whole first record differs')
    # The original in-memory group keys are integers; JSON object keys are
    # strings. Preserve the sealed original numeric-key serializer, while
    # comparing every stored field after the explicit JSON round trip.
    stored = json.loads((base/'first-record.json').read_text())
    require(digest(json.loads(json.dumps(record))) == digest(stored), 'all first-record fields')
    print(json.dumps({'all82_closed': all(row['closed'] for row in record['cases']),
                      'whole_first_record_sha256': digest(record)}, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__': main()
