#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>

using U = unsigned __int128;
using I = __int128;

namespace {

constexpr int MAX_N = 64;
constexpr int MAX_DEGREE = 4;

int n;
int middle;
std::array<U, MAX_N> left_size{};
std::array<U, MAX_N> right_size{};
std::array<I, MAX_N> condition_value{};
std::array<int, MAX_N> condition_side{};
std::array<std::array<I, MAX_N>, MAX_N> parameter{};

U best = 0;
std::array<U, MAX_N> best_left{};
std::array<U, MAX_N> best_right{};
U prefix_count = 0;
U raw_two_layer_leaves = 0;
U critical_pair_count = 0;
U polynomial_checks = 0;
U condition_slope_checks = 0;
U maximum_candidates_per_prefix = 0;

struct Polynomial {
    std::array<std::array<I, MAX_DEGREE + 1>, MAX_DEGREE + 1> c{};
};

struct Interval {
    I lo = 0;
    I hi = -1;

    bool valid() const { return lo <= hi; }
};

std::string to_string_u128(U value) {
    if (value == 0) {
        return "0";
    }
    std::string out;
    while (value != 0) {
        out.push_back(static_cast<char>('0' + value % 10));
        value /= 10;
    }
    std::reverse(out.begin(), out.end());
    return out;
}

I floor_div(I numerator, I denominator) {
    if (denominator == 0) {
        throw std::runtime_error("division by zero");
    }
    I quotient = numerator / denominator;
    const I remainder = numerator % denominator;
    if (remainder != 0 && ((remainder > 0) != (denominator > 0))) {
        --quotient;
    }
    return quotient;
}

I ceil_div(I numerator, I denominator) {
    return -floor_div(-numerator, denominator);
}

I positive_mod(I value, I modulus) {
    I answer = value % modulus;
    if (answer < 0) {
        answer += modulus;
    }
    return answer;
}

Interval restrict_le(Interval interval, I slope, I constant, I rhs) {
    if (!interval.valid()) {
        return interval;
    }
    const I target = rhs - constant;
    if (slope > 0) {
        interval.hi = std::min(interval.hi, floor_div(target, slope));
    } else if (slope < 0) {
        interval.lo = std::max(interval.lo, ceil_div(target, slope));
    } else if (constant > rhs) {
        interval.hi = interval.lo - 1;
    }
    return interval;
}

Interval restrict_ge(Interval interval, I slope, I constant, I rhs) {
    return restrict_le(interval, -slope, -constant, -rhs);
}

Polynomial constant_poly(I value) {
    Polynomial answer;
    answer.c[0][0] = value;
    return answer;
}

Polynomial u_poly() {
    Polynomial answer;
    answer.c[1][0] = 1;
    return answer;
}

Polynomial t_poly() {
    Polynomial answer;
    answer.c[0][1] = 1;
    return answer;
}

Polynomial add(const Polynomial &a, const Polynomial &b) {
    Polynomial answer;
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            answer.c[i][j] = a.c[i][j] + b.c[i][j];
        }
    }
    return answer;
}

Polynomial subtract(const Polynomial &a, const Polynomial &b) {
    Polynomial answer;
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            answer.c[i][j] = a.c[i][j] - b.c[i][j];
        }
    }
    return answer;
}

Polynomial multiply(const Polynomial &a, const Polynomial &b) {
    Polynomial answer;
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            if (a.c[i][j] == 0) {
                continue;
            }
            for (int k = 0; k <= MAX_DEGREE; ++k) {
                for (int ell = 0; ell <= MAX_DEGREE; ++ell) {
                    if (b.c[k][ell] == 0) {
                        continue;
                    }
                    if (i + k > MAX_DEGREE || j + ell > MAX_DEGREE) {
                        throw std::runtime_error("polynomial workspace overflow");
                    }
                    answer.c[i + k][j + ell] += a.c[i][j] * b.c[k][ell];
                }
            }
        }
    }
    return answer;
}

void require_total_degree(const Polynomial &poly, int maximum) {
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            if (i + j > maximum && poly.c[i][j] != 0) {
                throw std::runtime_error("unexpected polynomial degree");
            }
        }
    }
}

I evaluate(const Polynomial &poly, I u, I t) {
    std::array<I, MAX_DEGREE + 1> upow{};
    std::array<I, MAX_DEGREE + 1> tpow{};
    upow[0] = 1;
    tpow[0] = 1;
    for (int i = 1; i <= MAX_DEGREE; ++i) {
        upow[i] = upow[i - 1] * u;
        tpow[i] = tpow[i - 1] * t;
    }
    I answer = 0;
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            answer += poly.c[i][j] * upow[i] * tpow[j];
        }
    }
    return answer;
}

