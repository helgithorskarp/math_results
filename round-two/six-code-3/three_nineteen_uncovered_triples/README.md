# Three nineteen-centers around an uncovered triple: sharp maximum63

Actual author **six-code-3, researcher**, fresh round two, 2026-10-01.

**Result.** A weight-five distance-six code on eighteen points has at
most63 words if three points each occur nineteen times, their three
pairs each occur five times, and their triple is uncovered. The
[explicit63-word witness](witness63.json) proves this restricted maximum
is sharp. The [proof](PROOF.md) combines the prior m=2 bound with the
complete remaining m=1 branch:40 marked types and1501 labelled cores,
each with an independently checked residual capacity at most21.

For a71-word code with replication profile `(19^5,20^13)`, this implies
that every uncovered triple contains a pair of replication at most four.
This is a new necessary condition, and does not exclude the profile.
The campaign's global interval remains69--71; neither a70-word
construction nor a global upper70 is claimed. Independent mathematical
review of this new theorem remains pending; the written completeness
bridges are unformalized.

Run from a repository checkout with the two preceding six-code-3
directories present, using Python3.11+ and a C++17 compiler:

```sh
python3 -B round-two/six-code-3/three_nineteen_uncovered_triples/reproduce.py --work /tmp/cwc-three-nineteen-all
```

The default performs a fresh complete primary enumeration, all forty
independent literal/native case replays, exact residual checks in normal
and optimized Python, exhaustive tiny-graph and corruption controls,
and a sanitized native replay of an actual case. It uses one CPU-intensive
job at a time and one numerical-library thread. The private working
carrier is regenerated, not published. Guard expiry raises an incomplete
check instead of supplying a negative mathematical result.

[expected.json](expected.json) supplies full case hashes and exact output.
[VALIDATION.json](VALIDATION.json) records actual commands and coverage.
[residual.json](residual.json) stores the compact color/branch certificates;
[verify_residual.py](verify_residual.py) needs no optimizer. The optional
deterministic [certificate generator](residual.py) can be rerun with
`--work WORK --output OUTPUT`; supplied certificates do not need to be
regenerated for verification.

[DEPENDENCIES.json](DEPENDENCIES.json) pins imported mathematical results,
the classification manifest and the separate reused source helpers.
The original nineteen-star census has an
[independent audit](../../six-reviewer-2/nineteen-star-audit/REVIEW.md).
The [subsequent three-star audit](../../six-reviewer-2/three-star-audit/REVIEW.md)
also confirms the m=2 premise and strengthens its bound to61. Neither
audit reviews this new m=1 transfer. Historical priority of this
specific restricted maximum is unassessed.

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked2026-10-01, still lists69--72 externally. The known69-word
baseline comes from [Aw, Chee and Ling (2003), Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
[baseline69.txt](baseline69.txt) is the unchanged
[public witness](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69), reproduced
here at size69 and distance6. Its degree census is `12^1,18^2,19^3,20^12`.
Baseline reproduction is validation, rather than a new construction.
