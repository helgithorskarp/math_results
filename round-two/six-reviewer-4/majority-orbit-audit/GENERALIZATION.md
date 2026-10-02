# The parameter-orbit count for every odd prime

**six-reviewer-4, independent mathematical reviewer.** This is a proved
generalization of the parameter-counting part of LEMMA9745, not a claim
of progression-free colorings or a repair obstruction at other primes.

For an odd prime \(p\), normalize three distinct signed roots to
\((0,1,t)\), with \(t\ne0,1\), and normalize the first input palette
to zero. There are \(4(p-2)\) parameter states. The same \(S_3\)
root/palette relabeling action is well defined over \(\mathbb F_p\).
It counts parameter orbits; different orbits may give identical words.

Identity fixes \(4(p-2)\) states. Each transposition fixes exactly two
states: the first-two swap forces \(t=1/2\), first relative palette
zero, and leaves the other palette free. Each three-cycle fixes exactly
\(n_p\) states, where \(n_p\) is the number of roots of
\(t^2-t+1\) over \(\mathbb F_p\); both relative palettes must be zero.
Burnside therefore gives
\[
\#\text{parameter orbits}
 =\frac{4(p-2)+6+2n_p}{6}.
\]

At \(p=3\), there is one quadratic root and the answer is two. For
\(p>3\), the quadratic roots are exactly the elements of multiplicative
order six: \((t+1)(t^2-t+1)=t^3+1\), and \(t=-1\) is excluded because
\(3\ne0\). Conversely an element of order six has cube minus one and
is not minus one, hence is a quadratic root. The cyclic group
\(\mathbb F_p^*\) has two elements of order six precisely when
\(p\equiv1\pmod3\), and none when \(p\equiv2\pmod3\). Thus
\[
\#\text{orbits}=\begin{cases}
2,&p=3,\\
(2p+1)/3,&p>3, p\equiv1\pmod3,\\
(2p-1)/3,&p>3, p\equiv2\pmod3.
\end{cases}
\]
The prime103 gives69, as required. This ordinary proof supplies uniformity;
the separate exact component counts in `general_orbits.py` at fourteen
explicit primes are controls, not extrapolation. No character-value
distinction at a root or progression certificate at other primes is used.
