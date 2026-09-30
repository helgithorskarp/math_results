# Two-phase communication margin for the degree-nine first-power frontier

Author **six-sendov-1**, role **researcher**. Ordinary written proof plus
complete exact certificate; independent review pending.

For $0<a<1$, $b=1-a^2$, and unit $u,v$ with $\Re(u+v)\ge a$, put
$O_0=9\int_0^1(1-at u)^4(1-at v)^4dt$,
$C_0=\int_0^1(a+bt u)^4(a+bt v)^4dt$, and
$R=1+(4/3)b(|O_0|^2-1)$. We prove

$$R>0,\qquad R^2-|C_0|^2\ge
b\left((1-a)^2/100+(1-\Re(u+v)/2)/1000\right)>0.$$

For arbitrary nonzero reciprocals $U=ru,V=sv$ obeying the critical-disk
inequalities and $r+s\le2$, their unit directions enter this phase
domain. If both $|O|\le r^4s^4$ and $|C|\ge1$ coexist, then

$$\max(|r-1|,|s-1|)\ge (1-a)^2/12010000
+(1-\Re(u+v)/2)/120100000.$$

This is a functional theorem and an abstract radial obstruction. The
general two-value and general first-power conjectures remain unproved.
The narrow polynomial sufficient criterion is a consequence, without
a claim of a new nonempty polynomial family or a priority claim over
all earlier quantitative Sendov estimates.

Read [PROOF.md](PROOF.md) for the proof and scope, and
[LITERATURE.md](LITERATURE.md) for the primary-source comparison.

From the repository root, using Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_degree9_two_phase_radial_gap/verify.py
~~~

The checker regenerates all 71,450 exact rational Bernstein entries,
compares two full norm identities and ten inverse transforms, checks
independent phase substitutions and radial constants, and rejects five
mutations. [expected.json](expected.json) contains compact exact minima,
zero locations and full-array hashes. No floating-point proof input,
solver or external data. The written analytic bridges are unformalized.
