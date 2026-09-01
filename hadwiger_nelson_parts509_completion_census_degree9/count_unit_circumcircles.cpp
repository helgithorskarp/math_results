#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int BASIS = 8;
constexpr std::int64_t SCALE = 96;
constexpr std::int64_t DISTANCE_SCALE = SCALE * SCALE;
constexpr std::array<int, 3> PRIMES = {3, 5, 11};

using SmallField = std::array<std::int64_t, BASIS>;
using BigInteger = __int128;
using BigField = std::array<BigInteger, BASIS>;

struct Point {
    SmallField x{};
    SmallField y{};
};

int radical_factor(int left, int right) {
    int factor = 1;
    const int shared = left & right;
    for (int bit = 0; bit < 3; ++bit) {
        if (shared & (1 << bit)) {
            factor *= PRIMES[bit];
        }
    }
    return factor;
}

SmallField squared_distance(const Point& a, const Point& b) {
    std::array<__int128, BASIS> result{};
    for (int coordinate = 0; coordinate < 2; ++coordinate) {
        SmallField difference{};
        const auto& av = coordinate == 0 ? a.x : a.y;
        const auto& bv = coordinate == 0 ? b.x : b.y;
        for (int i = 0; i < BASIS; ++i) {
            difference[i] = av[i] - bv[i];
        }
        for (int i = 0; i < BASIS; ++i) {
            for (int j = 0; j < BASIS; ++j) {
                result[i ^ j] += static_cast<__int128>(difference[i]) * difference[j]
                    * radical_factor(i, j);
            }
        }
    }
    SmallField narrowed{};
    for (int i = 0; i < BASIS; ++i) {
        if (result[i] < std::numeric_limits<std::int64_t>::min()
            || result[i] > std::numeric_limits<std::int64_t>::max()) {
            throw std::overflow_error("squared-distance coefficient exceeds int64");
        }
        narrowed[i] = static_cast<std::int64_t>(result[i]);
    }
    return narrowed;
}

BigField multiply(const SmallField& left, const SmallField& right) {
    BigField result{};
    for (int i = 0; i < BASIS; ++i) {
        for (int j = 0; j < BASIS; ++j) {
            result[i ^ j] += static_cast<BigInteger>(left[i]) * right[j]
                * radical_factor(i, j);
        }
    }
    return result;
}

BigField multiply(const BigField& left, const SmallField& right) {
    BigField result{};
    for (int i = 0; i < BASIS; ++i) {
        for (int j = 0; j < BASIS; ++j) {
            result[i ^ j] += left[i] * right[j] * radical_factor(i, j);
        }
    }
    return result;
}

SmallField add_subtract(const SmallField& left, const SmallField& middle,
                        const SmallField& right) {
    SmallField result{};
    for (int i = 0; i < BASIS; ++i) {
        result[i] = left[i] + middle[i] - right[i];
    }
    return result;
}

bool is_exact_unit_circumcircle(const SmallField& s, const SmallField& t,
                                const SmallField& u) {
    // For squared side lengths s,t,u, 16*area^2 = 4*s*t-(s+t-u)^2.
    // The stored numerators have common denominator DISTANCE_SCALE, so
    // circumradius one is equivalent to
    // S*T*U = DISTANCE_SCALE * (4*S*T-(S+T-U)^2).
    const BigField st = multiply(s, t);
    const BigField stu = multiply(st, u);
    const SmallField w = add_subtract(s, t, u);
    const BigField w_squared = multiply(w, w);
    for (int i = 0; i < BASIS; ++i) {
        const BigInteger difference = stu[i]
            - DISTANCE_SCALE * (4 * st[i] - w_squared[i]);
        if (difference != 0) {
            return false;
        }
    }
    return true;
}

std::uint64_t mod_normalize(std::int64_t value, std::uint64_t modulus) {
    std::int64_t result = value % static_cast<std::int64_t>(modulus);
    if (result < 0) {
        result += static_cast<std::int64_t>(modulus);
    }
    return static_cast<std::uint64_t>(result);
}

std::uint64_t field_evaluation(const SmallField& value, std::uint64_t modulus,
                               const std::array<std::uint64_t, 3>& roots) {
    std::array<std::uint64_t, BASIS> basis{};
    basis[0] = 1;
    for (int mask = 1; mask < BASIS; ++mask) {
        std::uint64_t product = 1;
        for (int bit = 0; bit < 3; ++bit) {
            if (mask & (1 << bit)) {
                product = (product * roots[bit]) % modulus;
            }
        }
        basis[mask] = product;
    }
    std::uint64_t result = 0;
    for (int i = 0; i < BASIS; ++i) {
        result = (result + mod_normalize(value[i], modulus) * basis[i]) % modulus;
    }
    return result;
}

