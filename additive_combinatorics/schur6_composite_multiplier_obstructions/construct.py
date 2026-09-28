"""Explicit product colourings witnessing the sharp order-3 and order-5 costs."""


def witnesses():
    # A symmetric modular five-colouring of Z/49 minus zero.
    small = [0,1,2,3,3,1,1,0,4,0,1,0,3,2,1,1,0,2,0,1,0,2,0,1,
             1,0,2,0,1,0,2,0,1,1,2,3,0,1,0,4,0,1,1,3,3,2,1,0]
    nine, ten = [], []
    for x in range(1, 539):
        a, b = x % 49, x % 11
        if a:
            layer = 0 if a % 7 else 1
            digit = a % 7 if layer == 0 else a // 7
            nine.append(3 * layer + min(digit, 7 - digit) - 1)
        else:
            nine.append(6 + {1:0, 2:1, 3:1, 4:0, 5:2}[min(b, 11-b)])
        ten.append(min(b, 11-b) - 1 if b else 5 + small[a-1])
    return [
        {"name":"mod49_five", "modulus":49, "colours":5,
         "multiplier":48, "permutation":list(range(5)),
         "word":"".join(map(str, small))},
        {"name":"mod539_order3_nine", "modulus":539, "colours":9,
         "multiplier":67, "permutation":[2,0,1,5,3,4,6,7,8],
         "word":"".join(map(str, nine))},
        {"name":"mod539_order5_ten", "modulus":539, "colours":10,
         "multiplier":344, "permutation":[2,4,1,0,3,5,6,7,8,9],
         "word":"".join(map(str, ten))},
    ]
