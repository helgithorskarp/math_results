# Period618 six-phase normal form and affine symmetry barrier

Author: **six-vdw-1**, role **researcher**, 2026-09-30 UTC. Exact computer-assisted lemma with separate same-author native enumeration and Python replay; not peer reviewed or formalized. The shared signing identity does not establish distinct authorship.

A binary word on **Z/618Z** avoids every monochromatic seven-term progression with **nonzero step, allowing repeated residues**, only if its color-preserving affine stabilizer has order dividing **12**. Its CRT column-phase stabilizer has order dividing **6**. The complete six-state parameterization below remains an unresolved construction direction toward a length3704 witness. This supplies neither a new W(2,7) lower bound nor an exclusion of unrestricted period618 or interval colorings.

## Exact phase parameterization

Write t in CRT coordinates x=t mod103 and y=t mod6. Step309 forces c(x,y+3)=1-c(x,y). Step206, of order3, forces both parity triples of y to be nonconstant. Of the eight antipodal six-bit columns, exactly the two alternating columns fail this condition. The six surviving columns are the rotations of000111. Thus there is a unique function phi:Z/103Z -> Z/6Z satisfying

    c(t) = 1[ ((t mod6)-phi(t mod103)) mod6 >=3 ].

Conversely these columns satisfy every cyclic progression whose nonzero step is divisible by103, because its order is2,3 or6. Every other seven-term progression visits seven distinct x coordinates. Therefore the full problem is exactly a103-variable constraint problem with six states each, imposing

    NAE( 1[ (b+j*s-phi(a+j*r)) mod6 >=3 ] : j=0,...,6 ),
    a,r in Z/103Z, r!=0; b,s in Z/6Z.

This is a necessary reparameterization, not an optional symmetry assumption. Restricting phi to{0,3} would recover the separable CRT product and is not imposed here. The same normal form holds at period6q for every prime q>=7, with q replacing103. This elementary CRT observation is not claimed as historically new.

For period618, the full cyclic condition is equivalent to avoiding seven-term progressions on the first3704 positions. Reverse any cyclic step larger than309, choose its start in[0,617], and realize all seven points below2472. Conversely every interval progression on[0,3703] has step at most617, nonzero modulo618. All residues, including repetitions from steps of order2 or3, must be checked. A period p<=617 is impossible at3704, since0,p,...,6p fits and has a single color. Period618 is the smallest possible periodic template, not a claimed minimal period of an existing witness.

## Exact order17 column obstruction

The prime103 has primitive root5 and102=6*17. Suppose phi is invariant under the subgroup H=<5^6> of order17. Its nonzero values are constant on six multiplicative cosets5^i H. Its value at zero is independent. Translation by a multiple of103 leaves x fixed and shifts y through all six values, rotating every phase equally. It preserves cyclic progressions and H invariance, so normalize phi(0)=0 without losing any coloring. Exactly6^6=46656 normalized assignments remain, representing all6^7=279936 unnormalized assignments.

[enumerate.cpp](enumerate.cpp) constructs the six cosets by explicit multiplication, enumerates every normalized phase assignment, and tests cyclic progressions directly. It found a monochromatic progression for every assignment. The total was15725418 tested start/step pairs. An interrupted run returns INCOMPLETE, not an exclusion.

For each assignment it writes one pair(a,d) as two unsigned16-bit little-endian integers, after the12-byte header `VDW618H17_1\n`. There are exactly46656 records in increasing little-endian base-six assignment order. The independently checked186636-byte certificate is regenerated locally and omitted from Git. SHA256:

    91297899505896e510d0aa438b46f4cc76f48e22608609c1b4d93042657612a9

[check.py](check.py) imports neither the enumerator nor a solver. It labels each nonzero x using the quotient image x^17, verifies complete file coverage, reconstructs each parameter word, and checks its seven actual colors. It reverses large steps and verifies a monochromatic interval realization below2472 for every record. It checks326592 point colors. Six controls reject a bad header, missing coverage, extra coverage, zero step, out-of-domain start and a nonmonochromatic record.

Hence no valid phi has H17 symmetry. Its color-preserving multiplicative stabilizer is a subgroup of F_103^*, of order dividing102. Every divisor greater than6 contains17. Therefore its order divides6. This is symmetry of the CRT phase function over103, distinct from multiplicative rigidity of punctured-field patterns over617.

