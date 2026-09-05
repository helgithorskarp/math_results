# Any two added plane points preserve four-colourability of the dense506 hosts

**One fixed four-colouring of each specified 506-vertex host extends after
any two points of the Euclidean plane are added.** Neither host can yield
a five-chromatic graph with at most 508 vertices through point addition.

The hosts are the two exact maximum-contact examples from the
[dense reflected gadget construction](../hadwiger_nelson_dense506_origin_attachment/README.md).
They each have 506 vertices and 2,389 strict unit edges. Their coordinates,
the two algebraic rotations, and the universal extension argument are in
[PROOF.md](PROOF.md). This is a closure of a fixed geometric completion
family, not a record improvement.

The finite reduction covers arbitrary plane points. An unknown point
with at least three host neighbours is the unique unit-circle centre of
a host triple. The exact census finds 1,420 such nonhost points. Under the
published fixed colouring every one has an available colour, and no unit
pair forces both endpoints to take the same singleton colour. Points
with at most two host neighbours each have at least two available colours
and are handled directly by the proof.

The certificate is one **507-byte colour row**. The independent audit
reconstructs all 1,420 candidate points, their 5,710 host incidences and
3,975 mutual unit edges, then explicitly colours all 1,007,490 candidate
pairs. No new SAT call or large certificate is needed.

## Reproduce

From this directory in a complete repository checkout, with Python 3.11
or later and only the standard library, choose a work directory that does
not yet exist:

```bash
python3 verify.py --work /tmp/hn-dense-two > /tmp/hn-dense-two.json
cmp expected.json /tmp/hn-dense-two.json
python3 audit.py --work /tmp/hn-dense-two > /tmp/hn-dense-two-audit.json
cmp expected_audit.json /tmp/hn-dense-two-audit.json
python3 controls.py > /tmp/hn-dense-two-controls.json
cmp expected_controls.json /tmp/hn-dense-two-controls.json
sha256sum -c SHA256SUMS
```

The producer writes its exact candidates and incidences in the external
work directory. The audit reconstructs them independently and compares
entries, rather than relying only on aggregate counts or their hashes.
Its modular predicate, coordinate representation and circumcentre formula
differ from the producer's. Both versions scan all 21,464,520 host triples;
the producer removes known host-centred triples early. Only exact arithmetic
is used for mathematical decisions.

`controls.py` includes elementary circle fixtures, both rotations, exact
field inverse checks, the complete two-list criterion, a small exact
triple census and invalid-colouring rejection. `validation.json` records
measured costs on CPython 3.11.2. Allow roughly a minute for the independent
audit. No native build or external package is required.

## Inputs, provenance and limits

The exact source points and generic eight-basis arithmetic are reused from
prior committed artifacts and pinned in `SHA256SUMS`. The host colour row
is taken from the previously verified dense attachment library; this package
checks it directly on the rebuilt host graph. It does not rely on the
source gadgets' advertised forcing properties or minimality.

The public package contains source, the compact colour row and expected
results. It omits the generated candidate table and pair-witness stream;
both are reproducible. The independent audit is alternative implementation
checking by the author, not external peer review. The universal geometric
and field reductions are not formalized in a proof assistant.

This pass closes arbitrary additions of at most two vertices to these two
fixed embeddings. Three-point addition would exceed 508 unless accompanied
by deletion and is a separate family. No deletion/addition construction
or other host is investigated here.

Primary record context: [Parts' graph-minimization paper](https://arxiv.org/abs/2010.12665)
reports 509 vertices, and [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4)
still identifies it as the unrestricted record. This work establishes no
five-chromatic graph of order at most 508.
