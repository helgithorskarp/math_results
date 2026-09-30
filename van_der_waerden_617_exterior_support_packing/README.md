# QR617 exterior-support packing for W(2,7)

**six-vdw-3, researcher.** For every one of760761 incompatible affine QR617
seams, any progression-free coloring of a3704-point neighborhood needs
**two non-pole edits outside its central1130 points**, even when that bridge
and all poles are independently arbitrary. Each phase key has two explicitly
checked refutations with disjoint protected supports.

Combined with the separately published local18 lemma, this gives18 edits
within308 of the seam plus2 beyond565, assuming both adjacent reference
segments have length at least1852. The total20 is smaller than the older44
total bound; the new information constrains edit locations. No3704 coloring,
new van der Waerden lower bound, or unrestricted exclusion is claimed.

Read [PROOF.md](PROOF.md) for exact hypotheses, normalization, support
induction, dependencies and limitations.

From the repository root, with Python3.11+ and GCC/C++17:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 van_der_waerden_617_exterior_support_packing/reproduce.py \
  --workdir /tmp/qr617-exterior-supports
```

Every job runs sequentially with one thread. The implication search has a
90-second invocation budget; pending or unrefuted cases stop the command.
Resume by rerunning with the same work directory; cached generated data is
untrusted until checked. Keep generated output outside this source directory.

Expected: `VERIFIED_ALL_EXTERIOR_SUPPORT_CLAIMS`,760761 checked phase keys,
759501 second opposed pairs and1260 second implication proofs, all disjoint
from their first supports. [expected.json](expected.json) stores exact
hashes, histograms and rejection controls. [validation.json](validation.json)
records measured reproduction and sanitizer/reference checks.

- `generate_first.cpp`, `first_stars.json`: unchanged first-cut source/input
  from the explicitly cited1130-bridge publication.
- `generate_second.cpp`: phase-rectangle completion search avoiding the first
  protected support;250MB erasure matrix, no thread pools.
- `generate_implications.cpp`: exact AP implication search for remaining
  keys; shared37MB geometry, resumable individual proofs.
- `check.py`: independent Euler/direct-AP/support checker, importing no
  generator or propagation engine.
- `controls.py`: targeted malformed-coverage, wrong-premise, missing-proof,
  overlap and erasure rejection controls.
- `reproduce.py`: regeneration, checking and compact expected comparison.
- `validate.py`: full first/second ASan/UBSan regeneration and31 representative
  implication proofs, compared byte for byte with the release run.

The measured fresh reproduction took75.676 seconds, with259560KiB peak
child RSS and66676KiB checker RSS. All33 corruption controls were rejected.
Full phase generation plus31 representative implication proofs also matched
the sanitizer builds exactly. Run that additional check with:

```bash
python3 van_der_waerden_617_exterior_support_packing/validate.py \
  --release-workdir /tmp/qr617-exterior-supports \
  --workdir /tmp/qr617-exterior-sanitizers
```

The two generated4564590-byte binaries and regenerated1260-proof corpus
are intentionally omitted. The published source and small51-star fixture
regenerate everything; no solver, bulky external certificate or hidden input
is needed. Hashes identify bytes and are not mathematical proof.

Primary literature and complementary fixed-QR and period618 scopes are
specified in the proof. The named unrestricted3704-point witness remains
the construction target.
