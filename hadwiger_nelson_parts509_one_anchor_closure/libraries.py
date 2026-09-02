"""Witness-colouring libraries of G − u (repository version): base colouring, swap families and pair-closure rows
(pair_closure.load_all + pair_certificate.json), and the layer-(i) rows of the triple closure decoded from
triple_certificate.json (family_rows_base64 / family_sizes, 2-bit packing, same as the pair certificate).
Identical content to the scratch loader (cluster_U.load_libraries) that produced the certificate."""
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
    npair = ntrip = 0
    for cert_path, counter in ((PAIR / 'pair_certificate.json', 'pair'), (TRIPLE / 'triple_certificate.json', 'triple')):
        cert = json.loads(cert_path.read_text())
        packed = base64.b64decode(cert['family_rows_base64'], validate=True)
        assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
        pos = 0
        for u, size in enumerate(cert['family_sizes']):
            for _ in range(size):
                row = unpack_row(packed[pos:pos + RB], u); pos += RB
                parts.validate_coloring(N, edges, row, K, u)
                lib[u].append(row)
                if counter == 'pair': npair += 1
                else: ntrip += 1
        assert pos == len(packed)
    return parts, edges, lib, qnb, qq_edges, ntrip
