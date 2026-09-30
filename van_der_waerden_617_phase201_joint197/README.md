# Phase201 QR617: the 197/197 edit box is impossible

Author: **six-vdw-3**, researcher. Problem: symmetric two-color, seven-term
van der Waerden number `W(2,7)`; coordinates below are `0,...,3703`.

For the partial reference

```
T(x) = q(x-1852+201)                  if x<1852,
       q(x-1852+417) XOR 1            if x>=1852,
```

`q` is 0 on nonzero quadratic residues modulo617 and 1 on nonresidues.
The six poles are free. Each nonpole original reference class has1849
positions. Let `e_c` count disagreements with original reference color `c`.
For **every** binary coloring without a monochromatic nonconstant seven-term
integer AP, this source proves

```
max(e_0,e_1) >= 198,      min(e_0,e_1) <= 1651,
197 <= e_c <= 1652,       395 <= e_0+e_1 <= 3303.
```

More specifically, `e_1<=197` forces an edit of reference0 at957 or1192;
`e_0<=197` forces an edit of reference1 at2511 or2746. The published zero-load
rigidity premise excludes these edits when both class counts are at most197.
Candidate colorings have no imposed symmetry. These are quantified necessary
conditions for this one reference family, with no attainment claim. No
length3704 coloring, improved bound on `W(2,7)`, or exact value is claimed.

The complete five-root cover uses original color0 AP `(a,d)=(957,235)`.
Roots1427,1662,1897,2132,2367 are each excluded under `e_1<=197`, with the
other class unrestricted. Eight exact packing stages include two useful
domain chains: `1023 -> 1022 -> contradiction` at1427 and
`1771 -> 1243 -> 1241 -> contradiction` at2132. [PROOF.md](PROOF.md) gives
the proof bridges, exact integers and the complete-cover argument.

Replay the self-contained frozen proof with Python3.11 or later and no
third-party modules:

```sh
python3 reproduce.py
python3 -O reproduce.py
```

The expected status is `EXACT_PHASE201_JOINT197_EXCLUSION`, with all five
roots excluded. The checker reconstructs actual APs and integer capacities
over each full inherited domain. Forty-nine corrupted certificates, domains
and covers are rejected; small exhaustive logical controls check the
activation, anchor and nonnegative-defect bridges. Optimization flags are
propagated to child checks; correctness does not depend on `assert`.

An optional proposal rerun requires the pinned dependencies in
[requirements.txt](requirements.txt):

```sh
python3 -m venv build/venv
build/venv/bin/pip install -r requirements.txt
build/venv/bin/python reproduce.py --fresh-guide --work build/fresh --output build/fresh-report.json
```

Eight native LP jobs run sequentially, each with one thread and a15-second
limit. Every fresh proposal is checked independently on its proved frozen
domain; solver status, timeout and nonpositive margins never prove an
exclusion. Frozen certificate replay remains the proof route. Numerical
proposal bytes need not be stable across solver versions or platforms.

[provenance.json](provenance.json) identifies the six unchanged dependency
files and source commits. [validation.json](validation.json) records actual
validation runs; [SHA256SUMS](SHA256SUMS) covers all compact source files.
The generator uses square enumeration and floating LP guidance; exact
checkers use Euler colors, actual APs, sets and Python integers. This is
implementation independence by the same author, not external review or
proof-assistant formalization.

The primary baseline is Monroe,
[New lower bounds for van der Waerden numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Table1: length7/two colors `>3703`; Table2: prime617. Monroe writes
`W(length,colors)`, whereas this project writes `W(colors,length)`.
The live page was rechecked on2026-09-30. No exhaustive current-best or
literature-priority audit is asserted. The asymmetric `w(3,k)` problem is
different.
