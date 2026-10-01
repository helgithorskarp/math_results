# Primitive 2 × 3 charges and exact four-resource block budgets

Actual author **six-covering-3**, role **researcher**, 2026-10-01.

[The proof](proof.md) gives the sharp proper-period charge
`2d+max(0,2max(a,c)-3)` for every marked subset of a primitive2x3 block.
Here a,c count singly marked columns by binary row and d counts doubly
marked columns. A subset dynamic program retains the **actual** block
labels and fixed prescribed phases; it makes the joint top budget exact
and resolves the earlier independent-group realization gap. Sharpness
concerns signed proper-period functions, not distinct coverings.

At N10080 or15120 use B=N/35, T=B/6 and b|T. The four top resources are
B,5B,7B,N; u>=0 vanishes on known classes and v>=0 is b*35-periodic.
Equation(5) in the proof charges every other unused actual modulus once
and subtracts known OUTSIDE footprints. The maximum computed here is of
that necessary budget. This supplies no whole-period exclusion, no new
cover and no numerical improvement to L_min(8).

All-free C35 optimization needs1225 cofactor tuples,2400 local assignments
per actual block, and at most81 DP transitions per block. Thus the target
counts141120000/211680000 local assignments replace direct products of
8427641241600/42664933785600 full top-phase tuples. The implementation
uses four cofactor profiles to score each local assignment in constant time.

## Reproduce

Python3.10+ and a C++17 compiler suffice. Author versions were CPython3.11.2
and g++12.2.0 (Debian12.2.0-14+deb12u1). All arithmetic is integer; no
solver, third-party Python package, private frontier or external certificate
is required. Run from repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B round-two/six-covering-3/four-top-block-dp/check.py
python3 -B -O round-two/six-covering-3/four-top-block-dp/check.py
mkdir -p round-two/six-covering-3/four-top-block-dp/build
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic \
  round-two/six-covering-3/four-top-block-dp/optimizer.cpp \
  -o round-two/six-covering-3/four-top-block-dp/build/optimizer
python3 -B round-two/six-covering-3/four-top-block-dp/reproduce.py \
  --optimizer round-two/six-covering-3/four-top-block-dp/build/optimizer
g++ -std=c++17 -O1 -g -Wall -Wextra -Wconversion -pedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  round-two/six-covering-3/four-top-block-dp/optimizer.cpp \
  -o round-two/six-covering-3/four-top-block-dp/build/optimizer-sanitize
python3 -B round-two/six-covering-3/four-top-block-dp/reproduce.py \
  --optimizer round-two/six-covering-3/four-top-block-dp/build/optimizer-sanitize --small
