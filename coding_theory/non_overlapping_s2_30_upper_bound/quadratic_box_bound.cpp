#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

using U = unsigned __int128;
using I = __int128;

namespace {

constexpr int MAX_N = 64;
constexpr int MAX_FREE = 8;

struct Poly {
    I constant = 0;
    std::array<I, MAX_FREE> linear{};
    std::array<std::array<I, MAX_FREE>, MAX_FREE> quadratic{};
    int degree = 0;
};

int n;
int middle;
int free_layers;
int start_level;
int start_index;
std::array<U, MAX_N> left_size{};
std::array<U, MAX_N> right_size{};
std::array<I, MAX_N> condition_value{};
std::array<int, MAX_N> condition_side{};
std::array<std::array<I, MAX_N>, MAX_N> parameter{};

U prefix_count = 0;
U prefix_seen = 0;
U polynomial_count = 0;
I global_upper = -1;
std::array<U, MAX_N> maximizing_prefix_left{};
std::array<U, MAX_N> maximizing_prefix_right{};
std::array<I, MAX_FREE> maximizing_highs{};
unsigned maximizing_mask = 0;
Poly maximizing_poly{};
U positive_cross_terms = 0;
unsigned shard_id = 0;
unsigned shard_count = 1;

std::string to_string_u128(U value) {
    if (value == 0) return "0";
    std::string out;
    while (value) {
        out.push_back(static_cast<char>('0' + value % 10));
        value /= 10;
    }
    std::reverse(out.begin(), out.end());
    return out;
}

std::string to_string_i128(I value) {
    if (value < 0) {
        std::string out = "-";
        out += to_string_u128(static_cast<U>(-value));
        return out;
    }
    return to_string_u128(static_cast<U>(value));
}

Poly constant_poly(I value) {
    Poly out;
    out.constant = value;
    return out;
}

Poly variable_poly(int variable) {
    Poly out;
    out.linear[variable] = 1;
    out.degree = 1;
    return out;
}

Poly subtract(const Poly &a, const Poly &b) {
    Poly out;
    out.constant = a.constant - b.constant;
    out.degree = std::max(a.degree, b.degree);
    for (int i = 0; i < free_layers; ++i) {
        out.linear[i] = a.linear[i] - b.linear[i];
        for (int j = i; j < free_layers; ++j) {
            out.quadratic[i][j] = a.quadratic[i][j] - b.quadratic[i][j];
        }
    }
    return out;
}

void add_inplace(Poly &a, const Poly &b) {
    a.constant += b.constant;
    a.degree = std::max(a.degree, b.degree);
    for (int i = 0; i < free_layers; ++i) {
        a.linear[i] += b.linear[i];
        for (int j = i; j < free_layers; ++j) {
            a.quadratic[i][j] += b.quadratic[i][j];
        }
    }
}

Poly multiply(const Poly &a, const Poly &b) {
    if (a.degree + b.degree > 2) {
        throw std::runtime_error("polynomial degree exceeds two");
    }
    Poly out;
    out.degree = a.degree + b.degree;
    out.constant = a.constant * b.constant;
    for (int i = 0; i < free_layers; ++i) {
        out.linear[i] = a.constant * b.linear[i] +
                        b.constant * a.linear[i];
        out.quadratic[i][i] =
            a.constant * b.quadratic[i][i] +
            b.constant * a.quadratic[i][i] +
            a.linear[i] * b.linear[i];
        for (int j = i + 1; j < free_layers; ++j) {
            out.quadratic[i][j] =
                a.constant * b.quadratic[i][j] +
                b.constant * a.quadratic[i][j] +
                a.linear[i] * b.linear[j] +
                a.linear[j] * b.linear[i];
        }
    }
    return out;
}

Poly convolution_poly(const std::array<Poly, MAX_N> &left,
                      const std::array<Poly, MAX_N> &right, int index) {
    Poly out;
    for (int j = 0; j < index; ++j) {
        add_inplace(out, multiply(left[j], right[index - 1 - j]));
    }
    return out;
}

U convolution_at(int index) {
    U out = 0;
    for (int j = 0; j < index; ++j) {
        out += left_size[j] * right_size[index - 1 - j];
    }
    return out;
}

bool prefix_is_symmetric(int current_level) {
    for (int i = 0; i < current_level; ++i) {
        if (left_size[i] != right_size[i]) return false;
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

I affine_box_upper(const Poly &poly, const std::array<I, MAX_FREE> &highs,
                   int variables) {
    if (poly.degree > 1) {
        throw std::runtime_error("free-layer total is not affine");
    }
    I out = poly.constant;
    for (int i = 0; i < variables; ++i) {
        if (poly.linear[i] > 0) out += poly.linear[i] * highs[i];
    }
    if (out < 0) {
        throw std::runtime_error("negative affine box upper bound");
    }
    return out;
}

I floor_div(I numerator, I denominator) {
    if (denominator == 0) throw std::runtime_error("division by zero");
    I quotient = numerator / denominator;
    const I remainder = numerator % denominator;
    if (remainder != 0 && ((remainder > 0) != (denominator > 0))) --quotient;
    return quotient;
}

I univariate_integer_max(I quadratic, I linear, I high) {
    if (high < 0) throw std::runtime_error("negative box high");
    I best = std::max<I>(0, quadratic * high * high + linear * high);
    if (quadratic < 0) {
        const I below = floor_div(-linear, 2 * quadratic);
        for (I point : {below, below + 1}) {
            point = std::max<I>(0, std::min<I>(high, point));
            best = std::max(best, quadratic * point * point + linear * point);
        }
    }
    return best;
}

I box_upper(const Poly &poly, const std::array<I, MAX_FREE> &highs) {
    if (poly.degree > 2) throw std::runtime_error("objective degree exceeds two");
    I out = poly.constant;
    for (int i = 0; i < free_layers; ++i) {
        out += univariate_integer_max(poly.quadratic[i][i],
                                      poly.linear[i], highs[i]);
        for (int j = i + 1; j < free_layers; ++j) {
            if (poly.quadratic[i][j] > 0) {
                out += poly.quadratic[i][j] * highs[i] * highs[j];
                ++positive_cross_terms;
            }
        }
    }
    return out;
}

void evaluate_prefix() {
    const U ordinal = prefix_seen++;
    if (ordinal % static_cast<U>(shard_count) != static_cast<U>(shard_id)) {
        return;
    }
    ++prefix_count;
    std::array<Poly, MAX_N> base_left{};
    std::array<Poly, MAX_N> base_right{};
    for (int i = 0; i < start_index; ++i) {
        base_left[i] = constant_poly(static_cast<I>(left_size[i]));
        base_right[i] = constant_poly(static_cast<I>(right_size[i]));
    }

    std::array<I, MAX_FREE> highs{};
    for (int variable = 0; variable < free_layers; ++variable) {
        const int index = start_index + variable;
        const Poly total = convolution_poly(base_left, base_right, index);
        if (total.degree > 1) {
            throw std::runtime_error("free total is not affine");
        }
        highs[variable] = affine_box_upper(total, highs, variable);
        base_left[index] = variable_poly(variable);
        base_right[index] = subtract(total, base_left[index]);
    }

    const unsigned orientation_count = 1U << (free_layers - 1);
    for (unsigned mask = 0; mask < orientation_count; ++mask) {
        auto left = base_left;
        auto right = base_right;
        for (int index = middle; index < n - 1; ++index) {
            const Poly total = convolution_poly(left, right, index);
            bool choose_left;
            const int unknown_bit = index - middle;
            if (unknown_bit < free_layers - 1) {
                choose_left = ((mask >> unknown_bit) & 1U) != 0;
            } else {
                choose_left = condition_value[index] > 0;
            }
            if (choose_left) left[index] = total;
            else right[index] = total;
        }
        const Poly objective = convolution_poly(left, right, n - 1);
        ++polynomial_count;
        const I upper = box_upper(objective, highs);
        if (upper > global_upper) {
            global_upper = upper;
            maximizing_mask = mask;
            maximizing_highs = highs;
            maximizing_poly = objective;
            maximizing_prefix_left = left_size;
            maximizing_prefix_right = right_size;
        }
    }
}

void enumerate_prefixes(int current_level) {
    if (current_level == start_index) {
        evaluate_prefix();
        return;
    }
    const U total = current_level == 0 ? 2 : convolution_at(current_level);
    const U minimum = current_level == 0 ? 1 : 0;
    U maximum = total;
    if (prefix_is_symmetric(current_level)) maximum = total / 2;
    for (U value = minimum; value <= maximum; ++value) {
        left_size[current_level] = value;
        right_size[current_level] = total - value;
        compute_condition(current_level);
        enumerate_prefixes(current_level + 1);
    }
}

}  // namespace

int main(int argc, char **argv) {
    if (argc != 3 && argc != 5) {
        std::cerr << "usage: quadratic_box_bound EVEN_N FREE_LAYERS [SHARD SHARDS]\n";
        return 2;
    }
    n = std::stoi(argv[1]);
    free_layers = std::stoi(argv[2]);
    if (argc == 5) {
        shard_id = static_cast<unsigned>(std::stoul(argv[3]));
        shard_count = static_cast<unsigned>(std::stoul(argv[4]));
    }
    if (n < 8 || n > 30 || n % 2 != 0 || free_layers < 1 ||
        free_layers > MAX_FREE) {
        std::cerr << "invalid even length or free-layer count\n";
        return 2;
    }
    if (shard_count == 0 || shard_id >= shard_count) {
        std::cerr << "require 0 <= SHARD < SHARDS\n";
        return 2;
    }
    middle = n / 2;
    start_level = middle - free_layers + 1;
    start_index = start_level - 1;
    if (start_level < 2 || 3 * start_level <= n) {
        std::cerr << "quadratic certificate requires 3*START_LEVEL > EVEN_N\n";
        return 2;
    }
    for (int i = 0; i < MAX_N; ++i) parameter[i][i] = 1;

    const auto begin = std::chrono::steady_clock::now();
    enumerate_prefixes(0);
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - begin).count();

    std::cout << "n " << n << "\n";
    std::cout << "free_layers " << free_layers << "\n";
    std::cout << "start_level " << start_level << "\n";
    std::cout << "upper_bound " << to_string_i128(global_upper) << "\n";
    std::cout << "shard " << shard_id << "\n";
    std::cout << "shards " << shard_count << "\n";
    std::cout << "prefixes_seen " << to_string_u128(prefix_seen) << "\n";
    std::cout << "prefixes_evaluated " << to_string_u128(prefix_count) << "\n";
    std::cout << "orientation_polynomials " << to_string_u128(polynomial_count) << "\n";
    std::cout << "positive_cross_terms " << to_string_u128(positive_cross_terms) << "\n";
    std::cout << "elapsed_seconds " << seconds << "\n";
    std::cout << "maximizing_mask " << maximizing_mask << "\n";
    std::cout << "prefix_L";
    for (int i = 0; i < start_index; ++i) std::cout << ' ' << to_string_u128(maximizing_prefix_left[i]);
    std::cout << "\nprefix_R";
    for (int i = 0; i < start_index; ++i) std::cout << ' ' << to_string_u128(maximizing_prefix_right[i]);
    std::cout << "\nhighs";
    for (int i = 0; i < free_layers; ++i) std::cout << ' ' << to_string_i128(maximizing_highs[i]);
    std::cout << "\nconstant " << to_string_i128(maximizing_poly.constant);
    std::cout << "\nlinear";
    for (int i = 0; i < free_layers; ++i) std::cout << ' ' << to_string_i128(maximizing_poly.linear[i]);
    std::cout << "\nquadratic";
    for (int i = 0; i < free_layers; ++i) {
        for (int j = i; j < free_layers; ++j) {
            std::cout << ' ' << to_string_i128(maximizing_poly.quadratic[i][j]);
        }
    }
    std::cout << '\n';
}