## Color-preserving affine stabilizer

Let G be all maps t -> u*t+v modulo618, with gcd(u,618)=1, preserving c's two named colors. No nonidentity translation preserves c: translation by v!=0 would make t,t+v,...,t+6v monochromatic. Thus projection of G to the unit group is injective. The unit group has order204=12*17, so |G| divides204.

If17 divided |G|, Cauchy's theorem would give g(t)=u*t+v of order17. Its multiplier also has order17. Modulo6, u=1 and g^17=id gives17*v=0, hence v=0. Modulo103, u has order17 and u!=1. Choose B with B=v/(1-u) modulo103 and B=0 modulo6. Then g(B)=B modulo618. Conjugating by translation of B gives pure multiplication with coordinates (x,y)->(u*x,y). Translating the coloring preserves its progression freedom; uniqueness of the six-phase representation makes its phi invariant under H17. The exact obstruction above rules this out. Therefore17 does not divide |G|, and **|G| divides12**.

The independent checker enumerates all204 unit multipliers and16 of order17, then verifies all1648 affine order17 maps and their CRT conjugation. In this composite modulus the fixed center is not unique; no prime-field uniqueness argument is assumed. Neither bound asserts existence at its endpoint, and no unrestricted coloring is excluded.

The projection argument is adapted, with explicit composite-modulus CRT steps, from **six-reviewer-3's** [independent affine QR617 review](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_affine_rigidity_review3), graph bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4, source338836f8162e978d6dd43d9851a067a99b006ba4. That review concerns a different prime and is cited for the argument, not used as a computational proof input here.

## Reproduction and trust boundary

From this directory:

    python3 reproduce.py

Requires CPython3.11+ and g++ with C++17, standard libraries only. The wrapper compiles, generates the certificate twice, compares its bytes, independently replays every record and six negative controls, checks the group/normal-form bridges, and verifies fail-closed tiny-time-budget behavior. It compares the entire deterministic output with [expected.json](expected.json). Success prints VERIFIED. Generated state stays in the ignored build directory.

Explicit commands:

    mkdir -p build
    g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow enumerate.cpp -o build/enumerate
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 build/enumerate build/obstructions.bin 30
    python3 check.py build/obstructions.bin --controls

At initial validation, native enumeration took0.273s and independent replay with controls0.205s. Full enumeration also passed address/undefined-behavior sanitizers with byte-identical certificate, in0.989s. All solver/BLAS/OpenMP threads were one; no concurrent CPU job or resource escalation was used. Positive elapsed times control interruption only, never a mathematical decision. Native arithmetic stays below618^2; indices and certificate integers are range checked. Python uses exact integers.

The trust boundary is the published source, compiler/interpreter, exact CRT and finite-group proofs, and exhaustive certificate coverage. Hashes anchor reproducibility; the individual progression checks establish the exclusion. This is not a proof-assistant formalization. No key, ledger, external proof corpus, solver verdict or unpublished mathematical input is needed.

## Context and remaining construction frontier

[Monroe, JCMCC128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/), Tables1/2, gives the inspected incumbent >3703 at modulus617 and uses W(length,colors). Here W(2,7) means two colors and seven terms; a3704-point witness would imply W(2,7)>=3705. This artifact claims no current record verification beyond that inspected primary context.

[Heule, Section4.3](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf) and [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf) supply prior multiplicative and cyclic construction methods. [Grier's cyclic note](https://danielgrier.com/documents/cyclic_waerden.pdf) requires distinct terms, whereas the periodic interval bridge here must include repeated residues. That convention difference matters at steps309 and206.

The previous [617 order11 rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity), graph bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem, motivated moving beyond those closed templates. The present composite-period618 lemma does not generalize that prime617 statement. The teammates' fixed-QR617 edit budgets and affine QR617 seam barriers concern different base words and domains; their constants do not transfer here.

Bounded primary-source and relevant campaign searches did not locate this exact order17 obstruction or period618 affine bound. No historical priority is asserted. The useful next direction is the unrestricted six-state phase construction, or the first permitted column symmetry order6/index17 over103. Exploratory local search found only invalid target words; it is not part of this proof and gives no exclusion. The length3704 witness remains unresolved.
