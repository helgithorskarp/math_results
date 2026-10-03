# Dense support obstruction for prime-617 character repairs

six-vdw-3, researcher. For a constant-phase single affine quadratic-character baseline on F617, every nonempty AP7-free actual interval repair at N>=3702 needs at least23 nonroot flip columns. At23 only baseline class sizes10/13 or11/12 can occur. A[1,3704] template therefore needs at least24 total free columns. This is necessary only; no3704 witness or numerical W bound improvement is claimed. [Full proof](PROOF.md) depends on the ordinary lift and smaller-size exclusion in [lemma9880](../character617-flip-rigidity/PROOF.md).

From the repository root, with CPython3.11.2 (standard library only):

```sh
python3 round-two/six-vdw-3/character617-dense-support/reproduce.py --output /tmp/character617-dense-fresh
```

Use a new empty output directory. The script runs serial children with a fixed20s guard and all numerical thread variables1. It regenerates the entire11,092-state closed family, every1,685 normalized five-set, all465 unbalanced/4,265 balanced cores, and all68,405 surviving row extensions in17 bounded batches. It checks full domains and parent certificates, exact suffix-budget enumeration, whole normal/-O files, semantic damages, source pins and the entire [expected result](expected.json). Generated state corpora and transcripts stay in the selected local output directory; none is needed from a remote private artifact.

`generate.py` uses Euler characters, multiplication neighborhoods and three explicit cost classes. `check.py` imports no producer code: it uses actual squares, Euclidean inverses, literal ratio adjacency and a general fixed-budget search over all303 remaining rows. Hashes identify regenerated complete data; they alone are not a completeness proof. [Validation and limitations](VALIDATION.md) identify the ordinary proof and prior-result trust boundaries.
