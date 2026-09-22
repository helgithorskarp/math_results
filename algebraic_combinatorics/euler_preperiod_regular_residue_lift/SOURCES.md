# Sources and status audit

## Primary problem source

- Berke Guelec, *Modular periodicity of the Euler up/down numbers at odd
  prime powers*, arXiv:2608.27058v2 (3 September 2026),
  https://arxiv.org/abs/2608.27058v2 .  This proves the period theorem,
  gives the exact preperiod criterion used here, disproves the earlier exact
  preperiod conjecture at `5^5`, and proposes the surviving lower bound
  `s(p^r)>=r-2`.

## Classical arithmetic inputs

- DLMF 24.10.3 records the mod-`p` Kummer congruence
  `B_m/m = B_n/n (mod p)` when the indices are congruent and nonzero modulo
  `p-1`: https://dlmf.nist.gov/24.10.E3 .
- DLMF 24.15.4 records the tangent--Bernoulli identity:
  https://dlmf.nist.gov/24.15.E4 .
- D. E. Knuth and T. J. Buckholtz, *Computation of Tangent, Euler, and
  Bernoulli Numbers*, Math. Comp. 21 (1967), 663--688,
  https://www.ams.org/journals/mcom/1967-21-100/S0025-5718-1967-0221735-9/S0025-5718-1967-0221735-9.pdf .
  This is also the classical source for prime-power periodicity of tangent
  and Euler numbers.

## Discovery Net context

- Problem: `bafkreialtva5byyimxkdw3iwb4r5xfg6e37jshg5svsdylqkjfba7uahiq`.
- Exact modular triple classification:
  `bafkreiact6j6vv3byqm4ulufeco4ase3epnh6lh54ap6tauona77pt7mty`.
- Independent review identifying higher lifts as the next structural bridge:
  `bafkreic7tcpdux3d6dc4p3cosarfm23mmzqk2zgvyc25wz73tk3rvko7km`.
- Boundary-residue lift theorem:
  `bafkreia6wmbdao57hose7xc3xr6tgh3e3coiqvxgas37mdcmkipd2a3l5e`.

The boundary theorem treats the excluded residue `j=0 (mod p-1)`.  The
present theorem treats every interior Bernoulli-regular residue and thereby
closes the order-only part `O_p-B_p` of the requested higher-lift bridge.

## Search boundary

Live searches on 2026-09-22 covered the current Guelec v2 record, DLMF's
Kummer and tangent sections, Knuth--Buckholtz, searches for exact
`p`-adic valuations of tangent numbers, and literature on Kummer-type
congruences for tangent and Genocchi numbers.  They found classical
congruences and period results, but no source applying the displayed exact
regular-residue dichotomy to the `p^3,p^2,p` preperiod obstruction.

This is a bounded search, not a priority proof.  Because equation (1) is a
short corollary of classical identities, the contribution makes no exclusive
novelty claim for the standalone arithmetic formula.  Its claimed increment
is the class-wide structural bridge and the preperiod congruence sieve.
