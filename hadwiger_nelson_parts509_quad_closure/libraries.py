"""Witness-colouring libraries of G − u (repository version): base deletion colouring, swap families, pair-closure rows
and triple-closure layer-(i) rows, all decoded from the sibling certificates (2-bit packing, 127 bytes per row) and
validated as proper 4-colourings of G − u against the exact edge list (the 26 Q2K-cluster fresh rows of the triple
certificate are not used; identical content to the scratch loader that produced the certificate)."""
import base64, hashlib, json, importlib.util
from paths import PAIR, TRIPLE, N, K


def unpack_row(raw, u):
    vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
    it = iter(vals)
    return [-1 if v == u else next(it) for v in range(N)]


def load_libraries():
    spec = importlib.util.spec_from_file_location('pc', PAIR / 'pair_closure.py')
    pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
    parts = pc.load_parts()
    points, edges, rows, fams, qnb, qq_edges = pc.load_all()
    lib = [[rows[u]] + list(fams[u]) for u in range(N)]
    RB = (N - 1) // 4
    counts = {'base': N, 'swap': sum(len(f) for f in fams)}
    for cert_path, name in ((PAIR / 'pair_certificate.json', 'pair'), (TRIPLE / 'triple_certificate.json', 'triple')):
        cert = json.loads(cert_path.read_text())
        packed = base64.b64decode(cert['family_rows_base64'], validate=True)
        assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
        pos, n = 0, 0
        for u, size in enumerate(cert['family_sizes']):
            for _ in range(size):
                row = unpack_row(packed[pos:pos + RB], u); pos += RB
                parts.validate_coloring(N, edges, row, K, u)
                lib[u].append(row); n += 1
        assert pos == len(packed)
        counts[name] = n
    return parts, edges, lib, qnb, qq_edges, counts
