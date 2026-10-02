# Independent cross-repeated leaf audit

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms the new main theorem of LEMMA9461 in its
specified neighborhood and exact degree carrier \(9^4,10^{18}\).
Its secondary whole-leaf corollary retains the explicit imported Y-repeated
finite premise; the previously sufficient X-repeated audit is credited.
This packet proves additional necessary degree-sensitive page-deficit
identities and weighted positivity, without excluding the full degree carrier
or determining the Ramsey number.

Use CPython3.11+ and g++12.2/C++17, standard libraries only. Set
OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, NUMEXPR_NUM_THREADS,
VECLIB_MAXIMUM_THREADS and BLIS_NUM_THREADS all to1. Children run serially;
each direct compile/mathematical stage has a fixed60-second guard.

From the repository root:

```sh
python3 round-two/six-reviewer-4/cross-leaf-audit/reproduce.py \
  --out scratch/cross-own --compare round-two/six-reviewer-4/cross-leaf-audit/RESULTS.json
python3 round-two/six-reviewer-4/cross-leaf-audit/fetch_inputs.py --out scratch/cross-author
python3 round-two/six-reviewer-4/cross-leaf-audit/corroborate.py \
  --author-dir scratch/cross-author --out scratch/cross-author-replay
python3 round-two/six-reviewer-4/cross-leaf-audit/check.py \
  --out scratch/cross-normal --author-full scratch/cross-author-replay/author-full.json
python3 -O round-two/six-reviewer-4/cross-leaf-audit/check.py \
  --out scratch/cross-optimized --author-full scratch/cross-author-replay/author-full.json
```

Compare the two regenerated `mathematics.json` files byte-for-byte. Their
recorded mathematical digest and actual runs are in [evidence.json](evidence.json).
The author replay is split at its original function boundaries, with its
source functions unchanged; it is later corroboration, not independent evidence.
Full target source hashes are in [AUTHOR_SOURCE.json](AUTHOR_SOURCE.json).
The author source is downloaded rather than republished here.

[census.cpp](census.cpp) regenerates all836 X interfaces,52664 endpoint
frames and every2018064 Cartesian tuple in4500 nonempty domains. Exactly192
actual-tagged joins remain and each already contains a known-edge red book.
The entire3438378-byte independent record has SHA256
`723bb6410697587ac4a2432f243536f5a7bb00dbab5b9b420ac168afe88fafa8`.
[first-seal.json](first-seal.json) records the whole record and unchanged core
hashes before opening the new target programs/fixture. The defining proof,
coordinates and claimed totals were visible; this is not a blind review.
Standard subset minima and orbit normalization are credited techniques.

[compare.py](compare.py) reconstructs the complete Xi candidate domains
using separate literal Python neighbor sets and compares every physical entry
in all five author inventories. It also independently checks all1105944
endpoint pairs and all192 witnesses. The four assigned SY--Q red spines have
sorted page vectors `(3,3,3,4)` in160 joins and `(3,4,4,4)` in32: their sums
exceed the total cap12. This is a finite certificate refinement.
[controls.py](controls.py) tests all24 core relabelings with3960 individual
low transports,1440 ordered SX transports,92160 Q-tag transports,4096 exact
subset pairs,1152 physical witness transports and14 adverse encodings/records.
The credited primary21 positive fixture has93 red edges and page maxima3/6.
[structure.py](structure.py) checks signed deficit identities and exact energy
equalities on24 distinct four-low degree-preserving controls and four varied
degree controls. These are not valid host constructions or sampled proofs of
universal positivity.

Full release and AddressSanitizer/UndefinedBehaviorSanitizer censuses compare
all streams, not only totals. Generated multi-megabyte domains, binaries,
temporary downloaded source and logs stay in scratch. Only compact expected
results, source and receipts are published. Correct ordinary coverage,
normalization, finite code correspondence, integer tooling and the imported
secondary premise remain unformalized trust boundaries. A timeout or killed
run supplies no exclusion; no resource limit is increased.
