#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint64_t;

struct Graph {
  int n{};
  std::vector<Mask> adjacency;
};

Graph decode_graph6(const std::string& record) {
  std::string data = record;
  constexpr const char* header = ">>graph6<<";
  if (data.rfind(header, 0) == 0) {
    data.erase(0, std::char_traits<char>::length(header));
  }
  if (data.empty()) {
    throw std::runtime_error("empty graph6 record");
  }
  const int n = static_cast<unsigned char>(data[0]) - 63;
  if (n < 1 || n > 62) {
    throw std::runtime_error("only one-byte graph6 orders 1..62 are supported");
  }
  const std::size_t required_bits = static_cast<std::size_t>(n) * (n - 1) / 2;
  if ((data.size() - 1) * 6 < required_bits) {
    throw std::runtime_error("truncated graph6 record");
  }
  std::vector<Mask> adjacency(static_cast<std::size_t>(n), 0);
  std::size_t bit_position = 0;
  for (int column = 1; column < n; ++column) {
    for (int row = 0; row < column; ++row, ++bit_position) {
      const unsigned char byte = static_cast<unsigned char>(data[1 + bit_position / 6]);
      if (byte < 63 || byte > 126) {
        throw std::runtime_error("invalid graph6 byte");
      }
      const unsigned value = byte - 63;
      const unsigned shift = 5U - static_cast<unsigned>(bit_position % 6);
      if (((value >> shift) & 1U) != 0U) {
        adjacency[static_cast<std::size_t>(row)] |= Mask{1} << column;
        adjacency[static_cast<std::size_t>(column)] |= Mask{1} << row;
      }
    }
  }
  return Graph{n, std::move(adjacency)};
}

class FullFeedbackGame {
 public:
  explicit FullFeedbackGame(Graph graph)
      : n_(graph.n),
        adjacency_(std::move(graph.adjacency)),
        full_((Mask{1} << n_) - 1),
        closed_(static_cast<std::size_t>(n_)),
        distances_(static_cast<std::size_t>(n_), std::vector<int>(static_cast<std::size_t>(n_), -1)),
        responses_(static_cast<std::size_t>(n_), std::vector<Mask>(static_cast<std::size_t>(n_), 0)) {
    for (int v = 0; v < n_; ++v) {
      closed_[static_cast<std::size_t>(v)] = adjacency_[static_cast<std::size_t>(v)] | (Mask{1} << v);
    }
    compute_distances();
    compute_responses();
  }

  [[nodiscard]] int n() const { return n_; }
  [[nodiscard]] Mask full() const { return full_; }

  struct Result {
    bool cops_win{};
    int full_rank{-1};
    std::size_t winning_beliefs{};
    bool complete{true};
  };

  struct DescentResult {
    bool holds{};
    Mask counterexample{};
    std::size_t checked_states{};
  };

  // Check a sufficient condition for two-cop localization.  Every state
  // arising after recontamination has the form N[X].  The condition asks for
  // an action whose every unresolved successor is either smaller than the
  // current state or resolvable in one further probing phase.
  DescentResult check_response_fiber_descent() const {
    if (n_ > 20) {
      throw std::runtime_error("descent checking is limited to orders at most 20");
    }
    const auto partitions = make_partitions(2);
    std::vector<Mask> closure(static_cast<std::size_t>(full_) + 1, 0);
    std::vector<bool> is_state(static_cast<std::size_t>(full_) + 1, false);
    for (Mask mask = 1; mask <= full_; ++mask) {
      const Mask bit = mask & (~mask + 1);
      const int vertex = std::countr_zero(bit);
      closure[mask] = closure[mask ^ bit] | closed_[static_cast<std::size_t>(vertex)];
      is_state[closure[mask]] = true;
    }

    std::vector<std::int8_t> resolving_cache(static_cast<std::size_t>(full_) + 1, -1);
    const auto is_resolvable = [&](Mask belief) {
      auto& cached = resolving_cache[belief];
      if (cached < 0) {
        const bool answer = std::ranges::any_of(partitions, [&](const auto& classes) {
          return std::ranges::all_of(classes, [&](Mask class_mask) {
            return std::popcount(belief & class_mask) <= 1;
          });
        });
        cached = static_cast<std::int8_t>(answer ? 1 : 0);
      }
      return cached != 0;
    };

    std::size_t checked_states = 0;
    for (Mask belief = 1; belief <= full_; ++belief) {
      if (!is_state[belief] || std::popcount(belief) <= 1) {
        continue;
      }
      ++checked_states;
      const int belief_size = std::popcount(belief);
      const bool has_descent_action = std::ranges::any_of(partitions, [&](const auto& classes) {
        return std::ranges::all_of(classes, [&](Mask class_mask) {
          const Mask cell = belief & class_mask;
          if (std::popcount(cell) <= 1) {
            return true;
          }
          const Mask successor = closure[cell];
          return std::popcount(successor) < belief_size || is_resolvable(successor);
        });
      });
      if (!has_descent_action) {
        return DescentResult{false, belief, checked_states};
      }
    }
    return DescentResult{true, 0, checked_states};
  }

