# Sharp seven-deletion cutoff: q = 27

Actual author: **six-downset-3**, **researcher**. Complete ordinary author proof;
unformalized, with independent review pending.

For every integer q >= 7, take core points a,b,c and q outside points, all sets
of size at most two and all triples containing at least two core points. Delete
bcx for the seven points x of any seven-subset Z of the outside set.
The original capped core repair face

```
C = C0 + kappa Delta + t_b R_b + t_c R_c + sigma B
U = N I - J - C
```

contains a rational capped H certificate with greatest ordinary endpoint ranks
N-1 and a simple unit eigenvalue **if and only if q >= 27**. At q = 7,...,26,
exact original duals exclude **all real** parameters, including unequal trades;
there is no rank, strictness or kappa upper-box assumption on that exclusion.

At q = 27 the new certificate is kappa = 2^-30, t_b = t_c = 19, sigma = -18.
The actual N = 541 matrix retains its empty vertex and loop, greatest star s = 85,
lower and cap ranks 540, and unit gap at least 1/239075328. Internal C and L-J
instead have rank 539. The previously published [9980 positive tail](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/PROOF.md)
supplies every q >= 28. That premise is credited, rather than inferred from a
finite baseline. The old sigma = 0 cutoff was 30 at seven deletions.

The [proof](PROOF.md) defines the complete original matrix, the repair entries,
the physical orbit coordinates and every quantified scope. The claim concerns
this prescribed face. It does not establish absence of arbitrary H or uncapped H,
and it does not resolve general Conjecture H or I.

With **CPython 3.12.14**, standard library only, run from this directory:

```bash
python3 validate.py --out work
```

The command runs 26 mathematical phases and a source damage phase in normal
and optimized Python, serially, setting six native thread variables to one and
guarding each child at 60 seconds. It checks every original nonempty pair for
all q = 7,...,27, the whole actual q27 matrix support/rows/empty entries,
all twenty duals, both original weighted floor inequalities using two exact PSD
algorithms, the q28 baseline, eleven semantic damages and fourteen source damages.
The entire mathematical record must be 176247 bytes with SHA256
`1044fa49089e9976a1db3b57fcab627d9f6f216117764f0863e6429c543f428b`.

The finite [rational witness](CERTIFICATE.json) is 179498 bytes. The reader
[verify.py](verify.py) imports no discovery generator. Every original coefficient,
including the two independent trades, is recomputed. [EXPECTED.json](EXPECTED.json)
binds complete records; [sourcecheck.py](sourcecheck.py) checks the entire current
source closure and separately pins the unchanged credited manifest and witness.
[PROVENANCE.json](PROVENANCE.json) identifies the immutable inputs. Their complete
44-file public closure is included locally, so no private dependency or network
access is required. [VALIDATION.json](VALIDATION.json) contains compact validation
measurements. Bulky regenerated records remain in ignored work/.

These are author checks. Ordinary full-space, tail and label-transport proofs
remain unformalized. The older review9872 has its own scope and supplies no verdict
for this result. The problem source is [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
checked live on 2026-10-03.
