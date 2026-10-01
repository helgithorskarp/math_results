# Reproduction and trust boundaries

Actual author **six-books-3**, role **researcher**, 2026-10-01.

All commands in README passed with CPython 3.11.2 on one CPU. The
resource scope remained one CPU and two GiB; all thread settings were
one. No process or solver limit was raised. Measured wall times were
5.57s for byte-identical generation, 36.92s for the generator-free
checker under `python3 -O`, 39.35s for full generator comparison and
1.96s for literal/forgery controls under `python3 -O`. Observed peak
child RSS was at most 23072 KiB. These are operational observations,
not mathematical premises.

The independent implementation replayed all 256500 labeled local cores
and compared **25650000** full local-incidence entries under explicit
coordinate maps. It covered all **43** admissible six-point rows across
the 56 normalized profiles, mapped them to all **42** selected cases,
and preserved each residual-base entry and slack degree. The comparison
mode checked equality of the complete integer-weighted state sets and
**4019100** residual entries. All **40191** matrices had a strict
negative integer quadratic form. There were no survivors or partial
states. The certificate has 208 primitive ten-coordinate vectors.

The controls apply degree-preserving switches to 252 circulants and
check five roots in each, for **1260** regular-graph root controls. They
check 12600 column identities, 13860 outside-degree identities, 56700
pair identities, 12600 incident slack identities, and 3792 literal
six-row removals (379200 entries). There are 1522 successful switches.
The control graphs generally fail the book caps: unused capacities
may be signed there, and the algebraic identities still hold. They
are not Ramsey witnesses. Seven deliberately invalid certificates
are rejected, with guards active under optimized Python.

SHA-256:

* F domain, sorted decimal masks with a newline per mask:
  `290e3fcbb46e49ad49919091b69c23aa33e23cc488bf58e667d7a6c144ad25cf`.
* Complete ordered state/matrix stream:
  `dd25b0f2147d1c60a017ba092c71cb0046e8be92fa89b2d79bfd5bf68403ddd4`.
* Compact `negative_vectors.json`:
  `144a039f884b096d5fb01ccf998eddaeadfbac05a4c4a208d0c2ed54b04c0c43`.
* Known primary red-complement `baseline21.rows`:
  `4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.

The original primary 21-vertex matrix bytes were fetched on 2026-10-01,
SHA-256 `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
All 441 entries agree after complementing its blue color. The red graph
has 93 edges, degree multiplicities 8:4,9:16,10:1, and maximum red/blue
codegrees 3/6. This is baseline reproduction. The located primary
status remains 22 <= R(B4,B7) <= 23.

The conditional local2^4,3^6 theorem uses no earlier finite computation.
The thirteen-edge corollary uses the positive-codegree result at
commit `7400e3949d93733d2050118e0557d94a8a8f1625`, graph
`bafkreid6vw7ktqeizndog5fdazervle4elnf6gvf7iqcjvsqdczxioidum`.
The 110-edge-host application uses the maximum-degree bound at commit
`ce3177a731086284ee89f18a8a3948b672b3c64e`, graph
`bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
The proof audit of that latter dependency is by six-reviewer-1 at
commit `b3e45c1ca194e1becece046ed2e4695f9692406c`, graph
`bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m`.
That audit does not review the present theorem.

Exact integer certificates close the finite matrix exclusion. The
incidence and exhaustive-coverage bridges remain written mathematics;
two implementations by one author are not independent peer review.
There is no host symmetry, connectivity assumption, solver status,
floating-point output or determinant heuristic in the conclusion.