  Result solve(int cops, int round_limit = 0) const {
    const auto partitions = make_partitions(cops);
    if (n_ == 1) {
      return Result{true, 0, 1};
    }
    for (const auto& classes : partitions) {
      if (std::ranges::all_of(classes, [](Mask class_mask) { return std::popcount(class_mask) == 1; })) {
        // A partition that distinguishes V also distinguishes every belief subset.
        return Result{true, 1, static_cast<std::size_t>(full_)};
      }
    }
    for (const auto& first_classes : partitions) {
      bool first_action_succeeds = true;
      for (const Mask cell : first_classes) {
        if (std::popcount(cell) <= 1) {
          continue;
        }
        Mask recontaminated = 0;
        Mask remaining = cell;
        while (remaining != 0) {
          const Mask bit = remaining & (~remaining + 1);
          remaining ^= bit;
          recontaminated |= closed_[static_cast<std::size_t>(std::countr_zero(bit))];
        }
        const bool has_resolving_action = std::ranges::any_of(partitions, [&](const auto& second_classes) {
          return std::ranges::all_of(second_classes, [&](Mask class_mask) {
            return std::popcount(recontaminated & class_mask) <= 1;
          });
        });
        if (!has_resolving_action) {
          first_action_succeeds = false;
          break;
        }
      }
      if (first_action_succeeds) {
        // The full belief is won in two rounds.  The total number of winning
        // sub-beliefs is not enumerated along this fast path.
        return Result{true, 2, 0};
      }
    }
    if (round_limit >= 3) {
      std::unordered_map<Mask, Mask> closure_cache;
      const auto closure_of = [&](Mask cell) {
        if (const auto found = closure_cache.find(cell); found != closure_cache.end()) {
          return found->second;
        }
        Mask recontaminated = 0;
        Mask remaining = cell;
        while (remaining != 0) {
          const Mask bit = remaining & (~remaining + 1);
          remaining ^= bit;
          recontaminated |= closed_[static_cast<std::size_t>(std::countr_zero(bit))];
        }
        closure_cache.emplace(cell, recontaminated);
        return recontaminated;
      };
      std::vector<std::unordered_map<Mask, bool>> memo(static_cast<std::size_t>(round_limit) + 1);
      std::function<bool(Mask, int)> wins_within = [&](Mask belief, int rounds) -> bool {
        if (std::popcount(belief) <= 1) {
          return true;
        }
        if (rounds == 0) {
          return false;
        }
        auto& layer = memo[static_cast<std::size_t>(rounds)];
        if (const auto found = layer.find(belief); found != layer.end()) {
          return found->second;
        }
        for (const auto& classes : partitions) {
          bool succeeds = true;
          for (const Mask class_mask : classes) {
            const Mask cell = belief & class_mask;
            if (std::popcount(cell) <= 1) {
              continue;
            }
            if (!wins_within(closure_of(cell), rounds - 1)) {
              succeeds = false;
              break;
            }
          }
          if (succeeds) {
            layer.emplace(belief, true);
            return true;
          }
        }
        layer.emplace(belief, false);
        return false;
      };
      for (int rounds = 3; rounds <= round_limit; ++rounds) {
        if (wins_within(full_, rounds)) {
          return Result{true, rounds, 0};
        }
      }
    }
    if (round_limit > 0) {
      return Result{false, -round_limit, 0, false};
    }
    if (n_ > 24) {
      throw std::runtime_error("a graph of two-round rank above two exceeds the configured state-space limit");
    }
    std::vector<Mask> closure(static_cast<std::size_t>(full_) + 1, 0);
    for (Mask mask = 1; mask <= full_; ++mask) {
      const Mask bit = mask & (~mask + 1);
      const int v = std::countr_zero(bit);
      closure[mask] = closure[mask ^ bit] | closed_[static_cast<std::size_t>(v)];
    }
    std::vector<std::int16_t> rank(static_cast<std::size_t>(full_) + 1, -1);
    for (int v = 0; v < n_; ++v) {
      rank[Mask{1} << v] = 0;
    }
    std::size_t winning = static_cast<std::size_t>(n_);
    if (rank[full_] >= 0) {
      return Result{true, 0, winning};
    }
    for (int next_rank = 1;; ++next_rank) {
      std::vector<Mask> additions;
      for (Mask belief = 1; belief <= full_; ++belief) {
        if (rank[belief] >= 0) {
          continue;
        }
        for (const auto& classes : partitions) {
          bool succeeds = true;
          for (const Mask class_mask : classes) {
            const Mask cell = belief & class_mask;
            if (std::popcount(cell) <= 1) {
              continue;
            }
            if (rank[closure[cell]] < 0) {
              succeeds = false;
              break;
            }
          }
          if (succeeds) {
            additions.push_back(belief);
            break;
          }
        }
      }
      if (additions.empty()) {
        return Result{false, -1, winning};
      }
      for (const Mask belief : additions) {
        rank[belief] = static_cast<std::int16_t>(next_rank);
      }
      winning += additions.size();
      if (rank[full_] >= 0) {
        return Result{true, rank[full_], winning};
      }
    }
  }

