# T375 is vertex-minimal for its marked-colour obstruction

Let `T375` be the exact 375-vertex, 1,661-edge Euclidean unit-distance graph
in the sibling
[`hadwiger_nelson_small_triangle_forcer375`](../hadwiger_nelson_small_triangle_forcer375/README.md),
and let its marked vertices be `t0=0`, `t1=1`, `t2=2`. They form an
equilateral triangle of side `1/sqrt(3)`. The parent result proves that T375
is four-colourable, but has no proper four-colouring in which the three
marked vertices have one colour.

**Exact strengthening.** For every nonterminal vertex `v` of T375, the graph
`T375-v` has a proper four-colouring with

```text
colour(t0) = colour(t1) = colour(t2) = 0.
```

The 372 explicit deletion colourings are checked directly on every surviving
edge. Consequently, if `W` is any proper vertex subset of T375 containing all
three terminals, choose a nonterminal `v` outside `W` and restrict the supplied
colouring of `T375-v` to `W`. Thus **every proper terminal-containing induced
subgraph permits a monochromatic marked triangle**. T375 is inclusion-minimal
by vertices for this marked-colour obstruction.

This closes deletion-only optimization inside the strongest small conditional
forcing support from the earlier Exoo–Ismailescu construction. It makes no
claim of minimum order among all geometric forcing gadgets. It does not produce
a five-chromatic graph on at most 508 vertices, and it does not reopen the
retired E477 spindle or Parts-derived construction families.

## Certificate and proof architecture

The certificate stores one two-bit colour word for each deletion `v=3,...,374`.
Four colours occupy one byte, with the lower-index vertex in the low bits. The
deleted position is a canonical zero and is ignored. All 372 packed words use
34,968 bytes before base64 encoding, and their concatenation has SHA-256

```text
c1a3bd619ac328d2dc5407349033e8237ca3ab35cda88894f2f022110d083e0c
```

`verify.py` uses only Python's standard library. It does not import the parent
geometry producer or its colouring search. It rebuilds the 627-point source
orbit from the 109 appendix rows using exact integer arithmetic, selects the
375 certified labels, checks distinctness, and decides all 70,125 squared
distances exactly. For coordinate rows `[a,b,c,d]`, a difference has squared
length one precisely when

```text
3a^2 + 11b^2 + c^2 + 33d^2 = 1296,
ab + cd = 0.
```

The reconstructed point and edge hashes are

```text
points 0bf15083801eb6fa982b04e820aca6c5a16c9b75b2d85b3efd00c53716edb1fe
edges  0e3d04cf0e0df94e9a7a9adda6677d92db162faf3ab29947dde8e0f52c287660
```

The checker verifies the parent's unpinned four-colouring and reruns the
complete contrary search with the terminals pinned equally. Singleton
propagation followed by minimum-domain branching exhausts 735 nodes and 367
conflicts. It tries all already used colours and one representative unused
colour; unused colour names are interchangeable because the constraints only
compare colours for equality. Every recursive branch fixes another vertex, so
the search is finite and complete. This rechecks the parent obstruction; the
new minimality conclusion then follows from the 372 directly verified positive
witnesses and the restriction argument above. Six malformed-certificate
controls are rejected.

The parent appendix and certificate are hash-pinned in `provenance.json`.
The mathematical construction is due to Exoo and Ismailescu,
[arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1). The standing record
comparison remains Parts's 509-vertex graph,
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also stated by Haugland in
[arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4). No new record claim
is made.

## Reproduction

From this directory, with Python 3.11 or later:

```sh
python3 verify.py
python3 -O verify.py
python3 build_certificate.py
sha256sum -c SHA256SUMS
```

The first two commands print exactly `expected.json`. The producer regenerates
all 372 words deterministically. Its recorded search totals are 108,993 nodes
and 42,351 conflicts, with at most 838 nodes for one query. These production
statistics are not premises of the proof; the final checker trusts only the
decoded colour words, the reconstructed exact graph, and its own complete
baseline search.

## Files

- `certificate.json`: compact deletion-colouring witnesses.
- `verify.py`: exact geometry, complete baseline search, witness checker, and
  malformed-input controls.
- `build_certificate.py`: deterministic certificate producer.
- `expected.json`: canonical verifier output.
- `provenance.json`: pinned parent inputs and source context.
