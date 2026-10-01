Actual author: six-vdw-1, researcher. All positions below are one-based.

Fix N=3704 and the literal binary word b in `base3704.bits`, with file SHA256
42e6cbef0710d38089475954306b3bd2c0367d5a28aed5ccc74b2698f27fed87.
For r=(t-1) mod617, let b_t=0 on nonzero quadratic residues and b_t=1 on
nonresidues. Poles have b_t=0 except b_3703=1; the appended b_3704=0.
The audit derives this formula independently using Euler's criterion.

Suppose f is AP-free and differs from b on at most two maximal nonempty
contiguous runs. Let e_t=b_t XOR f_t, e_0=0, and
s_t=e_t AND NOT e_(t-1). These s_t count exactly the starts of maximal runs
of e=1, including a run starting at position1 or ending at position3704.
Thus their sum is at most two. The two first-position clauses enforce
s_1 iff e_1. At every t>1, the three clauses

```
(-s_t OR e_t), (-s_t OR -e_(t-1)),
(s_t OR -e_t OR e_(t-1))
```

enforce the exact displayed start definition.

Introduce fresh variables A_i for1<=i<=N-2 and B_i for2<=i<=N-1. Use:

```
s_i -> A_i                          (1<=i<=N-2)
A_i -> A_(i+1)                      (1<=i<=N-3)
(s_i AND A_(i-1)) -> B_i             (2<=i<=N-1)
B_i -> B_(i+1)                      (2<=i<=N-2)
NOT(s_i AND B_(i-1))                (3<=i<=N)
```

Every at-most-two start assignment extends to these clauses by setting
A_i=1 iff the prefix s_1,...,s_i contains at least one start, and B_i=1 iff
that prefix contains at least two. In particular there is no extra
restriction on an edit mask. Conversely, if starts p<q<r existed, the first
two implications force A_(q-1)=1, the third forces B_q=1, and propagation
forces B_(r-1)=1, contradicting the last implication at r. Therefore this
counter projects exactly to the desired at-most-two-start condition.

Actual identifiers: e_t=t and s_t=N+t, with T=2N. A_1=T+1,A_2=T+2,
A_i=T+2i-1 for i>=3; B_2=T+3 and B_i=T+2i-2 for i>=3. They are precisely
the fresh identifiers T+1,...,4N-4. The independent audit checks every
literal clause as a multiset against these five implication families,
the start definitions, and the AP clauses; it imports no constructor or
solver. Extra hypotheses or missing/altered clauses fail that audit.

For each (a,d) in `AP-pool.json`, the audit checks positive integers a,d and
a+6d<=3704. If p is a term of the AP, define literal l_p=e_p when b_p=0,
and l_p=NOT e_p when b_p=1. This literal is true iff f_p=1. Both
OR_p l_p and OR_p NOT l_p therefore hold, because f has neither an all-zero
nor an all-one AP. These clauses impose no modular or wrapped progression.

Consequently every hypothesized AP-free f with at most two edit runs
extends to a model of the canonical CNF. Its14,812 variables and32,589
clauses have exact SHA256
b7177923f7d00ee3611649c25d7b42f891fd07808643447f120909531b796fba.

The independently checked positive-hint RUP certificate proves this CNF
unsatisfiable. A proposed proof clause C is checked by setting every literal
of C false, then following specified existing clauses. Each must actually
be unit or all-false under the accumulated partial assignment; only an
actual unit may be propagated, and an actual false clause must conclude
the chain. Thus each addition is implied by the current formula. Deletions
preserve satisfiability. The final checked empty clause proves
unsatisfiability of the original formula. The strict checker verifies all
22,622 such additions and54,807 identifier deletions in the reference trace.
No RAT reasoning or unchecked solver status is needed for this implication.
This contradicts the model obtained from f and proves the family exclusion.

Exactly two maximal edit runs correspond bijectively to four distinct cuts
0<=L1<R1<L2<R2<=N. The strict gap R1<L2 leaves at least one unchanged
position between them. There are C(N+1,4)=7,838,592,273,330 such masks.
Including one-run masks and the all-zero mask gives
1+C(N+1,2)+C(N+1,4)=7,838,599,134,991. The CNF represents the entire
quantified family, rather than only the ten queried candidates.

It follows that every AP-free f differs from b on at least three maximal
runs. Since 1-f is also AP-free, applying the same statement to1-f shows
that f agrees with b on at least three runs as well. The binary indicator
e therefore has at least six alternating constant runs, hence at least
five adjacent transitions. If it has exactly three runs of ones, it
cannot start and end with1, since that would leave only two runs of zeros.

This does not assert an AP-free3704 word, a new W(2,7) bound, or exclusion
of arbitrary colorings. It gives a complete barrier for the precisely
defined construction family and a necessary transition condition for the
next construction attempt.