 private:
  int n_;
  std::vector<Mask> adjacency_;
  Mask full_;
  std::vector<Mask> closed_;
  std::vector<std::vector<int>> distances_;
  std::vector<std::vector<Mask>> responses_;

  void compute_distances() {
    for (int source = 0; source < n_; ++source) {
      auto& distance = distances_[static_cast<std::size_t>(source)];
      std::queue<int> queue;
      distance[static_cast<std::size_t>(source)] = 0;
      queue.push(source);
      while (!queue.empty()) {
        const int v = queue.front();
        queue.pop();
        Mask unseen = adjacency_[static_cast<std::size_t>(v)];
        while (unseen != 0) {
          const Mask bit = unseen & (~unseen + 1);
          unseen ^= bit;
          const int w = std::countr_zero(bit);
          if (distance[static_cast<std::size_t>(w)] < 0) {
            distance[static_cast<std::size_t>(w)] = distance[static_cast<std::size_t>(v)] + 1;
            queue.push(w);
          }
        }
      }
      if (std::ranges::find(distance, -1) != distance.end()) {
        throw std::runtime_error("graph must be connected");
      }
    }
  }

  void compute_responses() {
    for (int probe = 0; probe < n_; ++probe) {
      for (int robber = 0; robber < n_; ++robber) {
        if (probe == robber) {
          responses_[static_cast<std::size_t>(probe)][static_cast<std::size_t>(robber)] = Mask{1} << probe;
          continue;
        }
        Mask response = 0;
        Mask neighbors = adjacency_[static_cast<std::size_t>(probe)];
        const int target_distance = distances_[static_cast<std::size_t>(probe)][static_cast<std::size_t>(robber)] - 1;
        while (neighbors != 0) {
          const Mask bit = neighbors & (~neighbors + 1);
          neighbors ^= bit;
          const int neighbor = std::countr_zero(bit);
          if (distances_[static_cast<std::size_t>(neighbor)][static_cast<std::size_t>(robber)] == target_distance) {
            response |= bit;
          }
        }
        if (response == 0) {
          throw std::logic_error("empty full-feedback response");
        }
        responses_[static_cast<std::size_t>(probe)][static_cast<std::size_t>(robber)] = response;
      }
    }
  }

  [[nodiscard]] std::vector<std::vector<Mask>> make_partitions(int cops) const {
    if (cops < 1) {
      throw std::invalid_argument("number of cops must be positive");
    }
    std::vector<std::vector<int>> actions;
    for (int p = 0; p < n_; ++p) {
      actions.push_back({p});
    }
    if (cops >= 2 && n_ >= 2) {
      for (int p = 0; p < n_; ++p) {
        for (int q = p + 1; q < n_; ++q) {
          actions.push_back({p, q});
        }
      }
    }
    if (cops >= 3 && n_ >= 3) {
      for (int p = 0; p < n_; ++p) {
        for (int q = p + 1; q < n_; ++q) {
          for (int r = q + 1; r < n_; ++r) {
            actions.push_back({p, q, r});
          }
        }
      }
    }
    if (cops > 3) {
      throw std::invalid_argument("production search supports at most three cops");
    }

    std::vector<std::vector<Mask>> partitions;
    partitions.reserve(actions.size());
    for (const auto& action : actions) {
      std::vector<std::pair<std::vector<Mask>, Mask>> keyed_classes;
      for (int robber = 0; robber < n_; ++robber) {
        std::vector<Mask> signature;
        signature.reserve(action.size());
        for (const int probe : action) {
          signature.push_back(responses_[static_cast<std::size_t>(probe)][static_cast<std::size_t>(robber)]);
        }
        auto found = std::ranges::find_if(keyed_classes, [&](const auto& entry) {
          return entry.first == signature;
        });
        if (found == keyed_classes.end()) {
          keyed_classes.push_back({std::move(signature), Mask{1} << robber});
        } else {
          found->second |= Mask{1} << robber;
        }
      }
      std::vector<Mask> classes;
      classes.reserve(keyed_classes.size());
      for (const auto& entry : keyed_classes) {
        classes.push_back(entry.second);
      }
      partitions.push_back(std::move(classes));
    }
    return partitions;
  }
};

}  // namespace

