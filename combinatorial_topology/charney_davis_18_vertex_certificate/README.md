# Charney–Davis for eighteen-vertex flag homology 5-spheres

This package gives a complete computer-assisted proof of

    gamma_3(Delta) = f_2(Delta) - 6 f_1(Delta) + 332 >= 0

for every finite flag generalized homology 5-sphere over a field with
exactly eighteen vertices. Every face link must have sphere homology.
The new result is pending independent mathematical review.

The [proof](PROOF.md) chooses a facet containing as many cubic complement
vertices as possible. Its ridge completions leave six further vertices.
The resulting incidence graph has only 25 possible types, covering 3,471
labelled patterns. Every associated necessary-condition system is excluded.
No sphere census or external graph catalogue is assumed.

The [encoding](ENCODING.md) and [case generator](cases.py) make the finite
reduction explicit. [EXPECTED.json](EXPECTED.json) records all input and
certificate hashes. All 25 DRAT proofs passed DRAT-trim; their LRAT
translations passed the standalone [strict RUP checker](strict_rup.py),
which checked 28,938 additions and 1,924,778 propagation hints. This checker
imports no solver and rejects unsupported RAT hints. Neither it nor the
human reduction is proof-assistant formalized.

## Reproduce

Recorded environment: CPython 3.12.14 for generation, PySAT 1.9.dev15,
PBLib/pypblib 0.0.4, Glucose 4.1, GCC 12.2.0, and CPython 3.11.2 for the
separate strict checking pass. A C/C++ compiler, make, and SWIG may be
needed to build dependencies. Run from this directory. Put generated
formulas, traces, and third-party builds outside the source checkout.

```sh
CD18_WORK=/tmp/cd18-certificate
mkdir -p "$CD18_WORK"
python3 -m venv "$CD18_WORK/venv"
"$CD18_WORK/venv/bin/python" -m pip install -r requirements.txt
git clone https://github.com/marijnheule/drat-trim.git "$CD18_WORK/drat-trim"
git -C "$CD18_WORK/drat-trim" checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C "$CD18_WORK/drat-trim" drat-trim
"$CD18_WORK/venv/bin/python" audit.py
"$CD18_WORK/venv/bin/python" prove.py --work "$CD18_WORK/proofs" --drat-trim "$CD18_WORK/drat-trim/drat-trim"
```

The final line must report that all 25 cases have checked DRAT and LRAT
certificates. The staged reference run used about four minutes for generation,
solving, and certificate checking. Allow approximately 0.5 GB for the generated
inputs and certificates; none is committed here. Each system has at most
266,597 Boolean variables including auxiliaries and 738,277 clauses.
The 25 formulas contain 14,368,101 clauses in total.

`--case 5_0079` selects one case, including the path where the contradiction
is found during initial unit propagation. A final empty-clause step is
supplied when needed and must still be justified by both checkers. To check
an already generated certificate using only the standard library:

```sh
python3 strict_rup.py "$CD18_WORK/proofs/3_0007.cnf" "$CD18_WORK/proofs/3_0007.lrat"
```

For optional validation with a separately implemented integer encoding:

```sh
"$CD18_WORK/venv/bin/python" -m pip install ortools==9.15.6755
"$CD18_WORK/venv/bin/python" independent_cp.py --seconds 300 --output "$CD18_WORK/independent_cp.json"
```

All 25 systems were independently reported INFEASIBLE; recorded solver time
was 325.80 seconds with one worker and seed 1. This agreement uses different
degree formulas and encodings, but the same mathematical reduction. It is
corroboration, not a replacement for the checked proofs. Timeouts are failures
to complete a check, never nonexistence evidence.

## Checks and limits

[audit.py](audit.py) matches [AUDIT.json](AUDIT.json):

- 4,608 vertex-link identity checks on deterministic arbitrary graphs;
- 1,344 exhaustive truth assignments for signed and conditional encoders;
- all 2,025 face links of an explicit sphere with gamma=(1,6,9,0), checked
  over F_2, together with positive and negative CNF controls;
- one valid certificate control accepted and seven malformed controls rejected.

The explicit sphere is a join of two nine-vertex flag 2-spheres obtained
by stated edge subdivisions of an octahedron, so its spherehood over every
field also follows from the construction.

During validation, an exploratory CaDiCaL trace failed DRAT verification and
was discarded. Separately, the bundled legacy `lrat-check.c` accepted a
no-hint empty clause in a negative control. It is **not** a trusted checker
for this package. The final evidence uses only the Glucose traces, successful
DRAT checks, and successful strict RUP checks. The invalid empty-clause
control is rejected by both of these final checking paths.

The trust boundary includes the published Davis–Okun and Labbé–Nevo results,
the written reduction, CNF generation and its exact encoders, and the proof
checkers. No solver infeasibility assertion is taken on trust in the main
proof. There is no claim of a classification of all spheres, an unrestricted
Charney–Davis theorem, or independent peer acceptance. See [PROOF.md](PROOF.md)
for provenance, coefficient-field details, and the cumulative consequence
when combined with the previously accepted seventeen-vertex theorem.
