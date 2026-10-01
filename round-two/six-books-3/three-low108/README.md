# Exact full-root exclusion in the one8+two9 sector

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid ordinary (B4,B7) graph on22 points, with108 red edges, maximum
degree ten and degree pattern one8+two9 cannot have a full Petersen root.
With credited8828, it therefore has no full root. The existing seven-root
bound of8987 then gives at least seven one-nine roots. With credited8941,
8979 and8012 upper10, a full root at108 is possible only in the four-nine
pattern. No remaining host existence/exclusion or Ramsey endpoint follows.
[PROOF.md](PROOF.md) supplies the complete ordinary and finite arguments;
new independent review and formalization are pending.

Run from the repository root, **sequentially**:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 round-two/six-books-3/three-low108/produce.py
python3 round-two/six-books-3/three-low108/verify.py
python3 round-two/six-books-3/three-low108/controls.py
python3 round-two/six-books-3/three-low108/controls.py --summary-only
python3 -O round-two/six-books-3/three-low108/produce.py
python3 -O round-two/six-books-3/three-low108/verify.py
python3 -O round-two/six-books-3/three-low108/controls.py
python3 -O round-two/six-books-3/three-low108/controls.py --summary-only
```

CPython3.11.2, standard library only; no solver or private data. The two
integrity modes separate jobs within the same45-second guard; both are required.
Default modes compare [expected.json](expected.json), and every guard remains
active under -O. Normal runs write only optional Python caches and temporary
summary-control files under /tmp. `produce.py --derive --output PATH` explicitly
regenerates the certificate; `--derive` omits frozen-summary comparison only.
The checker accepts `--certificate PATH --expected PATH` and retains all
mathematical checks. Never interpret an incomplete run as an exclusion.

The producer's full-row/exact-column join and the checker's low8/large quotient
join match all51,240 raw keys entrywise. Supplied462 local representatives
expand to the complete independent raw union. Literal22-point sets rebuild
every outside star domain.423 templates are initially empty,38 have static
pair covers, and one has a seven-step trace removing44 stars. Weighted coverage
is46,740+4,440+60. Static covers use47 groups/87 target stars. No branching or
all-other-full-roots assumption is needed. Equal one-tag rows are sorted
numerically; repeated words are included. Low domains retain all375 two-tag
and582 one-tag words within the proved incidence budget.

The primary21 positive control passes ten actual stars/completion;196
asymmetric changes reject.29 damaged certificates and one forged narrowed
summary reject. Separate author algorithms are validation, not external peer
review. [provenance.json](provenance.json) records exact dependencies;
[manifest.json](manifest.json) hashes every other source file.

Canonical incidence digest:
`49dbd338b5c8911c85e34c4176d23061e3c3cdffe4c69a7f2d0ef8771b3e52e3`.
Canonical certificate digest:
`e9bc3b9b1373aa5df9ff0a70f89caddeb2e63db56fd77068451e0f44fcab1039`.
Source and explicit coverage establish the claim; hashes record agreement.
The first checker hit its45-second guard; exact caching then completed its
full audit in20.8s/104MiB without changing that guard or resources. The compact
certificate regenerates all omitted incidence/star data. Current Ramsey
status remains22..23.
