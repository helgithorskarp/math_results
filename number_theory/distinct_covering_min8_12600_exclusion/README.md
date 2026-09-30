# Period 12600 exclusion and five candidates for L_min(8)

**Author: six-covering-2, researcher.** No finite distinct covering with all
moduli at least eight can have every modulus dividing 12600. This is a
complete exact certificate, covering all subsets of eligible divisors and
all congruence phases.

Together with the previously established finite sieve and the period-20160
construction, this removes 12600 and gives

\[
L_{\min}(8)\in\{10080,15120,15840,18480,20160\}.
\]

Here the principal parameter requires minimum **exactly eight**. The optimum
and feasibility of the four smaller retained values remain unresolved. The
numerical interval is still \(10080\le L_{\min}(8)\le20160\).

[proof.md](proof.md) gives the full counting and symmetry argument,
attribution, evidence and trust boundary. The standalone 12600 exclusion
uses no earlier exclusion theorem. The five-candidate consequence uses
separately cited campaign results.

From the repository root, Python 3.10+ and the standard library suffice:

```sh
python3 -B number_theory/distinct_covering_min8_12600_exclusion/check.py
python3 -B number_theory/distinct_covering_min8_12600_exclusion/audit.py
python3 -B number_theory/distinct_covering_min8_12600_exclusion/controls.py
```

Both full replays validate all 1159 nodes: 202 expansions, 430 uniform cuts,
527 weighted cuts, zero open leaves. Of the weighted cuts, 112 group pairs
of remaining resources. The two implementations agree on every recorded
cut and all 457720 ordered pair-capacity entries. They use different branch
symmetry tests, weight decoding and joint-capacity arithmetic. Both are
checks by the author; no external review of this new exclusion is claimed.

`certificate.json` is 582605 bytes: 527 literal integer vectors, 23628
disjoint CRT boxes and the complete small branching tree. It is required
proof evidence, not a solver trace or an omitted private search corpus.
Certificate SHA-256:
`332bccfc80087837a8f9b370d4b45c7e8726eb63f75a3b523b7135760e7cf8e0`.
The expected manifests authenticate reproduction; each inequality and
branch is independently checked before comparison. No solver, floating
point, network fetch, private database or generated orbit declaration is
needed to replay the proof.
