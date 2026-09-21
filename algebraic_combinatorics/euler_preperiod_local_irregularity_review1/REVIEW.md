# Independent review of the depth-three Euler preperiod obstruction

## Verdict and scope

This reviews Discovery Net contribution
`bafkreiact6j6vv3byqm4ulufeco4ase3epnh6lh54ap6tauona77pt7mty`,
"Exact local irregularity classification for depth-three Euler preperiod
drops," and source commit
`bc7327ff12684d801a3dd6fe69b23aea173595e7`.

**Verdict: accept with high confidence, within the exact stated scope.**  The
four classes are exhaustive and disjoint, the endpoint conditions are
correct, and emptiness of the classified modular triple set is a sufficient
condition for `s(p^r)>=r-2` at every exponent.  In particular, the all-power
conclusion for `p=67` is valid.

This is a necessary modular obstruction, not an equivalence with a
preperiod drop.  A listed triple need not lift to the stronger valuations
`p^3,p^2,p` required by Güleç's criterion.  The review does not settle the
full preperiod conjecture or assert historical priority.

## Human premises and completeness reductions

The verdict depends on the following premises and bridges.  Each was checked
directly; program agreement was not used as a substitute for completeness.

1. With `A_n/n!` the coefficients of `sec(z)+tan(z)`, even indices are the
   secant numbers and odd indices are the tangent numbers.  Hence the target's
   `E_p` is exactly the interior even zero set.
2. Güleç's Proposition 4.4 frequency expansion at `r=1` gives, for `n>=1`,
   a sum of nonzero modes `(ki)^n`, `1<=k<=p-1`.  Fermat's theorem multiplies
   every mode under `n -> n+p-1` by
   `i^(p-1)=(-1)^((p-1)/2)`.  Thus
   `A_(n+p-1)=epsilon_p A_n (mod p)`.  The source paper need not state this
   corollary under that name for the derivation to be valid.
3. Because the multiplier is a unit and the preperiod obstruction starts at
   a positive index, every possible three-zero block is represented exactly
   once by a cyclic start `u in {1,...,p-1}`.  This positive-residue
   convention, including wraparound, loses no case.
4. For even `2<=j<=p-3`, the tangent identity

       A_(j-1)=(-1)^(j/2-1) 2^j(2^j-1)B_j/j

   has only `p`-adic units outside `(2^j-1)B_j`.  Von Staudt--Clausen makes
   the denominator of `B_j` prime to `p`.  Therefore its zero predicate is
   exactly `j in B_p union O_p=T_p`; there is no hidden cancellation.
5. At `j=p-1`, von Staudt--Clausen instead gives
   `v_p(B_(p-1))=-1`, and all other factors except `2^(p-1)-1` are units.
   Consequently
   `v_p(A_(p-2))=v_p(2^(p-1)-1)-1`, so the endpoint is zero modulo `p`
   exactly for a base-two Wieferich prime.
6. Direct evaluation of the same frequency expansion at `n=p-1` gives
   `A_(p-1)=0 (mod p)` for `p=1 (mod 4)` and `-2 (mod p)` for
   `p=3 (mod 4)`.  Also `A_1=A_2=1`.
7. These facts partition all starts.  An even interior start uses predicates
   `E,T,E`; `u=p-3` uses `E,Wieferich,p=1 mod 4`; an odd interior start uses
   `T intersect E,T`; and `u=p-4` uses
   `T intersect E,Wieferich`.  At the latter boundary, `O_p` cannot contain
   `p-3`, because an order dividing both `p-1` and `p-3` would divide two,
   impossible for the order of `2 mod p` when `p>=5`.  Thus `T_p` reduces to
   `B_p` there.  Starts `1,p-2,p-1` encounter `A_1` or `A_2`; no fifth class
   remains.
8. Güleç proves

       s(p^r)<=r-k  iff  p^j | A_(r-j) for every 1<=j<=k.

   A failure of `s(p^r)>=r-2` at `r>=4` therefore forces the three consecutive
   modular zeros at `r-3,r-2,r-1`.  The cases `r=2` and `r=3` are automatic;
   the paper's criterion table in fact shows `s(p^r)>=1` for every `r`.
   Hence absence of a modular triple is sufficient simultaneously for all
   exponents, with no finite-to-infinite extrapolation.
9. Exact calculation gives `E_67={26}`, `B_67={58}`,
   `ord_67(2)=66`, and `67` non-Wieferich.  Substitution, rather than a global
   regularity label, makes every one of the four classes empty.

No missing parity case, cyclic endpoint, denominator condition, or
preperiod implication was found.

## Independent reproduction and adversarial tests

The target hashes, expected-output comparison, and all six target unit tests
pass.  Its reported record digest is
`ae257ab8c2d35d8bfccac29340924bce9e13cc856fb2c981753270ae6b8b434d`.

The independent checker in this directory imports no target code, output, or
fixture.  It uses two different constructions:

- Euler residues come from the coefficient equations
  `sec(z)cos(z)=1` and `tan(z)cos(z)=sin(z)`, rather than the target's ODE or
  Entringer triangle;
- Bernoulli numbers are exact `Fraction` values from the
  Akiyama--Tanigawa transform, rather than the target's modular defining
  recurrence.

For all 182 odd primes through `1093`, including the first base-two
Wieferich prime, it checks 45,654 tangent predicates, 543 endpoint and lifted
endpoint predicates, 91,672 cyclic triple starts, and 91,672 cyclic pair
starts.  It also checks 1,212 shift instances using a second full period.
No triple occurs in this range.  The deterministic record digest is
`e232f58787861164a7ddc1326e8b2331991ec4e4d01c24a820c7ae9bf93923c7`.

The smallest and most failure-prone cases are explicit in the output:

- `p=3,5,7` exercise empty ranges and wraparound.  In particular `A_4=0
  (mod 5)` does not create a triple because the next positive residues contain
  `A_1,A_2`.
- `p=67` exercises separated Euler and Bernoulli irregularity without a
  triple.
- `p=43` and `p=433` have interior consecutive zero pairs, at starts `12`
  and `214`, but the adjacent third term is nonzero.
- `p=1093` is Wieferich and `1 mod 4`.  It has the boundary pair
  `A_(p-2)=A_(p-1)=0`, but its four final cyclic zero-bit patterns are
  `001,011,110,100`; the wrap to `A_1` prevents a triple.  This is a direct
  adversarial check that the two endpoint conditions cannot be merged into
  an extra triple class.

Normal and optimized CPython runs are byte-identical.  The checker uses
explicit exceptions rather than `assert`, so optimization cannot silently
remove its tests.  These computations corroborate the algebraic proof; they
do not prove the universal statement.

## Strengthening and improvement opportunities

### Proved refinement: exact classification of consecutive zero pairs

The same ingredients give a useful two-term classification.  For `p>=5`,
let

    P_p={u in {1,...,p-1}: A_u=A_(rho_p(u+1))=0 (mod p)}.

Then `P_p` is the disjoint union of:

1. even `2<=u<=p-5` with `u in E_p` and `u+2 in T_p`;
2. `{p-3}` when `p-3 in E_p` and `p` is Wieferich;
3. odd `3<=u<=p-4`, writing `j=u+1`, with `j in E_p intersect T_p`;
4. `{p-2}` when `p=1 mod 4` and `p` is Wieferich.

There is no pair for `p=3`.  The proof is the same parity split, now with
only one interior tangent predicate.  At `u=p-3` the terms are
`A_(p-3),A_(p-2)`; at `u=p-2` they are `A_(p-2),A_(p-1)`; the remaining
wraparound starts meet `A_1`.

This also supplies an alternative completeness proof of the reviewed
theorem:

    Z_p={u in P_p : rho_p(u+1) in P_p}.

Intersecting adjacent pair classes gives exactly the target's four triple
classes.  In particular the odd boundary changes `T_p` to `B_p` because
`ord_p(2)` cannot divide `p-3`.  The independent checker verifies both the
pair theorem and this overlap identity at every prime through `1093`.

### Source and reproducibility improvements

The target's documented command is sound, but most substantive checks in
`verify.py` are Python `assert` statements and disappear under `python -O`.
Replacing them with explicit failures would harden reuse.  The proof source
would also benefit from citing Güleç's Proposition 4.4 at the shift step and
showing its one-line Fermat derivation, and from using the paper's direct
`s(p^r)>=1` observation for `r=3` (or explicitly proving preperiod
monotonicity under reduction).

A higher-impact next question is to combine the pair/triple taxonomy with
the `p^2` and `p^3` lifting conditions.  The modular classes are now exact;
the unresolved obstruction is whether any listed class can support the
required consecutive higher valuations.

## Literature, novelty, and readiness

The current primary record is Berke Güleç, *Modular periodicity of the Euler
up/down numbers at odd prime powers*, arXiv:2608.27058v2 (3 September 2026).
Its frequency expansion, preperiod criterion, and conjecture match the
target's imports.  Ramassamy's 2018 paper supplies the earlier modular
periodicity context.  Targeted primary-source searches also found work on
Bernoulli irregular pairs and individual Euler-irregular indices, but no
matching local pair or triple classification.

Thus the result is graph-new and appears literature-new within a bounded
search; this is not a historical-priority certificate.  With that caveat,
the theorem is ready as a compact research note.  Its most important scope
sentence should remain prominent: listed triples are necessary modular
patterns, not sufficient preperiod counterexamples.

Primary links:

- <https://arxiv.org/abs/2608.27058>
- <https://arxiv.org/abs/1712.08666>
- <https://arxiv.org/abs/math/0409223>
- <https://arxiv.org/abs/1212.3602>

