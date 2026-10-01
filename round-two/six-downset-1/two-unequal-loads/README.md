# Two arbitrary unequal pendant loads

Actual author: **six-downset-1**, role **researcher**.

For every Boolean cube of dimension \(n\ge2\), attach \(D>t\ge1\)
fresh pendant pairs at two distinct old coordinates. The construction
gives a rational capped Conjecture-H matrix on the full downset,
including the empty loop. It attains the universally greatest lower
rank \(N-1\), upper rank \(N-1\), simple unit and negative endpoint,
and a scaled upper gap of at least \(1/2\).

[PROOF.md](PROOF.md) supplies the unbounded argument, every sector,
boundary cases, exact formulas, literature and credited predecessors.
General H/I remain open. The proof is author-checked, unformalized,
and independently unreviewed.

Run from the repository root with CPython3.11 or later on a POSIX host:

~~~sh
python3 -B round-two/six-downset-1/two-unequal-loads/verify_signs.py --expected round-two/six-downset-1/two-unequal-loads/RESULTS.json
python3 -B round-two/six-downset-1/two-unequal-loads/verify_full.py --expected round-two/six-downset-1/two-unequal-loads/RESULTS.json
~~~

The first command regenerates eight universally positive rational
functions over \(\mathbb Q(Q,T,B)\), after
\(q=Q+2,t=T+1,D=t+B+1\). It checks all coefficients and constants;
complete permutation determinants establish the symmetric Schur cap.
No CAS, network or stored polynomial data is needed.

The second command checks five full original-index fixtures through
\(N=70\), including all2452 changed-frame action entries, untouched
spaces, actual empty energy, rank repair and full scaled gaps. It uses
the credited [definition checker](../verify.py) and
[Gram helpers](../verify_two_marks.py).
These finite fixtures validate the interpretation and implementation;
the first command and the written argument supply unbounded coverage.

Repeat both commands with \(-O\); the committed exact outputs agree
entrywise in normal and optimized modes. Runtime and RSS fields are
excluded from frozen-output comparisons.
[RESULTS.json](RESULTS.json) contains compact coefficient/matrix hashes.
To check source integrity, run from this directory:

~~~sh
sha256sum -c SHA256SUMS
~~~

Only one mathematical job ran at a time, with numerical thread counts1.
Each proof stage retains a60-second guard; a timeout is incomplete work.
The source packet contains no CAS installation, raw coefficient corpus,
private ledger, environment dump or credentials.
