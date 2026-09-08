#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {
constexpr int n = 21;
constexpr int prime = 1000003;
using Matrix = std::array<std::array<int, n>, n>;

int mod(long long x) {
    x %= prime;
    if (x < 0) x += prime;
    return static_cast<int>(x);
}

long long power_mod(long long a, long long e) {
    long long r = 1;
    while (e != 0) {
        if ((e & 1LL) != 0) r = r * a % prime;
        a = a * a % prime;
        e >>= 1;
    }
    return r;
}

bool is_prime(int value) {
    if (value < 2) return false;
    for (int divisor = 2; static_cast<long long>(divisor) * divisor <= value; ++divisor) {
        if (value % divisor == 0) return value == divisor;
    }
    return true;
}

Matrix multiply_mod(const Matrix& a, const Matrix& b) {
    Matrix c{};
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            if (a[i][k] == 0) continue;
            for (int j = 0; j < n; ++j) {
                c[i][j] = mod(c[i][j] + static_cast<long long>(a[i][k]) * b[k][j]);
            }
        }
    }
    return c;
}

bool equals_i_plus_sign_a(const Matrix& b, const int a[n][n], int sign) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (b[i][j] != (i == j ? 1 : sign * a[i][j])) return false;
        }
    }
    return true;
}

std::string first_row_bits(const Matrix& b) {
    std::string s;
    for (int j = 0; j < n; ++j) s += (b[0][j] == 1 ? '1' : '0');
    return s;
}
}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: enumerate core.edges\n";
        return 2;
    }
    if (!is_prime(prime)) {
        std::cerr << "configured modulus is not prime\n";
        return 2;
    }
    std::ifstream input(argv[1]);
    int nv = 0, declared_edges = 0;
    if (!(input >> nv >> declared_edges) || nv != n || declared_edges != 98) {
        std::cerr << "expected header 21 98\n";
        return 2;
    }
    bool graph[n][n]{};
    int u = 0, v = 0, read_edges = 0;
    while (input >> u >> v) {
        if (!(0 <= u && u < v && v < n) || graph[u][v]) {
            std::cerr << "malformed or duplicate edge\n";
            return 2;
        }
        graph[u][v] = graph[v][u] = true;
        ++read_edges;
    }
    if (!input.eof()) {
        std::cerr << "noninteger trailing input\n";
        return 2;
    }
    if (read_edges != declared_edges) {
        std::cerr << "edge count mismatch\n";
        return 2;
    }

    int a_integer[n][n]{};
    Matrix a{};
    for (int i = 0; i < n; ++i) {
        int outdegree = 0;
        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            const bool arrow = (i < j) ? graph[i][j] : !graph[i][j];
            a_integer[i][j] = arrow ? 1 : -1;
            a[i][j] = mod(a_integer[i][j]);
            outdegree += arrow;
        }
        if (outdegree != 10) {
            std::cerr << "core tournament is not regular\n";
            return 2;
        }
    }

    // powers[k] = A^k over F_prime.  K has rows e_0^T A^k.
    std::array<Matrix, n> powers{};
    for (int i = 0; i < n; ++i) powers[0][i][i] = 1;
    for (int k = 1; k < n; ++k) powers[k] = multiply_mod(powers[k - 1], a);

    int augmented[n][2 * n]{};
    for (int k = 0; k < n; ++k) {
        for (int j = 0; j < n; ++j) augmented[k][j] = powers[k][0][j];
        augmented[k][n + k] = 1;
    }
    int rank = 0;
    for (int column = 0; column < n; ++column) {
        int pivot = rank;
        while (pivot < n && augmented[pivot][column] == 0) ++pivot;
        if (pivot == n) {
            std::cerr << "Krylov matrix is singular modulo " << prime << "\n";
            return 2;
        }
        std::swap(augmented[pivot], augmented[rank]);
        const long long inverse = power_mod(augmented[rank][column], prime - 2);
        for (int j = 0; j < 2 * n; ++j) {
            augmented[rank][j] = mod(static_cast<long long>(augmented[rank][j]) * inverse);
        }
        for (int i = 0; i < n; ++i) {
            if (i == rank || augmented[i][column] == 0) continue;
            const int factor = augmented[i][column];
            for (int j = 0; j < 2 * n; ++j) {
                augmented[i][j] = mod(augmented[i][j] -
                    static_cast<long long>(factor) * augmented[rank][j]);
            }
        }
        ++rank;
    }
    int inverse_k[n][n]{};
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) inverse_k[i][k] = augmented[i][n + k];
    }

    // If b=e_0^T B and AB=BA, then K B has row k equal to b A^k.
    // Thus B_ij = sum_t reconstruction[i][j][t] b_t modulo prime.
    static int reconstruction[n][n][n];
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            for (int t = 0; t < n; ++t) {
                long long value = 0;
                for (int k = 0; k < n; ++k) {
                    value += static_cast<long long>(inverse_k[i][k]) * powers[k][t][j];
                }
                reconstruction[i][j][t] = mod(value);
            }
        }
    }
    for (int j = 0; j < n; ++j) {
        for (int t = 0; t < n; ++t) {
            if (reconstruction[0][j][t] != (j == t ? 1 : 0)) {
                std::cerr << "first-row reconstruction failure\n";
                return 2;
            }
        }
    }

    std::uint64_t tested = 0;
    std::uint64_t modular_sign = 0;
    std::vector<Matrix> exact_candidates;
    std::vector<int> gram_mismatches;
    int gram_valid = 0;

    for (std::uint32_t mask = 0; mask < (1U << n); ++mask) {
        if (std::popcount(mask) != 11) continue;
        ++tested;
        int b[n];
        Matrix candidate{};
        for (int t = 0; t < n; ++t) {
            b[t] = ((mask >> t) & 1U) != 0 ? 1 : prime - 1;
            candidate[0][t] = ((mask >> t) & 1U) != 0 ? 1 : -1;
        }
        bool ok = true;
        for (int i = 1; i < n && ok; ++i) {
            for (int j = 0; j < n; ++j) {
                long long value = 0;
                for (int t = 0; t < n; ++t) {
                    value += static_cast<long long>(reconstruction[i][j][t]) * b[t];
                }
                const int residue = mod(value);
                if (residue == 1) candidate[i][j] = 1;
                else if (residue == prime - 1) candidate[i][j] = -1;
                else {
                    ok = false;
                    break;
                }
            }
        }
        if (!ok) continue;
        ++modular_sign;

        // Eliminate any modular false positive by exact integer checks.
        for (int i = 0; i < n && ok; ++i) {
            for (int j = 0; j < n; ++j) {
                int ab = 0, ba = 0;
                for (int k = 0; k < n; ++k) {
                    ab += a_integer[i][k] * candidate[k][j];
                    ba += candidate[i][k] * a_integer[k][j];
                }
                if (ab != ba) {
                    ok = false;
                    break;
                }
            }
        }
        if (!ok) continue;
        for (int i = 0; i < n && ok; ++i) {
            int row_sum = 0, column_sum = 0;
            for (int j = 0; j < n; ++j) {
                row_sum += candidate[i][j];
                column_sum += candidate[j][i];
            }
            if (row_sum != 1 || column_sum != 1) ok = false;
        }
        if (!ok) continue;

        int mismatches = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                int bbt = 0, aat = 0;
                for (int k = 0; k < n; ++k) {
                    bbt += candidate[i][k] * candidate[j][k];
                    aat += a_integer[i][k] * a_integer[j][k];
                }
                const int required = (i == j ? 43 : 0) - 2 - aat;
                if (bbt != required) ++mismatches;
            }
        }
        if (mismatches == 0) ++gram_valid;
        exact_candidates.push_back(candidate);
        gram_mismatches.push_back(mismatches);
    }

    std::cout << "core_vertices " << n << "\n";
    std::cout << "core_forward_edges " << declared_edges << "\n";
    std::cout << "core_tournament_outdegree 10\n";
    std::cout << "prime " << prime << "\n";
    std::cout << "krylov_rank " << rank << "\n";
    std::cout << "first_rows_tested " << tested << "\n";
    std::cout << "modular_sign_matrices " << modular_sign << "\n";
    std::cout << "exact_commuting_sign_matrices " << exact_candidates.size() << "\n";
    for (std::size_t i = 0; i < exact_candidates.size(); ++i) {
        std::string kind = "other";
        if (equals_i_plus_sign_a(exact_candidates[i], a_integer, 1)) kind = "I_plus_A";
        if (equals_i_plus_sign_a(exact_candidates[i], a_integer, -1)) kind = "I_minus_A";
        std::cout << "candidate " << i << " first_row " << first_row_bits(exact_candidates[i])
                  << " kind " << kind << " gram_mismatch_ordered_entries "
                  << gram_mismatches[i] << "\n";
    }
    std::cout << "gram_valid_matrices " << gram_valid << "\n";
    std::cout << "status EXCLUDED_REVERSE_CORE_DRT43_COMPLETION\n";
    return gram_valid == 0 ? 0 : 1;
}
