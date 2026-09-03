# Irregularity obstructions to a depth-three Euler preperiod drop

## Result

Let \(A_n\) be the Euler up/down numbers,

\[
\sum_{n\geq 0} A_n\frac{x^n}{n!}=\sec x+\tan x,
\]

and let \(s(p^r)\) be the preperiod of \((A_n\bmod p^r)_{n\geq0}\),
where \(p\) is an odd prime.  Güleç conjectured that

\[
s(p^r)\geq r-2 \qquad (r\geq2).
\]

Call \(p\) *E-regular* if it divides none of the signed classical Euler
numbers \(\mathcal E_2,\mathcal E_4,\ldots,\mathcal E_{p-3}\), where
\(\operatorname{sech}x=\sum \mathcal E_nx^n/n!\).  Call it *B-regular* if
it divides none of the numerators of
\(B_2,B_4,\ldots,B_{p-3}\).

**Theorem.**

1. Güleç's bound holds for every E-regular odd prime \(p\) and every
   \(r\geq2\).
2. If \(r\) is even, the bound also holds for every B-regular odd prime.
   Consequently a counterexample with even \(r\) would require a prime that
   is both E-irregular and B-irregular.
3. If a counterexample has odd \(r\), then either \(p\) has two E-irregular
   pairs \((p,\ell)\) and \((p,\ell+2)\), with
   \(2\leq\ell\leq p-5\), or \(p\equiv1\pmod4\) and
   \((p,p-3)\) is E-irregular.

Thus every possible counterexample is confined to a much smaller
irregular-prime locus; the restrictions depend on the parity of the exponent.

## Proof

We use two consequences of the frequency expansion in Güleç's paper.  In
\(\mathbb F_p[i]=\mathbb F_p[X]/(X^2+1)\), Proposition 4.4 at \(r=1\)
gives, for \(n\geq1\),

\[
A_n=2\eta^{-1}i^n\sum_{a=1}^{p-1}a^n i^{-a},
\tag{1}
\]

where \(\eta=1-i\) for \(p\equiv1\pmod4\), and
\(\eta=-1-i\) for \(p\equiv3\pmod4\).  The scalar in front of the sum is
a unit.  Fermat's theorem in (1) gives

\[
A_{n+p-1}=i^{p-1}A_n\pmod p \qquad(n\geq1).
\tag{2}
\]

In particular, vanishing modulo \(p\) is periodic with period \(p-1\).
Taking \(n=p-1\) and summing the geometric progression in (1) also gives

\[
A_{p-1}\equiv
\begin{cases}
0&\pmod p,&p\equiv1\pmod4,\\
-2&\pmod p,&p\equiv3\pmod4.
\end{cases}
\tag{3}
\]

Güleç's Lemmas 7.1 and 7.2 give the exact criterion

\[
s(p^r)\leq r-k
\quad\Longleftrightarrow\quad
p^j\mid A_{r-j}\quad(1\leq j\leq k).
\tag{4}
\]

Hence a failure of \(s(p^r)\geq r-2\) forces

\[
p\mid A_{r-3},A_{r-2},A_{r-1}.
\tag{5}
\]

Here it is enough to consider \(r\geq4\): the cases \(r=2\) and \(r=3\)
are immediate from \(s(p^r)\geq1\), also proved in the cited paper.

We first show that any run (5) forces E-irregularity.  Among three
consecutive indices there is an even index \(m\) with \(A_m\equiv0\pmod p\).
Reduce even indices modulo \(p-1\) using (2).  A nonzero even residue
\(\ell\in\{2,4,\ldots,p-3\}\) gives
\(p\mid A_\ell=(-1)^{\ell/2}\mathcal E_\ell\), hence the E-irregular pair
\((p,\ell)\).  The only remaining residue is zero.  By (3) it can vanish
only when \(p\equiv1\pmod4\); then (2) identifies the following terms with
\(A_1=1\) and \(A_2=1\).  A three-term zero run containing a residue-zero
even term is therefore impossible unless its other even term already has a
nonzero E-irregular residue.  This proves assertion 1.

More precisely, suppose first that \(r\) is odd.  Then (5) has parity pattern
even--odd--even.  Put \(\ell\equiv r-3\pmod{p-1}\),
\(0\leq\ell\leq p-3\).  The case \(\ell=0\) is impossible by (2)--(3) and
\(A_2=1\).  If \(2\leq\ell\leq p-5\), the two even terms in (5) give the
two E-irregular pairs \((p,\ell)\) and \((p,\ell+2)\).  If
\(\ell=p-3\), the first is the E-irregular pair \((p,p-3)\), while the
second has residue zero and (3) forces \(p\equiv1\pmod4\).  This proves
assertion 3.

Now let \(r\) be even and put \(k=r-2\).  The parity pattern in (5) is

\[
A_{k-1},\quad A_k,\quad A_{k+1}
\qquad\text{(tangent--secant--tangent)}.
\]

Let \(\ell\equiv k\pmod{p-1}\), \(0\leq\ell\leq p-3\).  As above,
\(\ell=0\) is impossible: (3) either makes the middle term nonzero, or
(2) makes the following term congruent to \(A_1=1\).  Therefore
\(2\leq\ell\leq p-3\), and the middle term supplies the E-irregular pair
\((p,\ell)\).

For an even integer \(j\), the tangent-number formula is

\[
A_{j-1}=(-1)^{j/2-1}
\frac{2^j(2^j-1)B_j}{j}.
\tag{6}
\]

If \(p\) is B-regular and \(2\leq\ell\leq p-5\), equations (2) and (6)
show that vanishing of the two tangent terms forces both
\(2^\ell\equiv1\pmod p\) and \(2^{\ell+2}\equiv1\pmod p\).  Their quotient
would give \(4\equiv1\pmod p\), impossible here.  If \(\ell=p-3\), the
first tangent term alone, together with B-regularity, gives
\(2^{p-3}\equiv1\pmod p\); Fermat's theorem again gives
\(4\equiv1\pmod p\), impossible for \(p\geq5\).  (For \(p=3\), the
claimed initial ranges are empty and the assertion follows directly from
\(A_1=A_2=1\).)  Thus an even-exponent counterexample forces B-irregularity
as well as E-irregularity, proving assertion 2.

## A tempting stronger statement is false

It is not enough to assert that an odd-index up/down number and the following
even-index number are coprime.  The Wieferich prime \(1093\) gives

\[
A_{1091}\equiv A_{1092}\equiv0\pmod{1093},
\qquad A_{1093}\equiv1\pmod{1093}.
\]

The last congruence is exactly what prevents a three-term run.  The script
`verify.py` reproduces this example and audits the zero-period and
irregularity implications for a user-selected finite range.  The computation
is a check, not part of the proof.

## Reproduction

```bash
python3 verify.py --bound 200
python3 verify.py --bound 3 --wieferich-demo
```

The second command prints the residues at indices 1091--1093 without auditing
all intervening primes.

## Sources

- Berke Güleç, *Modular periodicity of the Euler up/down numbers at odd
  prime powers*, arXiv:2608.27058 (especially Proposition 4.4, Lemmas 7.1--7.2,
  and Conjecture 7.6): <https://arxiv.org/abs/2608.27058>
- NIST DLMF, tangent-number formula (24.15.4):
  <https://dlmf.nist.gov/24.15.E4>

## Status and trust boundary

The theorem above is proved.  Güleç's full lower-bound conjecture remains
open.  The only imported research statements are the frequency expansion and
preperiod criterion explicitly identified above.  The finite computation is
independent evidence only and is not used to bridge any proof step.