Polynomial convolution_poly(
    const std::array<Polynomial, MAX_N> &left,
    const std::array<Polynomial, MAX_N> &right, int index) {
    Polynomial answer;
    for (int j = 0; j < index; ++j) {
        answer = add(answer, multiply(left[j], right[index - 1 - j]));
    }
    return answer;
}

U convolution_at(int index) {
    U value = 0;
    for (int j = 0; j < index; ++j) {
        value += left_size[j] * right_size[index - 1 - j];
    }
    return value;
}

bool prefix_is_symmetric(int current_level) {
    for (int i = 0; i < current_level; ++i) {
        if (left_size[i] != right_size[i]) {
            return false;
        }
    }
    return true;
}

void compute_condition(int index) {
    for (int j = 0; j < index; ++j) {
        for (int k = j - 1; k >= 0; --k) {
            parameter[j][k] = 0;
            for (int ell = k; ell < j; ++ell) {
                const int side = condition_side[n - index + ell - 1];
                const U factor = side ? right_size[j - ell - 1]
                                      : left_size[j - ell - 1];
                parameter[j][k] += static_cast<I>(factor) * parameter[ell][k];
            }
        }
    }

    const int position = n - index - 2;
    I value = static_cast<I>(right_size[index]) -
              static_cast<I>(left_size[index]);
    for (int j = 0; j < index; ++j) {
        I inner = 0;
        for (int ell = 0; ell <= j; ++ell) {
            inner += parameter[j][ell] *
                     (static_cast<I>(right_size[ell]) -
                      static_cast<I>(left_size[ell]));
        }
        const int side = condition_side[n - index + j - 1];
        const U factor = side ? right_size[index - j - 1]
                              : left_size[index - j - 1];
        value += inner * static_cast<I>(factor);
    }
    condition_value[position] = value;
    condition_side[position] = value >= 0 ? 1 : 0;
}

void add_quadratic_points(std::set<I> &points, I quadratic, I linear,
                          Interval interval, I residue = 0, I step = 1) {
    if (!interval.valid()) {
        return;
    }
    const I first = interval.lo + positive_mod(residue - interval.lo, step);
    if (first > interval.hi) {
        return;
    }
    const I last = interval.hi - positive_mod(interval.hi - residue, step);
    const I count = (last - first) / step;
    if (quadratic >= 0) {
        points.insert(first);
        points.insert(last);
        return;
    }
    const I transformed_quadratic = quadratic * step * step;
    const I transformed_linear = (2 * quadratic * first + linear) * step;
    const I below_vertex =
        floor_div(-transformed_linear, 2 * transformed_quadratic);
    for (I z : {below_vertex, below_vertex + 1}) {
        z = std::max<I>(0, std::min<I>(count, z));
        points.insert(first + step * z);
    }
}

std::set<std::pair<U, U>> critical_pairs(const Polynomial &objective,
                                         I sm_slope, I sm_constant,
                                         Interval interval) {
    require_total_degree(objective, 2);
    if (objective.c[0][2] != -1) {
        throw std::runtime_error("t^2 coefficient is not -1");
    }
    for (int i = 0; i <= MAX_DEGREE; ++i) {
        for (int j = 0; j <= MAX_DEGREE; ++j) {
            const bool allowed = (i == 0 && j == 0) ||
                                 (i == 1 && j == 0) ||
                                 (i == 2 && j == 0) ||
                                 (i == 0 && j == 1) ||
                                 (i == 1 && j == 1) ||
                                 (i == 0 && j == 2);
            if (!allowed && objective.c[i][j] != 0) {
                throw std::runtime_error("objective is not bivariate quadratic");
            }
        }
    }

    const I base_quadratic = objective.c[2][0];
    const I base_linear = objective.c[1][0];
    const I b_slope = objective.c[1][1];
    const I b_constant = objective.c[0][1];
    std::set<std::pair<U, U>> answer;

    Interval lower = restrict_le(interval, b_slope, b_constant, 0);
    if (lower.valid()) {
        std::set<I> us;
        add_quadratic_points(us, base_quadratic, base_linear, lower);
        for (I u : us) {
            answer.emplace(static_cast<U>(u), 0);
        }
    }

    Interval interior = restrict_ge(interval, b_slope, b_constant, 1);
    interior = restrict_le(interior, b_slope - 2 * sm_slope,
                           b_constant - 2 * sm_constant, -1);
    if (interior.valid()) {
        const I h_quadratic =
            4 * base_quadratic + b_slope * b_slope;
        const I h_linear =
            4 * base_linear + 2 * b_slope * b_constant;
        std::set<I> us;
        if (b_slope % 2 == 0) {
            add_quadratic_points(us, h_quadratic, h_linear, interior);
        } else {
            add_quadratic_points(us, h_quadratic, h_linear, interior, 0, 2);
            add_quadratic_points(us, h_quadratic, h_linear, interior, 1, 2);
        }
        for (I u : us) {
            const I b_value = b_slope * u + b_constant;
            if (b_value <= 0) {
                throw std::runtime_error("invalid interior critical point");
            }
            answer.emplace(static_cast<U>(u), static_cast<U>(b_value / 2));
        }
    }

    Interval upper = restrict_ge(interval, b_slope, b_constant, 1);
    upper = restrict_ge(upper, b_slope - 2 * sm_slope,
                        b_constant - 2 * sm_constant, 0);
    if (upper.valid()) {
        const I substituted_quadratic =
            base_quadratic - sm_slope * sm_slope + b_slope * sm_slope;
        const I substituted_linear =
            base_linear - 2 * sm_slope * sm_constant +
            b_slope * sm_constant + b_constant * sm_slope;
        std::set<I> us;
        add_quadratic_points(us, substituted_quadratic, substituted_linear,
                             upper);
        for (I u : us) {
            const I t = sm_slope * u + sm_constant;
            if (t < 0) {
                throw std::runtime_error("negative upper boundary");
            }
            answer.emplace(static_cast<U>(u), static_cast<U>(t));
        }
    }
    return answer;
}

