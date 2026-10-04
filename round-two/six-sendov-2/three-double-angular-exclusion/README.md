# Three-double angular exclusion

**six-sendov-2 / researcher**, 2026-10-04. Complete ordinary author proof
with exact algebraic certificates, **unformalized and independently unreviewed**.

Every normalized real eight-original profile with four strict positives,
four strict negatives, zero first/third/fifth moments and exactly three
distinct doubles plus two singles has angular coefficient **C<16**.
The bound is sharp as a limiting supremum. The proof classifies the ENTIRE
stratum by one physical parameter, retains all original multiplicities
and all seven critical slots, and proves both complete positivity
certificates on an interval containing every physical parameter.

Together with the credited prior quartet/triple reduction and all-distinct
local-maximum exclusion, this leaves only **one or two original doubles**
for a constrained local maximum with C>=47/2. That reduction is necessary,
not an existence or global-maximum theorem. The uniform complex first-power
inequality and angular monotonicity on a feasible quartet path remain open.

Read [PROOF.md](PROOF.md) for the complete ordinary argument and
[LITERATURE.md](LITERATURE.md) for exact dependency scopes and primary status.
The [certificate](CERTIFICATE.json) is4688 bytes and the entire
[expected record](EXPECTED.json) is27941 bytes, with every coefficient
and all three actual seven-slot specializations.

From this directory, Python3.10+ standard library:

    python3 -I -B verify.py --self-test
    python3 -I -B -O verify.py --self-test

Both return the whole-record SHA256
740cee543853acd8064ccbb6f24c1d92908a18ce605fb2b6d5d7b8ad7040c137,
27941 bytes, eight rejected altered mathematical certificates, and
C<16 for every physical member; supremum16 only as r descends1.
No proof gate uses Python assertions. To save the reconstructed record,
add --record /path/outside/the/source/record.json. The decoder rejects
noncanonical rational strings, wrong types, duplicate keys, missing/extra
certificate fields, wrong dimensions and oversized inputs.

Optional exact dense comparison requires SymPy1.14.0:

    python3 -B compare_cas.py

It rebuilds the ENTIRE certificate and three actual full seven-slot
records, importing no native-checker module. The whole-certificate SHA256 is
5ad1162d0465865db03b7032e7f27137b801f383f0e5f5825f75e277672fd521.
Its Bernstein vectors are recovered by exact interpolation in the
Bernstein basis; the native route uses a complete coefficient conversion.
These are same-author corroborations, not independent peer review.

Author validation uses local and cold public-source-only normal/optimized
runs, every mathematical mutation in each mode, whole expected-fixture
rejections, and the optional dense CAS route. Full output must match;
an accepted subset or aggregate count is insufficient. All six
BLAS/OpenMP/native-library thread variables are1. Children run serially
under45-second guards, with a50-second outer guard, within the unchanged
1CPU/2GiB process scope. No resource limit is used as a mathematical premise.
Bulk logs, timing/resource receipts, private probes and checkpoints stay local.

The recorded CPython3.12.14 suite passed four local/cold normal/optimized
positives, all eight mathematical mutations in each positive, eight
external whole-record fixture rejections, twelve external certificate
decoder rejections, and one cold dense CAS rebuild. Peak child memory
was21908KiB for the native/fixture suite and60000KiB including CAS.
The25 serial children finished without a resource limit or timeout.

The exact polynomial identities are checked by arbitrary-precision
arithmetic. Classification, actual root count, nonzero specialization,
compression interpretation and Bernstein positivity remain ordinary
written mathematics. No formalization or verdict transfer is claimed.
