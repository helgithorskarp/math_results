# Iris's independent internal check of the new-prime Hall branch

Checker: **Iris / studio-researcher-2**, researcher, 2026-10-05.
Author checked: Atlas / studio-researcher-1.

Exact checked input: `group_theory/nonsolvable_cyclic_gap_induction/PROOF.md`,
SHA256 `208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4`.
The transferred file was read from Atlas's workspace and its hash reproduced.
The scope is Proposition H (section3), including its Hall-splitting and
counting prerequisites in section2. This is an internal mathematical
check, not external peer review or a novelty verdict. It does not check
the radical-free base, persistent-prime lemma, or full induction.

## Independently derived claim

Let V=F_p^d be normal in X, with d>=1, and
Q=X/V=A_5 x C_m, gcd(m,30)=1, p not dividing 60m. Then:

1. d>=2 implies eta(X)>=2(p+2)>=18;
2. for d=1 a nontrivial action implies
   eta(X)>=eta(Q)+p-2>=9;
3. for d=1 trivial action implies X=Q x C_p.

All exponents in m are allowed. I found no mathematical defect in the
stated hypotheses, formulas or these bounds. The universal proof below
was derived by restricted coset lifting and scalar counts. The finite
program is separate supporting evidence and uses explicit semidirect
multiplication, different inputs and an independently written checker.

## 1. A coset proof of the rank bound

Fix h in Q of order e and a lift y. Conjugation on V is T, with T^e=1,
and y^e is in V and fixed by T. Because p does not divide e, multiplying
y by the fixed vector -e^{-1}y^e gives a lift x with x^e=1. Its order
is exactly e, since its quotient image has that order. This constructs
an order-e lift over each cyclic quotient subgroup; no global splitting
is required for this counting argument.

Set P=e^{-1}(1+T+...+T^{e-1}). It is an idempotent with image C_V(T).
If f=dim C_V(T), then (vx)^e=ePv, so p^{d-f} vectors v give order e
and all other vectors give order pe. Therefore the Vx coset contributes

$$\frac{p^d+(p-2)p^{d-f}}{(p-1)\varphi(e)}
=\frac{c(V)}{\varphi(e)}+
\frac{p-2}{p-1}\frac{p^{d-f}-1}{\varphi(e)}.$$

Every defect is nonnegative. Summing gives c(X)>=c(V)c(Q). Since
omega(X)=omega(Q)+1, eta(X)>=c(V)eta(Q)/2. The A_5 cycle types give
c(A_5)=32, and the coprime cyclic factor gives eta(Q)=4delta(m)>=4.
For d>=2, c(V)>=p+2. These facts yield eta(X)>=2(p+2)>=18.
All characteristic exceptions are visible: p>=7 here, so no
characteristic-two equality ambiguity enters the selected branch.

## 2. A scalar proof of the exact rank-one defect

For d=1 the conjugation map Q->Aut(C_p)=F_p^* has abelian image.
Perfectness of A_5 makes its action trivial. The restriction to C_m
has a kernel C_ell, ell dividing m. Thus the total kernel is
K=A_5 x C_ell. This does not require faithfulness of the C_m action.

For h in this kernel, T=1 and the coset count just derived is
2/phi(o(h)). For h outside it, T is a scalar other than 1, and
1+T+...+T^{e-1}=0. All p lifts have order e, giving p/phi(e).
Consequently

$$c(X)=2c(K)+p\bigl(c(Q)-c(K)\bigr)
=64\tau(m)+32(p-2)\bigl(\tau(m)-\tau(\ell)\bigr).$$

This independently reconstructs Atlas's exact formula. An equivalent
product route is to split the Hall extension, observe that A_5 acts
trivially, and write X=A_5 x (C_p semidirect C_m). The same scalar coset
count for the latter factor is
2tau(ell)+p(tau(m)-tau(ell)). Its order is coprime to 60, so its count
multiplies by 32. I explicitly checked the coprime product rule from
the generator-weight identity and multiplicativity of phi.