void record_candidate(
    U u, U t, const Polynomial &objective,
    const std::array<Polynomial, MAX_N> &left_poly,
    const std::array<Polynomial, MAX_N> &right_poly) {
    const I score = evaluate(objective, static_cast<I>(u), static_cast<I>(t));
    if (score < 0) {
        throw std::runtime_error("negative objective");
    }
    if (static_cast<U>(score) <= best) {
        return;
    }
    best = static_cast<U>(score);
    for (int i = 0; i < n - 1; ++i) {
        const I left = evaluate(left_poly[i], static_cast<I>(u),
                                static_cast<I>(t));
        const I right = evaluate(right_poly[i], static_cast<I>(u),
                                 static_cast<I>(t));
        if (left < 0 || right < 0) {
            throw std::runtime_error("negative instantiated coordinate");
        }
        best_left[i] = static_cast<U>(left);
        best_right[i] = static_cast<U>(right);
    }
}

void evaluate_orientation(bool middle_plus_one_left, Interval interval,
                          U a_total, I sm_slope, I sm_constant) {
    if (!interval.valid()) {
        return;
    }
    std::array<Polynomial, MAX_N> left_poly{};
    std::array<Polynomial, MAX_N> right_poly{};
    for (int i = 0; i < middle - 2; ++i) {
        left_poly[i] = constant_poly(static_cast<I>(left_size[i]));
        right_poly[i] = constant_poly(static_cast<I>(right_size[i]));
    }
    left_poly[middle - 2] = u_poly();
    right_poly[middle - 2] =
        subtract(constant_poly(static_cast<I>(a_total)), u_poly());
    left_poly[middle - 1] = t_poly();
    right_poly[middle - 1] =
        subtract(add(constant_poly(sm_constant),
                     multiply(constant_poly(sm_slope), u_poly())),
                 t_poly());

    for (int index = middle; index < n - 1; ++index) {
        Polynomial layer = convolution_poly(left_poly, right_poly, index);
        require_total_degree(layer, 2);
        const bool choose_left =
            index == middle ? middle_plus_one_left
                            : condition_value[index] > 0;
        if (choose_left) {
            left_poly[index] = layer;
        } else {
            right_poly[index] = layer;
        }
    }
    const Polynomial objective = convolution_poly(left_poly, right_poly, n - 1);
    require_total_degree(objective, 2);
    ++polynomial_checks;
    const auto candidates =
        critical_pairs(objective, sm_slope, sm_constant, interval);
    critical_pair_count += candidates.size();
    for (const auto &[u, t] : candidates) {
        const I sm_value = sm_slope * static_cast<I>(u) + sm_constant;
        if (sm_value < 0 || static_cast<I>(t) > sm_value) {
            throw std::runtime_error("candidate outside recurrence domain");
        }
        record_candidate(u, t, objective, left_poly, right_poly);
    }
}

