# Internal check by Lyra of Theo's definition-level rectangle checker

Author: literature-researcher-4. Checker: literature-researcher-2. Exact campaign target: decision message 410. This review checks a known definition-level reduction and finite code reproduction; it does not solve the growth target or constitute external peer review.

Reviewed source: `/scratch/research-team-colloquium-sol61-20261005/workspaces/literature-researcher-4/research/boxed2143_theo_20261005/rectangle_checker.py`, SHA-256 `93c4be5fa830f6628bc9f2031917f9f05d7bcb729bd2ca151180075df2f00a33`. Reviewed accompanying README and compared its reduction against the September primary Theorem 3.2 and decision 410.

## Reduction check for arbitrary finite permutations

Given a boxed occurrence, take lo and hi equal to the minimum and maximum selected values. Any additional point retained by this closed value interval and positioned between the first and last selected indices would have value strictly between lo and hi: distinctness of permutation values excludes a second point on a vertical boundary. Its index is likewise strictly interior because positions are distinct. Such a point violates the boxed condition. The four selected points therefore form a consecutive factor of the restricted word. For 2143 the second factor value is lo and third is hi; for 2413 these roles are reversed.

Conversely, four consecutive retained points with those canonical value boundaries have no extra point in their bounding rectangle. Every hypothetical extra interior point would be retained by the same interval and occur between the factor's endpoints. The four-point order then supplies exactly the chosen pattern. The canonical minimum/maximum make the interval unique for each occurrence, and the restricted-word location is unique. Sorting returned index tuples does not change that set.

The code enumerates every possible pair lo,hi. Four distinct integer values force hi-lo>=3, justifying its loop bounds. It enumerates every four-point consecutive factor in each restricted word and implements the correct order/boundary tests. The source's closed/open equivalence and the selected-point exclusions in 410 agree because a permutation has unique coordinates. I found no missing case in this known reduction.

## Independent finite reproduction

`python3 -B research/boxed2143_20261005/check_theo_rectangles.py > research/boxed2143_20261005/theo_rectangle_reproduction.json`

The independent representation enumerates index quadruples and literally scans the strict rectangle interior. Every complete occurrence set for both 2143 and the separately sourced 2413 baseline agrees for all 5,914 permutations of lengths 0 through 7. The ordered occurrence-stream hashes also agree with Theo's saved baseline, beyond aggregate count agreement. The target 2143 counts are 1,1,2,6,23,106,565,3395. Python 3.11.2, exact integers and standard-library enumeration are the trust base; elapsed time was about 0.81 seconds. Malformed-input and unsupported-pattern controls passed.

This validates the stated reduction and finite implementation comparison at the reviewed source hash. It does not establish exhaustive coverage at untested lengths by computation, a structural entropy bound, or an infinite growth theorem. Any future full-class decomposition/upper-bound claim requires a separate review of its whole argument and all asymptotic bridges.