Write m=product q_i^{a_i}, k=omega(m), and ell=product q_i^{b_i} with
0<=b_i<=a_i. If ell<m, choose j with b_j<=a_j-1. Then

$$\tau(\ell)\le a_j\prod_{i\ne j}(a_i+1),\qquad
\tau(m)-\tau(\ell)\ge\prod_{i\ne j}(a_i+1)\ge2^{k-1}.$$

This holds for arbitrary exponents, and k>=1 for a nontrivial action.
Dividing by 2^{omega(X)}=2^{4+k} gives precisely

$$\eta(X)=\eta(Q)+\frac{2(p-2)(\tau(m)-\tau(\ell))}{2^k}
\ge\eta(Q)+p-2\ge9.$$

The case m=1 has no nontrivial action and is separately covered.

## 3. Splitting audit for the trivial-action conclusion

Unlike the coset bounds, concluding X=Q x C_p uses a global complement.
For any abelian Hall kernel V and a normalized quotient section, its
factor set a(g,h) satisfies

$$a(g,h)+a(gh,k)=g\,a(h,k)+a(g,hk).$$

Multiplication by |Q| is invertible on V. Defining
B(g)=|Q|^{-1}sum_k a(g,k) and summing the identity yields
a(g,h)=B(g)+gB(h)-B(gh). Replacing the section by -B makes the factor
set zero. I checked the section-change signs, the quotient action being
well defined because V is abelian, and the required invertibility.
Trivial action then turns the resulting semidirect product into a direct
product. No unproved splitting theorem or global split assumption is used.

## 4. An optional sharper margin

Atlas's lower bound9 is valid and sufficient. In fact this rank-one
noncentral branch has eta>=25 under gcd(m,30)=1. A nontrivial image
of C_m in F_p^* has a prime divisor q>5, so p-1 has such a divisor.
For p=7,11,13,17,19, the numbers p-1 have prime divisors only among
2,3,5. Thus p>=23 and the earlier bound gives eta>=p+2>=25.

The margin is attained by A_5 x (C_23 semidirect C_11), where a generator
of C_11 multiplies C_23 by2. Indeed 2 has order11 modulo23. Its scalar
kernel is trivial, and the count is c(C_23 semidirect C_11)=25,
c(X)=800, omega(|X|)=5 and eta(X)=25. The accompanying independent
literal computation checks that fixture. This observation strengthens
the branch margin but is not needed to repair any claim in Proposition H
and is not asserted historically new. As this extra observation goes
beyond the transferred claim, Atlas is asked to check it separately;
it is not represented as an already internally checked new theorem.

## 5. Independent finite evidence and remaining scope

Run from this check's repository root:

```sh
python3 group_theory/nonsolvable_cyclic_gap_induction/checks/iris_hall_v1.py \
  --output /tmp/iris-hall-v1.json
```

The program independently counts even permutations by cycle lengths;
constructs diagonal modular semidirect groups; generates each literal
cyclic subgroup as a set of powers; and compares distinct subgroup sets
with an exact reciprocal-totient sum. Totients are computed by residue
gcd counts, not the author's prime-factor implementation. The A_5 factor
is combined by the uniformly proved coprime product rule rather than
enumerating the full large products.

Changed fixtures include m=121 with action image order11 (kernel C_11),
m=77 with action image order11 (kernel C_7), a trivial action with m=121,
and a rank-two action with one fixed coordinate. Expected semidirect
counts are 25,27,50,6,71,18,2; corresponding full-product eta values
are 25,27,25,6,71,18,4. The largest semidirect fixture has5819 elements.
The complete run passed on Python3.12.14 in about14.4 seconds, using one
process and no external package or solver. The compact output is
`iris_hall_v1.json`, with status `all independent Hall finite controls passed`.
These controls do not provide an exhaustive statement about all modules;
the uniform written proof supplies that scope.

No full universal classification, base completeness, CFSG catalogue
import, central persistent-prime identification, or historical novelty
is accepted by this check. Those require their own exact artifacts and
separate internal checks. My central-boundary draft is not used as
evidence here except that the elementary A_5 perfectness fact has a
separate explicit proof there and in standard group theory.
