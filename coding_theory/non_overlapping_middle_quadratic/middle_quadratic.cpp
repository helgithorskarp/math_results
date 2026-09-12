#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using U = unsigned __int128;
using I = __int128;

namespace {

constexpr int MAX_N = 64;

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
U original_middle_leaves = 0;
U vertex_candidates = 0;
U quadratic_leading_checks = 0;

struct Affine {
    I slope;
    I constant;
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

std::string to_string_i128(I value) {
    if (value < 0) {
        return "-" + to_string_u128(static_cast<U>(-value));
    }
    return to_string_u128(static_cast<U>(value));
}

U convolution_at(int zero_based_index) {
    U value = 0;
    for (int j = 0; j < zero_based_index; ++j) {
        value += left_size[j] * right_size[zero_based_index - 1 - j];
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

// This is an index-faithful reimplementation of Definition 14 and the
// condition computation used in the source algorithm.  Entries at larger
// condition indices have already been determined when this is called.
void compute_condition(int index) {
    for (int j = 0; j < index; ++j) {
        for (int k = j - 1; k >= 0; --k) {
            parameter[j][k] = 0;
            for (int l = k; l < j; ++l) {
                const int side = condition_side[n - index + l - 1];
                const U factor = side ? right_size[j - l - 1]
                                      : left_size[j - l - 1];
                parameter[j][k] += static_cast<I>(factor) * parameter[l][k];
            }
        }
    }

    const int condition_index = n - index - 2;
    I value = static_cast<I>(right_size[index]) -
              static_cast<I>(left_size[index]);
    for (int j = 0; j < index; ++j) {
        I inner = 0;
        for (int l = 0; l <= j; ++l) {
            inner += parameter[j][l] *
                     (static_cast<I>(right_size[l]) -
                      static_cast<I>(left_size[l]));
        }
        const int side = condition_side[n - index + j - 1];
        const U factor = side ? right_size[index - j - 1]
                              : left_size[index - j - 1];
        value += inner * static_cast<I>(factor);
    }
    condition_value[condition_index] = value;
    condition_side[condition_index] = (value >= 0) ? 1 : 0;
}

void record_if_better(U score, U middle_left,
                      const std::array<Affine, MAX_N> &left_affine,
                      const std::array<Affine, MAX_N> &right_affine) {
    if (score > best) {
        best = score;
        for (int i = 0; i < n - 1; ++i) {
            const I left_value = left_affine[i].slope *
                                     static_cast<I>(middle_left) +
                                 left_affine[i].constant;
            const I right_value = right_affine[i].slope *
                                      static_cast<I>(middle_left) +
                                  right_affine[i].constant;
            if (left_value < 0 || right_value < 0) {
                throw std::runtime_error("negative instantiated layer");
            }
            best_left[i] = static_cast<U>(left_value);
            best_right[i] = static_cast<U>(right_value);
        }
    }
}

void evaluate_middle_quadratic() {
    ++prefix_count;
    const U total = convolution_at(middle - 1);
    original_middle_leaves += total + 1;

    std::array<Affine, MAX_N> left_affine{};
    std::array<Affine, MAX_N> right_affine{};
    for (int i = 0; i < middle - 1; ++i) {
        left_affine[i] = {0, static_cast<I>(left_size[i])};
        right_affine[i] = {0, static_cast<I>(right_size[i])};
    }
    left_affine[middle - 1] = {1, 0};
    right_affine[middle - 1] = {-1, static_cast<I>(total)};

    for (int index = middle; index < n - 1; ++index) {
        I quadratic = 0;
        Affine layer{0, 0};
        for (int j = 0; j < index; ++j) {
            const int k = index - 1 - j;
            quadratic += left_affine[j].slope * right_affine[k].slope;
            layer.slope += left_affine[j].slope * right_affine[k].constant +
                           left_affine[j].constant * right_affine[k].slope;
            layer.constant +=
                left_affine[j].constant * right_affine[k].constant;
        }
        if (quadratic != 0) {
            throw std::runtime_error("upper layer is not affine");
        }
        // Match the published implementation's harmless tie convention:
        // positive condition chooses L, zero or negative chooses R.
        if (condition_value[index] > 0) {
            left_affine[index] = layer;
        } else {
            right_affine[index] = layer;
        }
    }

    I quadratic_coefficient = 0;
    I linear_coefficient = 0;
    I constant_coefficient = 0;
    for (int j = 0; j < n - 1; ++j) {
        const int k = n - 2 - j;
        quadratic_coefficient +=
            left_affine[j].slope * right_affine[k].slope;
        linear_coefficient +=
            left_affine[j].slope * right_affine[k].constant +
            left_affine[j].constant * right_affine[k].slope;
        constant_coefficient +=
            left_affine[j].constant * right_affine[k].constant;
    }
    if (quadratic_coefficient != -1) {
        throw std::runtime_error("quadratic leading coefficient is not -1: " +
                                 to_string_i128(quadratic_coefficient));
    }
    ++quadratic_leading_checks;

    std::set<U> candidates;
    const I signed_total = static_cast<I>(total);
    if (linear_coefficient <= 0) {
        candidates.insert(0);
    } else if (linear_coefficient >= 2 * signed_total) {
        candidates.insert(total);
    } else {
        const U floor_vertex = static_cast<U>(linear_coefficient / 2);
        candidates.insert(floor_vertex);
        candidates.insert(floor_vertex + (linear_coefficient % 2 != 0));
    }

    vertex_candidates += candidates.size();
    for (U t : candidates) {
        const I score_formula = constant_coefficient +
                                linear_coefficient * static_cast<I>(t) -
                                static_cast<I>(t) * static_cast<I>(t);
        if (score_formula < 0) {
            throw std::runtime_error("negative score from quadratic");
        }
        record_if_better(static_cast<U>(score_formula), t, left_affine,
                         right_affine);
    }
}

void enumerate_prefixes(int current_level) {
    if (current_level == middle - 1) {
        evaluate_middle_quadratic();
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

}  // namespace (internal implementation)

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "usage: middle_quadratic EVEN_N\n";
        return 2;
    }
    n = std::stoi(argv[1]);
    if (n < 4 || n > 30 || n % 2 != 0) {
        std::cerr << "EVEN_N must be even and satisfy 4 <= n <= 30\n";
        return 2;
    }
    middle = n / 2;
    for (int i = 0; i < MAX_N; ++i) {
        parameter[i][i] = 1;
    }

    const auto start = std::chrono::steady_clock::now();
    enumerate_prefixes(0);
    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration<double>(stop - start).count();

    std::cout << "n " << n << "\n";
    std::cout << "best " << to_string_u128(best) << "\n";
    std::cout << "prefixes " << to_string_u128(prefix_count) << "\n";
    std::cout << "original_middle_leaves "
              << to_string_u128(original_middle_leaves) << "\n";
    std::cout << "vertex_candidates " << to_string_u128(vertex_candidates)
              << "\n";
    std::cout << "quadratic_leading_checks "
              << to_string_u128(quadratic_leading_checks)
              << "\n";
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
