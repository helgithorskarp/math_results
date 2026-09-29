"""Small known instance and meaningful malformed-certificate controls."""
import json
from construct import refine
from verify import check_pairs


def rejects(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("An invalid input was accepted")


if __name__ == "__main__":
    # Classical minimum-three covering at LCM 120.
    seed = [[0,3], [0,4], [0,5], [1,6], [1,8], [2,10], [11,12],
            [1,15], [14,20], [5,24], [8,30], [6,40], [58,60], [26,120]]
    check_pairs(seed, 3, 120)
    lift = [list(pair) for pair in refine([tuple(p) for p in seed], 3, 0)]
    check_pairs(lift, 4, 360)
    rejects(lambda: check_pairs(seed + [[1,3]], 3, 120))
    rejects(lambda: check_pairs([[3,3]] + seed[1:], 3, 120))
    rejects(lambda: check_pairs(seed, 4, 120))
    rejects(lambda: check_pairs(seed, 3, 240))
    rejects(lambda: check_pairs([[0,2], [0,3]], 2, 6))
    rejects(lambda: refine([(0,2), (0,3), (1,4), (1,6), (11,12)], 2, 0))
    rejects(lambda: refine([tuple(p) for p in seed], 4, 0))
    rejects(lambda: refine([tuple(p) for p in seed], 3, 1))
    print(json.dumps({"small_seed_lcm": 120, "small_lift_lcm": 360,
                      "negative_controls_passed": 8}, sort_keys=True))
