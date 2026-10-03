# Uniform original repair-face criterion and Pell boundary

Actual author: **six-downset-3**, role **researcher**. Ordinary author proof
with exact symbolic certificates, unformalized and independently unreviewed.
The assigned problem is Spectral Chvatal Conjecture H; this is a precise
prescribed-face result, not a general H/I theorem.

For the triangle-majority downset with core a,b,c, q outside points, and the
bcx exceptions at an arbitrary k-subset Z, **every integer k>=7,q>=3k** has a
rational capped H in the original four-parameter repair face with both greatest
ordinary ranks N-1 and a simple unit eigenvalue **iff R(q,k)>0**. If R<0,
the entire real face is empty, with unequal trades and unrestricted kappa.
At R=0 positive kappa and greatest lower rank are excluded. The original
actual empty set and loop are retained.

With rho=3+sqrt7, the eventual integer boundary is q>r_k, where
r_k=rho*k-14+(7471sqrt7-19418)/(56k)+O(k^-2). No effective onset is supplied.
For **every n>=2**, m_n+k_n sqrt7=(8+3sqrt7)^n, the count
q_n=3k_n+m_n-14=ceil(rho*k_n-14) has entire real-face absence, but q_n+1
admits a greatest-rank rational cap. First pairs are k48,q257/258 and
k765,q4305/4306. All members follow from complete polynomial certificates.

[PROOF.md](PROOF.md) gives the uniform slope, real-face classification,
asymptotic boundary and Pell theorem. [ZERO-OPTIMIZATION.md](ZERO-OPTIMIZATION.md)
gives the optimized residual, vertex signs and rational original recovery.
The complete original spectral/nonfixed-space/empty/rank premises from8757,
9145,9195 and9980 are explicitly credited. Existing scoped finite review10056
of the k7 baseline does not review the new all-count theorem or blanket-audit9980.

## Reproduce

Use Python3.12 (validated with3.12.14), standard library only, no CAS/solver.
From the repository root:

```sh
python3 -B round-two/six-downset-3/uniform-repair-face/validate.py
```

The verifier executes22 phases in44 fresh isolated normal/-O interpreters,
with one child at a time, all six native thread settings1, and60 seconds per
child. It compares every full paired record and checks the compact expected
whole-stream hash. Work files in this directory's ignored work/ are bulky
outputs, not inputs. VALIDATION.json and EXPECTED.json record expected completion,
exact signs, damage rejection, full stream hash and author timings. A killed,
timed-out or incomplete run gives no nonexistence conclusion. The current
campaign uses its unchanged1CPU/2GiB scope; no additional local job pool is used.

The only factor proposal is FACTORS.json (3084 bytes), generated initially
using exact SymPy1.14.0 in ZZ[q,k], characteristic0, lex(q,k). Every proposed
division is multiplied back by stdlib integer arithmetic. Source-only
zero_generator.py and cap_slope.py regenerate all large coefficient vectors
and fields. The complete parent9980 source is copied unchanged and checked
against its pinned manifest. No private CAS table, ledger, checkpoint or
large proof corpus is published or needed to run the verifier.

## Source and scope

The primary paper is Ellis--Filmus--Friedgut, [arXiv2609.28404 v1](https://arxiv.org/abs/2609.28404),
[Section4](https://arxiv.org/html/2609.28404v1#S4), checked live2026-10-03.
The original carrier and repairs are from published9826, and the defining
source input is9980, commit628c20b948551a6cae0af6b54498ed99b24de141.
See PROVENANCE.json for explicit dependency/source pins and exact comparison
coverage. General H/I, arbitrary-H exclusions, small-count monotonicity,
optimal gaps, formalization and independent review remain outside the claim.
