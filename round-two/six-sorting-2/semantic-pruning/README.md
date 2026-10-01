# A strict refinement of weighted extreme pruning

**six-sorting-2, researcher.** Every extension of the explicit eleven-gate
thirteen-input prefix in `fixture.json` to a sorting network has at least
**45 comparators**, at arbitrary depth. All its gates are globally active,
and its ordinary one-/two-extreme weighted checks pass.

The new bound also counts comparators that become redundant after fixing
original inputs to extrema. For one minimum and one maximum, the ordinary
mass is **388** and the resulting semantic mass is **524**. Every size-44
sorter has mass at most `2^(44-S(11))=512`. This follows from published
`S(11)=35`; no global size-44 exclusion or size-44 construction is claimed.
The overall thirteen-input frontier remains **44..45**.

[PROOF.md](PROOF.md) gives the general bound
`m >= S(n-l-h)+ceil(log2 V_l,h(P))`, its proof, the precise clamping and
orientation conventions, and attribution to the prior weighted and
saturation/activity methods. Conditional truth tables must be kept for
every original marked family; sharing a marker position alone does not
justify identifying those truth tables.

## Reproduce

Standard-library Python **3.11 or later**, one CPU job and one thread:

```sh
cd round-two/six-sorting-2/semantic-pruning
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate.py
python3 -B verify.py
python3 -B profile.py --network fixture.json --field prefix --budget 44
```

The first command reproduces `certificate.json` byte for byte. The scalar
checker imports no producer code and compares every marked-family entry
and prefix profile. Expected statuses are `GENERATOR_CHECKS_PASSED` and
`ALL_INDEPENDENT_CHECKS_PASSED`, with 1,491,264 scalar free assignments,
41,748,192 scalar gate evaluations, 13941 local marker transitions and
three rejected corruptions. It also checks the known size-45 control on
all 8192 original Boolean inputs. The final command reports a first
rejection at **cut 11**, mixed family, mass **524**, and lower bound **45**.

Certificate SHA256:

    5bd4434dde232e3d91a2faddef1e17657b929f96a4f97d40d0298ae8031f3775

With CPython 3.11.2, generation took 0.153 seconds and scalar verification
16.281 seconds / 17140 KiB peak RSS. Measurements vary by host. No solver,
download, third-party package or large generated artifact is needed.

## Use on another prefix

Provide JSON with `{"n":13,"gates":[[a,b],...]}` and run:

```sh
python3 -B profile.py --network PATH --budget 44
```

For a Python caller, `profile.analyze(n, gates)` returns the five exact
family profiles, including every prefix trace and original-family costs.
`profile.lower_bound(n, family_data)` returns its rigorous necessary
size bound using the published small sorter values recorded in the
source. `analyze_family(n,gates,l,h)` computes a selected marked family.
Gate `(a,b)` is oriented: min goes to `a`, max to `b`. The core supports
orders 2..13 and arbitrary orientations; the supplied fixtures are
standard gates with `a<b`.

Reject a candidate prefix if the necessary bound exceeds the target
size. Passing supplies no sorting or extension certificate. Boolean
truth-table execution and the written pruning/threshold/standardization
proof are explicit trust boundaries. Both implementations are by this
researcher, rather than an external reviewer or a formal proof assistant.

The fixture records the primary size source, incumbent source and
published graph context. Exploratory random search and local Git state
are outside this source package. The witness is a strict test case for
this interface, not a priority claim for general pruning or a classification
of all thirteen-input prefixes.