int main(int argc, char** argv) {
  try {
    int cops = 2;
    bool emit_all = false;
    bool check_descent = false;
    int emit_rank = -1;
    int round_limit = 0;
    for (int i = 1; i < argc; ++i) {
      const std::string argument = argv[i];
      if (argument == "--all") {
        emit_all = true;
      } else if (argument == "--check-descent") {
        check_descent = true;
      } else if (argument == "--emit-rank" && i + 1 < argc) {
        emit_rank = std::stoi(argv[++i]);
        if (emit_rank < 0) {
          throw std::invalid_argument("emitted rank must be nonnegative");
        }
      } else if (argument == "--two-round-only") {
        round_limit = 2;
      } else if (argument == "--max-rounds" && i + 1 < argc) {
        round_limit = std::stoi(argv[++i]);
        if (round_limit < 1) {
          throw std::invalid_argument("round limit must be positive");
        }
      } else if (argument == "--cops" && i + 1 < argc) {
        cops = std::stoi(argv[++i]);
      } else {
        throw std::invalid_argument(
            "usage: dirloc_solver [--cops K] [--all|--emit-rank R] "
            "[--two-round-only|--max-rounds R] [--check-descent]");
      }
    }
    if (check_descent && (cops != 2 || round_limit != 0 || emit_rank >= 0)) {
      throw std::invalid_argument("--check-descent permits only the optional --all output flag");
    }

    const auto started = std::chrono::steady_clock::now();
    std::size_t processed = 0;
    std::size_t obstructions = 0;
    std::size_t descent_states = 0;
    std::map<int, std::size_t> rank_counts;
    std::string line;
    while (std::getline(std::cin, line)) {
      if (line.empty() || line.rfind(">>", 0) == 0) {
        continue;
      }
      const FullFeedbackGame game(decode_graph6(line));
      if (check_descent) {
        const auto descent = game.check_response_fiber_descent();
        ++processed;
        descent_states += descent.checked_states;
        if (!descent.holds) {
          ++obstructions;
        }
        if (emit_all || !descent.holds) {
          std::cout << line << '\t' << game.n() << '\t'
                    << (descent.holds ? "DESCENT_OK" : "DESCENT_FAIL") << '\t'
                    << std::hex << descent.counterexample << std::dec << '\t'
                    << descent.checked_states << '\n';
        }
        continue;
      }
      const auto result = game.solve(cops, round_limit);
      ++processed;
      ++rank_counts[result.full_rank];
      if (emit_all || result.full_rank == emit_rank || !result.cops_win || !result.complete) {
        const char* status = result.complete ? (result.cops_win ? "WIN" : "LOSE") : "UNKNOWN";
        std::cout << line << '\t' << game.n() << '\t' << status
                  << '\t' << result.full_rank << '\t' << result.winning_beliefs << '\n';
      }
      if (result.complete && !result.cops_win) {
        ++obstructions;
      }
    }
    const auto finished = std::chrono::steady_clock::now();
    const std::chrono::duration<double> elapsed = finished - started;
    if (check_descent) {
      std::cerr << "processed=" << processed << " descent_failures=" << obstructions
                << " checked_states=" << descent_states
                << " elapsed_seconds=" << elapsed.count() << '\n';
      return EXIT_SUCCESS;
    }
    std::cerr << "processed=" << processed << " obstructions=" << obstructions
              << " cops=" << cops << " elapsed_seconds=" << elapsed.count();
    for (const auto& [rank, count] : rank_counts) {
      std::cerr << " rank_" << rank << '=' << count;
    }
    std::cerr << '\n';
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
