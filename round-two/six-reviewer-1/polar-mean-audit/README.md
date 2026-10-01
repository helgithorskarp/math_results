# Independent arbitrary-multiplicity polar mean audit

Author **six-reviewer-1**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms lemma8533 and proves mean coefficient47/100,
a stronger closed mean/phase budget, and sharpness of the abstract low-mean
defect8/9. The unrestricted first-power Tang--Zhang endpoint remains open.

Python3.10+ standard library only. From this directory:

```sh
python3 -B audit.py --check expected.json
python3 -O -B audit.py --check expected.json
sha256sum -c SHA256SUMS
```

The independent checker uses closed antiderivative evaluation and exact
Newton interpolation with written degree bounds; full quotient multiplication;
literal Bernstein-basis elimination and complete reconstruction; two
independent interval restriction algorithms; exact Gaussian physical and
disk-polynomial controls; and a full eighth-root product in Q[w]/(w^4+1).
All32 original and32 improved sign coefficients are regenerated. No author
executable, solver, CAS, float, network or external fixture is needed.

The continuous product extremum and analytic bridges are the written proof,
rather than a conclusion from finite sampling. Zero abstract inputs are
included. Polynomial communication controls avoid numerical critical roots.
The sharpness family is abstract; no disk-polynomial realization is claimed.

For an optional comparison with the pinned original fixture:

```sh
git clone --no-checkout https://github.com/helgithorskarp/math_results /tmp/polar-mean-source
git -C /tmp/polar-mean-source checkout 935ec2f52affd0968be4649b89abbd42f691e633 -- round-two/six-sendov-1/general-polar-mean
python3 -B audit.py --check expected.json --author-expected /tmp/polar-mean-source/round-two/six-sendov-1/general-polar-mean/expected.json
```

This reads the original fixture only after independent reconstruction and
compares both full Bernstein lists and all five power hashes. Separate
normal/-O author replay matched its complete output including seven rejected
corruptions. Timings, hashes, primary sources and trust boundaries are in
[PROVENANCE.json](PROVENANCE.json). The largest check used about21MiB and
all runs completed in less than one second. There is no proof-assistant
verification, optimal mean-coefficient claim or historical-priority claim.
