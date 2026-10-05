# Four-mark triangle cap: independent audit

**six-reviewer-1 / independent mathematical reviewer.** Committed target
LEMMA10316/0 is confirmed at its full stated mathematical scope by an
ordinary unformalized proof audit. [REVIEW.md](REVIEW.md) gives the verdict;
[PROOF.md](PROOF.md) gives the complete universal argument.

Every integer \(n\ge4,h>l\ge2\), four distinct old cube marks, mutually
disjoint outside private triangle pairs, counts \((h,l,l,l)\), and the
actual empty row/loop are retained. The rational invariant supported
stochastic matrix has both greatest endpoint ranks \(N-1\).
The exact lower PSD interval and endpoint ranks are confirmed.
A proved refinement extends the sufficient real repair range to
\(0<\delta\le3/20\), with floor \(11/320\); the rational repair
\(\delta=1/32\) has floor \(409/512\). General H/I, entry nonnegativity
and an optimal upper interval are not claimed.

Use **CPython 3.12.14**, standard library only, on POSIX. No install,
CAS, solver, author executable or large data corpus is needed:

~~~sh
cd round-two/six-reviewer-1/four-mark-audit
python3 -B verify.py --output /tmp/four-mark-normal-fresh.json
python3 -O -B verify.py --output /tmp/four-mark-optimized-fresh.json
cmp /tmp/four-mark-normal-fresh.json /tmp/four-mark-optimized-fresh.json
~~~

Each output path must be fresh. The source seal is checked before
mathematical imports; six native thread settings are set to one and
each mathematical process has a fixed 45-second alarm.
Run processes serially within 1 CPU/2 GiB, with the fixed 4 MiB
coefficient-encoding guard and original-control \(N\le80\) guard.
The checker directly regenerates the original controls \(N=70,76\),
all 25 five-block forms/30 ordered Schur identities/265 pivot
coefficients, 24 full prototype polynomial positions, all original
sectors/cross terms, actual empty rows, inverses, repaired ranks,
cap floors, symmetry generators and outside-line negative witnesses.
The universal parameter, physical and real bridges are in PROOF.md.

Expected whole record: **183039 bytes**, SHA256
**903f734235fc53fbfd4ac6b5a2247f5e9c29ffc145693e00f56ee5e4a417e204**.
The complete local/cold normal/optimized records agreed before hashing.
[EXPECTED.json](EXPECTED.json) is a compact consistency description;
hash equality alone is not proof. Full generated records stay local.

To reproduce the 14 designated semantic rejection cases in both modes:

~~~sh
for mode in normal optimized; do
  for fixture in denominator-zero duplicate-exponent domain-wrong ordered-coverage pivot-link old-row-drop Schur-sign empty-row light-mean-omitted light-dual star-census deleted-inverse-row outside-empty-lift prototype-count; do
    if [ "$mode" = normal ]; then
      python3 -B verify.py --fixture "$fixture"
    else
      python3 -O -B verify.py --fixture "$fixture"
    fi
  done
done
~~~

Expected: each reports its exact designated rejection gate, with exit 0.
A crash, timeout, memory limit or different gate is not successful rejection.
[VALIDATION.json](VALIDATION.json) records the four complete positive
replays, all 28 designated rejections and four pre-import source faults.
The corrected omitted-light-mean test now expects the stronger metric
gate which precedes the frame gate. Positive mathematics was unchanged.
The earlier reviewer variable shadow and the stale rejection label
were checker implementation defects, not target counterexamples.

The exposed author coefficient DATA and reused own algorithm scaffolding
are explicitly attributed in [PROVENANCE.json](PROVENANCE.json) and
[DEPENDENCIES.json](DEPENDENCIES.json). Four-mark geometry, counts,
sectors, prototype identities and dual/inverse binding are new independent
checks. The coefficient reader imports no author code. Predecessor
reviews do not supply this four-mark verdict. Interpreter/checker
correctness and the ordinary unformalized bridges remain trust boundaries.
Source seals are consistency controls, not mathematical proofs.

The primary comparison is Ellis, Filmus and Friedgut,
[Section4 of arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
live checked 2026-10-05. Their general H/I conjectures remain outside
this restricted result; no historical priority is asserted.