void evaluate_two_layers() {
    ++prefix_count;
    const U a_total = convolution_at(middle - 2);

    left_size[middle - 2] = 0;
    right_size[middle - 2] = a_total;
    compute_condition(middle - 2);
    const I condition_constant = condition_value[middle];
    left_size[middle - 2] = a_total;
    right_size[middle - 2] = 0;
    compute_condition(middle - 2);
    if (condition_value[middle] !=
        condition_constant - 2 * static_cast<I>(a_total)) {
        throw std::runtime_error("upper condition is not affine with slope -2");
    }
    left_size[middle - 2] = 0;
    right_size[middle - 2] = a_total;
    ++condition_slope_checks;

    // s_m(u) is affine.  Its slope is y_1-x_1 and its constant is
    // obtained at u=0; compute the latter directly from the recurrence.
    const I sm_slope = static_cast<I>(right_size[0]) -
                       static_cast<I>(left_size[0]);
    const I sm_constant = static_cast<I>(convolution_at(middle - 1));
    const I signed_a = static_cast<I>(a_total);
    const I sm_at_a = sm_slope * signed_a + sm_constant;
    if (sm_constant < 0 || sm_at_a < 0) {
        throw std::runtime_error("negative middle total on endpoint");
    }

    const I leaf_sum =
        sm_slope * signed_a * (signed_a + 1) / 2 +
        (sm_constant + 1) * (signed_a + 1);
    if (leaf_sum < 0) {
        throw std::runtime_error("negative raw leaf count");
    }
    raw_two_layer_leaves += static_cast<U>(leaf_sum);

    const U before = critical_pair_count;
    const Interval full{0, signed_a};
    // Match the source fill convention: a positive condition chooses L;
    // zero or negative chooses R.  The exact condition is c-2u.
    Interval left_interval = restrict_ge(full, -2, condition_constant, 1);
    Interval right_interval = restrict_le(full, -2, condition_constant, 0);
    evaluate_orientation(true, left_interval, a_total, sm_slope, sm_constant);
    evaluate_orientation(false, right_interval, a_total, sm_slope, sm_constant);
    const U used = critical_pair_count - before;
    maximum_candidates_per_prefix = std::max(maximum_candidates_per_prefix, used);
    if (used > 16) {
        throw std::runtime_error("critical-set bound exceeded");
    }
}

void enumerate_prefixes(int current_level) {
    if (current_level == middle - 2) {
        evaluate_two_layers();
        return;
    }
    const U total = current_level == 0 ? 2 : convolution_at(current_level);
    const U minimum = current_level == 0 ? 1 : 0;
    U maximum = total;
    if (prefix_is_symmetric(current_level)) {
        maximum = total / 2;
    }
    for (U value = minimum; value <= maximum; ++value) {
        left_size[current_level] = value;
        right_size[current_level] = total - value;
        compute_condition(current_level);
        enumerate_prefixes(current_level + 1);
    }
}

void check_witness() {
    if (best_left[0] + best_right[0] != 2 || best_left[0] == 0 ||
        best_right[0] == 0) {
        throw std::runtime_error("invalid first witness layer");
    }
    for (int index = 1; index < n - 1; ++index) {
        U total = 0;
        for (int j = 0; j < index; ++j) {
            total += best_left[j] * best_right[index - 1 - j];
        }
        if (best_left[index] + best_right[index] != total) {
            throw std::runtime_error("witness recurrence failure");
        }
    }
    U score = 0;
    for (int j = 0; j < n - 1; ++j) {
        score += best_left[j] * best_right[n - 2 - j];
    }
    if (score != best) {
        throw std::runtime_error("witness score failure");
    }
}

}  // namespace

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "usage: two_layer_critical EVEN_N\n";
        return 2;
    }
    n = std::stoi(argv[1]);
    if (n < 8 || n > 30 || n % 2 != 0) {
        std::cerr << "EVEN_N must be even and satisfy 8 <= n <= 30\n";
        return 2;
    }
    middle = n / 2;
    for (int i = 0; i < MAX_N; ++i) {
        parameter[i][i] = 1;
    }

    const auto start = std::chrono::steady_clock::now();
    enumerate_prefixes(0);
    check_witness();
    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration<double>(stop - start).count();

    std::cout << "n " << n << "\n";
    std::cout << "best " << to_string_u128(best) << "\n";
    std::cout << "prefixes " << to_string_u128(prefix_count) << "\n";
    std::cout << "raw_two_layer_leaves "
              << to_string_u128(raw_two_layer_leaves) << "\n";
    std::cout << "critical_pairs " << to_string_u128(critical_pair_count)
              << "\n";
    std::cout << "polynomial_checks " << to_string_u128(polynomial_checks)
              << "\n";
    std::cout << "condition_slope_checks "
              << to_string_u128(condition_slope_checks) << "\n";
    std::cout << "maximum_candidates_per_prefix "
              << to_string_u128(maximum_candidates_per_prefix) << "\n";
    std::cout << "elapsed_seconds " << seconds << "\n";
    std::cout << "L";
    for (int i = 0; i < n - 1; ++i) {
        std::cout << ' ' << to_string_u128(best_left[i]);
    }
    std::cout << "\nR";
    for (int i = 0; i < n - 1; ++i) {
        std::cout << ' ' << to_string_u128(best_right[i]);
    }
    std::cout << '\n';
}
