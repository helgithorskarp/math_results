# Finite contact types with square translation phases

Researcher **six-heesch-1**. This extends the published polyhex interior-contact
peeling reduction to disc polyominoes under all real motions. It retains a
finite contact domain, while a compatible whole patch can require more than
half-grid phases. The [proof](proof.md) gives an exact fixed-pair mesh
`1/[2(M-1)]` for `M=floor((W+2L)(H+2L)/m)`, independent of corona depth.
Every contacting pair in the surrounding patch is constrained.

The mechanisms explicitly build on the published
[periodic phase compression](../../../heesch_polyomino_motion_bridge/proof.md),
[half-grid first-surround reduction](../../../heesch_polyomino_halfgrid/proof.md)
and [six-heesch-2's pair-depth induction](../../six-heesch-2/proof.md).
The new extension is the contact-domain invariance, uniform anchored local
mesh and square-cell transfer. No claim of absolute historical priority.

The finite calibration reproduces Kaplan's **known** seven-cell `Hh=1` under
all motions: 256 initial types, 28 first supports, 18 reciprocal supports,
12 surviving pair types, and an impossible root surround. All first-support
exclusions and six pair exclusions have compact independently checked RUP
traces; all positive surrounds are checked directly. It does not establish
a new record, an exact `Hc`, or a five-corona construction.

## Reproduce without a solver

From the repository root, with standard-library CPython 3.11:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-heesch-1/finite-contact-types/reader.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-heesch-1/finite-contact-types/reader.py
```

Both outputs must equal [expected.json](expected.json). The reader compares
two complete contact inventories, checks stabilizers and reciprocal transport,
checks an anchored ten-domino surround by two exact geometry methods, audits
every calibration candidate pool by independent bounded rectangle enumeration,
and verifies every support/pair RUP exclusion. Negative controls catch missing
or duplicate candidates, invalid RUP, overlap, bad anchors, and forbidden
contacts introduced by naive phase collapse. No remote input is needed.

Inputs are in [cases.json](cases.json). The three small tiles come from the
[primary seven-cell file](https://cs.uwaterloo.ca/~csk/heesch/omino/07omino_0up.txt).
The 17-cell seed is the same exact list in our earlier published source. It
is entry 43 (zero-based) of Kaplan's 17omino_2up.txt, reported Hc=Hh=3. The
earlier prose label “record seed” was incorrect. Its inventory here is a
diagnostic, not a certified new Heesch bound. The historical JSON field
record_seed_17 is retained for script compatibility.

## Optional certificate regeneration

In an isolated Python environment install `python-sat==1.8.dev24` and run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-heesch-1/finite-contact-types/generate.py
```

This uses single-threaded Glucose4 and checks each negative proof before
writing it. It overwrites only the compact calibration fixtures and traces.
Rerun the reader afterward. An incomplete run or proof-size guard proves no
negative statement. Full formulas are deterministically rebuilt, not stored.

The written proof and CNF/isometry implementation remain unformalized trust
boundaries. Author auditing is not an independent peer-review verdict.
