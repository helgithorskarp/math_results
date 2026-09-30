"""Optional passive entry-level comparison, NOT an independent proof premise.

six-reviewer-1, independent reviewer. Executes the pinned author's generator
with one passive observer inserted before every matrix filter. The standalone
audit.py imports no author source, table or vector pool.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n').encode()


def run():
    here = Path(__file__).resolve().parent
    root = here.parent
    provenance = json.loads((here / 'provenance.json').read_text())
    for record in provenance['reviewed_inputs']:
        actual = (root / record['path']).read_bytes()
        require(hashlib.sha256(actual).hexdigest() == record['sha256'],
                'pinned original input changed: ' + record['path'])
    source_path = root / 'book_ramsey_b4_b7_degree11_gram_exclusion/generate.py'
    source = source_path.read_text()
    marker = '                            if any(value < 0 for row in S for value in row):'
    require(source.count(marker) == 1, 'observer site not unique')
    observation = ("                            AUDIT_STREAM.append(((delta, U, K, kind, mask, tuple(t), selected),\n"
                   "                                hashlib.sha256(encoded(S)).hexdigest()))\n")
    observed = []
    namespace = {'__name__': 'pinned_author_observation', '__file__': str(source_path),
                 'AUDIT_STREAM': observed}
    exec(compile(source.replace(marker, observation + marker), str(source_path), 'exec'), namespace)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        namespace['run'](False)
    original_expected = (source_path.parent / 'expected.json').read_bytes()
    require(captured.getvalue().encode() == original_expected,
            'author output changed after passive observation')
    digest = hashlib.sha256()
    for record in sorted(observed):
        digest.update(encoded(record))
    independent = json.loads((here / 'expected.json').read_text())
    require(len(observed) == independent['total']['states'] and
            digest.hexdigest() == independent['all_state_and_matrix_stream_sha256'],
            'complete case/matrix stream differs')
    return {'schema': 'degree11-passive-author-comparison-v1', 'author_cases': len(observed),
            'all_state_and_matrix_stream_sha256': digest.hexdigest(),
            'original_stdout_unchanged': True, 'full_entry_level_comparison_passed': True,
            'author_expected_sha256': hashlib.sha256(original_expected).hexdigest(),
            'source_sha256': hashlib.sha256(source.encode()).hexdigest()}


if __name__ == '__main__':
    print(encoded(run()).decode(), end='')
