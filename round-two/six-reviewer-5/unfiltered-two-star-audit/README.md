# Complete unfiltered two-star audit

Actual agent: **six-reviewer-5, independent mathematical reviewer**.

This independently confirms six-code-3's local two-star lemma9098 and
proves sharper conclusions: its uniform66 is sharp; its multiplicity-four
subcase has sharp63; the earlier covered-triangle subcase9045 has sharp58.
See [the self-contained review](REVIEW.md) for the exact hypotheses.
No unrestricted numerical bound or whole-code classification is claimed.

Run offline with standard-library CPython3.12.14 (tested), from the repository
root. Generated data must remain outside this contribution directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-reviewer-5/unfiltered-two-star-audit/reproduce.py \
  --work scratch/unfiltered-normal
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B -O round-two/six-reviewer-5/unfiltered-two-star-audit/reproduce.py \
  --work scratch/unfiltered-optimized
```

Expected: `PASS_COLD_COMPLETE_UNFILTERED_REVIEW`, all548 raw-positive
transports, all34 residual graphs, maximum66 and multiplicity-four maximum63.
[EXPECTED.json](EXPECTED.json) contains every frozen representative record.
Its canonical compact JSON hash, without newline, is
`9bff2907067c5ba605ddfaa275a30bb92644edef34eaafbc3c4ff5fbac90903b`.
The whole source-file byte hash is in [SHA256SUMS](SHA256SUMS).

The fast lower-certificate command imports no enumeration or search module:

```sh
python3 -B round-two/six-reviewer-5/unfiltered-two-star-audit/check_witness.py
```

It checks all34 literal [completion witnesses](WITNESSES.json), including
66-word row6,63-word multiplicity-four row27 and58-word covered-triangle row18.
The witness-list canonical hash is
`438ea4bc030c04d8bd29c7d9913f5c720afe36fdde30a4979edeec295ff64980`.

[audit.py](audit.py) freshly decodes the researcher cores, independently
rebuilds all candidate universes by pair intersections, builds graphs by
triple incidence and checks every adjacency by literal sets. It checks the
positive researcher color arrays, computes all exact unweighted maxima,
and checks complete candidate/color transports for all548 raw interfaces.
[controls.py](controls.py) checks all1100 simple graphs on at most five
vertices against exhaustive subset maxima and rejects21 semantic/input
damages. Normal and optimized runs compare the entire frozen mathematical
record and every positive completion, rather than only aggregate hashes.

The byte-identical [raw carrier](raw_carrier.py), fixture and two old seed
arrays come from this reviewer's published9076 source
`4977fd9bc9a81ca4317c596935d48105028e3d54`.
The byte-identical [clique algorithm](clique.py) and guard/literal helpers
come from this reviewer's published9115 source
`b701fed831d85c668c7c0d92281ff3e8db052216`.
Researcher data [BRIDGE.json](BRIDGE.json) and
[AUTHOR_COLORS.json](AUTHOR_COLORS.json) come from9098 source
`889e97cfb0062c4af143608b9922e4acbce28784`; the former originated in9045.
[INPUTS.json](INPUTS.json) pins every imported file. No researcher executable
is imported into this audit. This continues the same independent reviewer;
it is not another distinct reviewer or a fresh authorship identity.

The raw carrier cold replay imports the reviewed generic23-star coverage
8933 conditional on universal8323. Supplied groups are used only for actual
checked positive point transports, never to discard a raw case. Their
maximality is unnecessary. The raw search is unquotiented.

Fixed guards: raw map calls200000 nodes/10seconds, raw whole180seconds;
clique calls3000000 nodes/30seconds; full audit240seconds. Every limit or
incomplete run raises and proves no absence. Jobs are serial, threads1,
unchanged1CPU/2GiB. Runtime and scope are recorded in
[VALIDATION.json](VALIDATION.json). Full transient191-million-map accounting,
548 transport records and logs are regenerated into `--work`, not published.
There is no proof-assistant formalization or independently checked search
trace; ordinary completeness and clique/color bridges and Python remain
the explicit trust boundary.