bool passes_modular_filter(std::uint64_t s, std::uint64_t t, std::uint64_t u,
                           std::uint64_t modulus) {
    const std::uint64_t st = (s * t) % modulus;
    const std::uint64_t stu = (st * u) % modulus;
    const std::uint64_t w = (s + t + modulus - u) % modulus;
    const std::uint64_t denominator = (4 * st + modulus - (w * w) % modulus) % modulus;
    const std::uint64_t rhs = (DISTANCE_SCALE % modulus) * denominator % modulus;
    return stu == rhs;
}

std::vector<Point> read_points(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open point file: " + path);
    }
    std::vector<Point> points;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == '#') {
            continue;
        }
        std::istringstream row(line);
        Point point;
        for (auto* coordinate : {&point.x, &point.y}) {
            for (auto& coefficient : *coordinate) {
                if (!(row >> coefficient)) {
                    throw std::runtime_error("point row has fewer than 16 coefficients");
                }
            }
        }
        std::string trailing;
        if (row >> trailing) {
            throw std::runtime_error("point row has more than 16 coefficients");
        }
        points.push_back(point);
    }
    return points;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: " << argv[0] << " points.tsv\n";
            return 2;
        }
        const auto points = read_points(argv[1]);
        if (points.size() != 509) {
            throw std::runtime_error("expected 509 points");
        }
        // This input bound gives a conservative coefficient bound below 2^105
        // for every exact circumradius identity coefficient, safely inside the
        // signed 128-bit range.  See README.md for the explicit calculation.
        for (const auto& point : points) {
            for (const auto& coordinate : {point.x, point.y}) {
                for (const auto coefficient : coordinate) {
                    if (coefficient < -144 || coefficient > 144) {
                        throw std::runtime_error("coordinate coefficient exceeds certified bound");
                    }
                }
            }
        }
        const std::size_t n = points.size();
        std::vector<SmallField> distances(n * n);
        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                distances[i * n + j] = squared_distance(points[i], points[j]);
                distances[j * n + i] = distances[i * n + j];
            }
        }

        constexpr std::uint64_t MOD1 = 60289;
        constexpr std::array<std::uint64_t, 3> ROOTS1 = {4799, 25141, 4267};
        constexpr std::uint64_t MOD2 = 1000081;
        constexpr std::array<std::uint64_t, 3> ROOTS2 = {35512, 183365, 29480};
        for (int bit = 0; bit < 3; ++bit) {
            if (ROOTS1[bit] * ROOTS1[bit] % MOD1 != static_cast<std::uint64_t>(PRIMES[bit])
                || ROOTS2[bit] * ROOTS2[bit] % MOD2 != static_cast<std::uint64_t>(PRIMES[bit])) {
                throw std::runtime_error("invalid modular square root constant");
            }
        }
        std::vector<std::uint64_t> values1(n * n), values2(n * n);
        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                values1[i * n + j] = values1[j * n + i]
                    = field_evaluation(distances[i * n + j], MOD1, ROOTS1);
                values2[i * n + j] = values2[j * n + i]
                    = field_evaluation(distances[i * n + j], MOD2, ROOTS2);
            }
        }

        std::uint64_t triples = 0;
        std::uint64_t first_filter_survivors = 0;
        std::uint64_t second_filter_survivors = 0;
        std::uint64_t exact_unit_circumcircles = 0;
        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                for (std::size_t k = j + 1; k < n; ++k) {
                    ++triples;
                    if (!passes_modular_filter(values1[i * n + j], values1[i * n + k],
                                               values1[j * n + k], MOD1)) {
                        continue;
                    }
                    ++first_filter_survivors;
                    if (!passes_modular_filter(values2[i * n + j], values2[i * n + k],
                                               values2[j * n + k], MOD2)) {
                        continue;
                    }
                    ++second_filter_survivors;
                    if (is_exact_unit_circumcircle(distances[i * n + j],
                                                   distances[i * n + k],
                                                   distances[j * n + k])) {
                        ++exact_unit_circumcircles;
                    }
                }
            }
        }
        std::cout << "all_checks=true\n"
                  << "vertices=" << n << "\n"
                  << "triples_checked=" << triples << "\n"
                  << "first_modular_filter_survivors=" << first_filter_survivors << "\n"
                  << "second_modular_filter_survivors=" << second_filter_survivors << "\n"
                  << "exact_unit_circumcircle_triples=" << exact_unit_circumcircles << "\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << "\n";
        return 1;
    }
}
