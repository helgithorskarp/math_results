"""Exact arithmetic for the support-union Tuza certificate."""

from argparse import ArgumentParser
from math import comb, isqrt


def clique_packing_number(k: int) -> int:
    if k < 3:
        return 0
    residue = k % 6
    if residue in (1, 3):
        leave = 0
    elif residue == 5:
        leave = 4
    elif residue in (0, 2):
        leave = k // 2
    else:
        leave = k // 2 + 1
    return (comb(k, 2) - leave) // 3


def discriminant(k: int) -> int:
    return -k * k + 2 * k + 8 * clique_packing_number(k)


def support_threshold(k: int) -> int:
    if k < 3:
        return k
    return (k + isqrt(discriminant(k))) // 2


def certificate(k: int, u: int) -> dict[str, int | bool]:
    if k < 3 or not 0 <= u <= k:
        raise ValueError("require k>=3 and 0<=u<=k")
    ell = max(u, k // 2)
    q = comb(k, 2)
    cover = q - ell * (k - ell)
    packing = clique_packing_number(k)
    return {
        "k": k,
        "u": u,
        "threshold": support_threshold(k),
        "cut_side": ell,
        "cover_size": cover,
        "clique_packing_size": packing,
        "slack": 2 * packing - cover,
        "certifies_tuza": cover <= 2 * packing,
    }


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("k", type=int)
    parser.add_argument("u", type=int)
    args = parser.parse_args()
    print(certificate(args.k, args.u))


if __name__ == "__main__":
    main()