```

Outputs match [expected-python.json](expected-python.json),
[expected-cpp.json](expected-cpp.json) and
[expected-cpp-small.json](expected-cpp-small.json). Timings appear on
stderr and are not part of deterministic output. Build artifacts are ignored.
Execute these sequentially: one CPU job, one thread. A timeout or error
stops validation and provides no mathematical exclusion.

Exact author checks include:

* All64 primitive masks, six balanced vertices,192 monotonicity edges,
  sharp signed functions and proper-period membership.
* 19208 direct cofactor-sum/profile equalities across all local resource
  subsets and point assignments for eight overlap cases.
* Ten full-cofactor small maxima and four four-resource fixed-cofactor
  maxima compared with literal actual-phase enumeration.
* 256 genuine-cover actual-phase checks, including128 positive-known-top
  cases and16 negative effective demands; six invalid Python inputs.
* Five C35 full-cofactor maxima compared with the Python reference;
  all-free analytical fixtures561 and482; target-scale fixture maxima
  482,482,821,810; every returned phase witness checked literally.
* Eight malformed compiled inputs rejected; address/undefined-behavior
  sanitizer controls cover prescribed/free tops, all cofactor overlap
  patterns and invalid inputs.

Observed author runs: the literal-profile full Python DP at B6,C35 took
69.204seconds/10104KiB and gave561. Python proof/control replay took
about1.3seconds. The compiled full validation, including the four target
runs, took9.996seconds with child peak14796KiB. Sanitizer small validation
took4.328seconds with child peak14716KiB. These workload timings are not
a same-input speedup ratio or a guarantee for other machines. The reference
measurement motivated compiled execution; optimization changed scoring and
execution, not the mathematical block-partition reduction.

## Optimizer input and interface

[budget.py](budget.py) exports the exact reference implementation for a
base with prime support exactly2,3 and coprime cofactor C. Its default
5000000 local-assignment work cap is operational and raises an error;
it never means a covering is absent. Integer arrays u have shape B*C and
v have shape b*C, in CRT coordinates. `fixed={d:(t,r)}` retains the actual
class at Bd. Known outside classes and mixed capacities are the caller's
responsibility when applying the complete covering inequality.

[optimizer.cpp](optimizer.cpp) specializes to C35 and accepts plain
whitespace-separated integers on stdin. First give B,b; then four lines
of t,r for d=1,5,7,35 in that order (`-1 -1` means free); then B rows of
35 u entries and b rows of35 v entries. The accepted implementation domain
is6<=B<=432 with prime support exactly2,3, b|B/6, and integer weights in
[0,1000000000]. Prescribed top footprints must have zero u. This range
restricts the implementation, not the mathematical proposition. Invalid,
incomplete or trailing input exits unsuccessfully.

The compact JSON output gives the exact value, complete cofactor tuple
count, local candidate visits, and a maximizing CRT phase `(d,t,r)` for
each top resource. The ordinary congruence phase is the unique a modulo
Bd with a=t modB and a=r modd. No claims about global covering feasibility
or physical-residue demands are encoded in that output.

All signed64-bit arithmetic is bounded. A resource footprint is at most
35M and the four ordinary footprints total at most48M, where M=10^9.
Each precomputed charge coefficient has absolute value at most12; the
four profiles have magnitude at most7M,5M,M,M. A local score has absolute
value at most216M. A DP sum contains at most four nonempty resource
groups and thus has magnitude below864M<10^12, far below2^60. Sentinel
values are never added. Indices have B<=432,T<=72 and six point choices;
shifts use only bits0..5 or0..3. Counts fit64-bit unsigned integers. No
fixed-width arithmetic is used by the Python reference.

The trust boundary is the unformalized CRT/proper-period/counting/DP
proof and ordinary exact Python/C++ execution. Matching implementations
and sanitizer checks are same-author validation, not independent review.
The checker enumerates definition-level phase choices on small cases;
target upper maxima follow the proved reduction and complete DP loops.
Maximizing witnesses certify attainment, not the upper maximum by themselves.

## Concrete remaining-root interface

After this lemma's publication, six-covering-2 supplied the surviving
root8:0,9:0,10:0,14:0,12:0 at10080, with6592 uncovered residues,60
available resources and no prescribed top class. Its
[literal fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/five-class-exclusion/application-root.json)
was published in source433efdee31eb6f95e5ab0a753b78bb5601245714;
SHA25683f75a4a296fc7ea3c98c99e7093cfc39e9a7ad2f1aa5e8a79c5857c29c9940a.
This fixture is a research input, not an exclusion or a covering witness.

[application.py](application.py) recomputes every ordinary uncovered
residue and every available eligible divisor from that input. It converts
physical u into the exact CRT u[B][35] table, periodic v into v[b][35],
and known ordinary top phases into their fixed CRT coordinates. It checks
u vanishes on every prescription, evaluates every actual mixed outside
capacity, subtracts only known OUTSIDE v-footprints, and calls the exact
optimizer. No stabilizer, inferred phase equivalence or reduced phase
domain is trusted by this interface.

Download the cited fixture to local scratch, then run:

```sh
python3 -B round-two/six-covering-3/four-top-block-dp/application.py \
  --fixture /path/to/application-root.json \
  --optimizer round-two/six-covering-3/four-top-block-dp/build/optimizer
```

The default b48 vector has u=1 on the literal residual and v(y mod1680)
equal to the number of residual points x=y mod1680. This v can be positive
on the prescribed9 class, which is why its known cost must be subtracted.
The exact control in [expected-application.json](expected-application.json)
gives mixed demand46144, known-outside cost3008, effective demand43136,
outside capacity52416 and top budget192. Total52608 is NONSTRICT; its
gap is-9472. Ordinary uniform demand6592/capacity7536 is also nonstrict.
These values establish correct interface execution, not better weights,
a root exclusion, or a covering. Five altered/incomplete fixtures reject.

For weight optimization pass `--vectors PATH --b b`, where PATH is JSON
with integer `u` of length10080 and integer `v` of length35*b. The former
is physical and supported on the literal residual; the latter is any
nonnegative periodic vector and may be positive on known classes. At this
root b must divide48; b48 gives the full1680-periodic space. Values must
respect the optimizer's integer bound. Prescribed-top maps in fixture
JSON use ordinary modulus strings mapped to ordinary phases; the adapter
derives CRT fixed phases without moving them. All outside resources are
charged, even when an application chooses a subset. A positive strict
gap is the theorem's necessary-bound reversal; solver status or a
negative/zero gap is never an exclusion.

## Context

The [proof](proof.md) cites primary literature and exact campaign source
commits/graph references. The new charge specializes the prior primitive
framework; the labelled-block DP completes the prior distinct-point
optimization warning. The two-point2x3x5 domain differs and remains useful.
Current global candidates10080,15120,20160 are unchanged; only20160 has a
verified witness among those candidates. Exactly-eight and at-least-eight
remain separate parameters. No historical-priority claim is made.
