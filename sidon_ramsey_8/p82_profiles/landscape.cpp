#include "core.hpp"
#include <memory>
// Profiles contain the remaining class sizes in nonincreasing order.
using Profile = std::vector<int>;
std::vector<Profile> readprofiles(const char *path) {
  std::ifstream in(path);
  std::string line;
  std::vector<Profile> out;
  while (std::getline(in, line)) {
    std::istringstream row(line);
    Profile a;
    int k;
    while (row >> k) {
      if (k < 2 || k > 11)
        throw std::runtime_error("profile size");
      a.push_back(k);
    }
    if (!row.eof() || a.empty() ||
        !std::is_sorted(a.begin(), a.end(), std::greater<>()))
      throw std::runtime_error("profile");
    out.push_back(a);
  }
  if (!in.eof() || out.empty())
    throw std::runtime_error("profile input");
  return out;
}
struct Solver {
  const Weights &weight;
  const Catalog *catalog;
  int method;
  std::ostream *trace, *terminal;
  uint64_t calls = 0, queries = 0, options = 0, leaves = 0, found = 0;
  std::vector<size_t> ids;
  std::vector<U> chosen;
  int classcap(int k) const { return k == 9 ? 3776423 : k < 9 ? k * 444444 : cap; }
  void word(uint64_t a) {
    for (int i = 0; i < 8; ++i)
      trace->put(char((a >> (8 * i)) & 255));
  }
  void mask(U a) {
    word(uint64_t(a));
    word(uint64_t(a >> 64));
  }
  std::vector<U> generate(U domain, int size) const {
    std::vector<U> out;
    if (method) {
      Enum e;
      out = e.run(domain, size);
    } else {
      Enumerate e;
      e.n = 82;
      out = e.run(domain, size);
    }
    std::sort(out.begin(), out.end());
    return out;
  }
  void record(U domain, const Profile &p, size_t at, int upper,
              const std::vector<U> &a) {
    ++queries;
    options += a.size();
    if (!trace || a.empty())
      return;
    mask(domain);
    word(p.size() - at);
    for (size_t i = at; i < p.size(); ++i)
      word(uint64_t(p[i]));
    word(uint64_t(upper));
    word(a.size());
    for (U b : a)
      mask(b);
  }
  std::vector<U> visit(U domain, const Profile &p, size_t at, int upper) {
    ++calls;
    if (at >= p.size() ||
        pop(domain) !=
            std::accumulate(p.begin() + std::ptrdiff_t(at), p.end(), 0))
      throw std::runtime_error("state");
    int size = p[at], count = 0, othercap = 0;
    for (size_t i = at; i < p.size(); ++i) {
      if (p[i] == size)
        ++count;
      else
        othercap += classcap(p[i]);
    }
    int sum = weight(domain);
    upper = std::min(upper, classcap(size));
    if (sum > count * upper + othercap)
      return {};
    if (at + 1 == p.size()) {
      ++leaves;
      bool ok = sidon(domain, method);
      if (terminal) {
        *terminal << "{\"ids\":[";
        for (size_t i = 0; i < ids.size(); ++i) {
          if (i)
            *terminal << ',';
          *terminal << ids[i];
        }
        *terminal << "],\"chosen\":[";
        for (size_t i = 0; i < chosen.size(); ++i) {
          if (i)
            *terminal << ',';
          printset(chosen[i], *terminal);
        }
        *terminal << "],\"residual\":";
        printset(domain, *terminal);
        *terminal << ",\"sidon\":" << (ok ? "true" : "false") << "}\n";
      }
      return ok ? std::vector<U>{domain} : std::vector<U>{};
    }
    int lower = std::max(0, (sum - othercap + count - 1) / count);
    std::vector<U> a;
    if (size == 10 && catalog && pop(domain) > 30) {
      if (lower < catalog->minweight)
        throw std::runtime_error("cutoff");
      a = catalog->query(domain, lower, upper);
    } else {
      a = generate(domain, size);
      a.erase(std::remove_if(a.begin(), a.end(),
                             [&](U b) {
                               int z = weight(b);
                               return z < lower || z > upper;
                             }),
              a.end());
    }
    record(domain, p, at, upper, a);
    for (U b : a) {
      chosen.push_back(b);
      auto ans = visit(domain ^ b, p, at + 1,
                       p[at + 1] == size ? weight(b) : classcap(p[at + 1]));
      chosen.pop_back();
      if (!ans.empty()) {
        ans.push_back(b);
        return ans;
      }
    }
    return {};
  }
  std::vector<U> run(U domain, const std::vector<Profile> &profiles) {
    for (const auto &p : profiles) {
      auto a = visit(domain, p, 0, classcap(p[0]));
      if (!a.empty()) {
        ++found;
        return a;
      }
    }
    return {};
  }
};
struct Packing {
  const Weights &weight;
  Solver *solver;
  int method, target, shard, parts;
  std::vector<U> sets;
  std::vector<int> ws;
  std::vector<size_t> ids;
  uint64_t packings = 0, found = 0;
  int threshold;
  std::vector<Profile> profiles;
  std::ostream &out;
  Packing(const char *path, const Weights &w, Solver *h, int alg, int k, int s,
          int n, std::ostream &o)
      : weight(w), solver(h), method(alg), target(k), shard(s), parts(n),
        ids(size_t(k)), threshold(total_weight - (8 - k) * cap), out(o) {
    if (k < 2 || k > 4 || n < 1 || s < 0 || s >= n ||
        weight(universe) != total_weight ||
        !std::equal(w.w.begin(), w.w.end(), w.w.rbegin()))
      throw std::runtime_error("packing parameters");
    profiles = k == 4   ? std::vector<Profile>{{10, 10, 10, 8}, {10, 10, 9, 9}}
               : k == 3 ? std::vector<Profile>{{10, 10, 10, 10, 9}}
                        : std::vector<Profile>{{10, 10, 10, 10, 10, 10}};
    std::ifstream in(path);
    std::string line;
    while (std::getline(in, line)) {
      U a = readset(line);
      if (pop(a) != 11 || !sidon(a, alg) || weight(a) > cap)
        throw std::runtime_error("eleven");
      sets.push_back(a);
      ws.push_back(weight(a));
    }
    if (!in.eof() || sets.size() != 8214 ||
        !std::is_sorted(ws.begin(), ws.end(), std::greater<>()))
      throw std::runtime_error("catalog");
    for (size_t a = 0; a < sets.size(); a += 2) {
      U r = 0;
      for (int x = 0; x < 82; ++x)
        if (sets[a] & (U(1) << x))
          r |= U(1) << (81 - x);
      if (r != sets[a + 1] || sets[a] >= sets[a + 1] ||
          (a && ws[a] == ws[a - 2] && sets[a] <= sets[a - 2]))
        throw std::runtime_error("orbits");
    }
  }
  void leaf(U used, int sum) {
    if (sum < threshold || pop(used) != 11 * target)
      throw std::runtime_error("leaf");
    ++packings;
    if (!solver)
      return;
    solver->ids = ids;
    auto a = solver->run(universe ^ used, profiles);
    if (!a.empty()) {
      ++found;
      std::cerr << "WITNESS IDs";
      for (auto id : ids)
        std::cerr << ' ' << id;
      std::cerr << '\n';
      for (U b : a) {
        printset(b, std::cerr);
        std::cerr << '\n';
      }
    }
  }
  void recursive(const std::vector<size_t> &cand, int need, U used, int sum) {
    if (cand.size() < size_t(need))
      return;
    int upper = sum;
    for (int i = 0; i < need; ++i)
      upper += ws[cand[size_t(i)]];
    if (upper < threshold)
      return;
    for (size_t i = 0; i + size_t(need) <= cand.size(); ++i) {
      size_t b = cand[i];
      if (sum + need * ws[b] < threshold)
        break;
      ids[size_t(target - need)] = b;
      if (need == 1) {
        leaf(used | sets[b], sum + ws[b]);
        continue;
      }
      std::vector<size_t> next;
      for (size_t j = i + 1; j < cand.size(); ++j)
        if (!(sets[b] & sets[cand[j]]))
          next.push_back(cand[j]);
      recursive(next, need - 1, used | sets[b], sum + ws[b]);
    }
  }
  void fixed(size_t a, const std::vector<size_t> &cand) {
    for (size_t i = 0; i + size_t(target - 1) <= cand.size(); ++i) {
      size_t b = cand[i];
      if (ws[a] + (target - 1) * ws[b] < threshold)
        break;
      ids[1] = b;
      if (target == 2) {
        leaf(sets[a] | sets[b], ws[a] + ws[b]);
        continue;
      }
      for (size_t j = i + 1; j + size_t(target - 2) <= cand.size(); ++j) {
        size_t c = cand[j];
        if (ws[a] + ws[b] + (target - 2) * ws[c] < threshold)
          break;
        if (sets[b] & sets[c])
          continue;
        ids[2] = c;
        U used = sets[a] | sets[b] | sets[c];
        int sum = ws[a] + ws[b] + ws[c];
        if (target == 3) {
          leaf(used, sum);
          continue;
        }
        for (size_t t = j + 1; t < cand.size(); ++t) {
          size_t d = cand[t];
          if (sum + ws[d] < threshold)
            break;
          if (used & sets[d])
            continue;
          ids[3] = d;
          leaf(used | sets[d], sum + ws[d]);
        }
      }
    }
  }
  void run() {
    out << "orbit,packings,calls,queries,options,leaves,found\n";
    for (size_t a = 0; a < sets.size(); a += 2) {
      if (target * ws[a] < threshold)
        break;
      if ((a / 2) % size_t(parts) != size_t(shard))
        continue;
      uint64_t op = packings, oc = solver ? solver->calls : 0,
               oq = solver ? solver->queries : 0,
               oo = solver ? solver->options : 0,
               ol = solver ? solver->leaves : 0, of = found;
      ids[0] = a;
      std::vector<size_t> cand;
      for (size_t b = a + 1; b < sets.size(); ++b)
        if (!(sets[a] & sets[b]))
          cand.push_back(b);
      if (method)
        recursive(cand, target - 1, sets[a], ws[a]);
      else
        fixed(a, cand);
      out << a / 2 << ',' << packings - op << ','
          << (solver ? solver->calls - oc : 0) << ','
          << (solver ? solver->queries - oq : 0) << ','
          << (solver ? solver->options - oo : 0) << ','
          << (solver ? solver->leaves - ol : 0) << ',' << found - of << '\n';
      out.flush();
      if (!out)
        throw std::runtime_error("case write");
    }
  }
};
int main(int argc, char **argv) {
  try {
    auto start = std::chrono::steady_clock::now();
    if (argc < 2)
      throw std::runtime_error("mode");
    std::string mode = argv[1];
    if (mode == "complete") {
      if (argc != 9 && argc != 10)
        throw std::runtime_error("complete method weights profiles domains "
                                 "trace decisions done [ten_catalog]");
      int method = integer(argv[2]);
      if (method < 0 || method > 1)
        throw std::runtime_error("method");
      Weights w(argv[3]);
      auto profiles = readprofiles(argv[4]);
      std::ifstream in(argv[5]);
      std::ofstream trace(argv[6], std::ios::binary), out(argv[7]);
      if (!in || !trace || !out)
        throw std::runtime_error("IO");
      std::unique_ptr<Catalog> catalog;
      if (argc == 10)
        catalog = std::make_unique<Catalog>(argv[9], w, 10, 0, method);
      Solver s{w, catalog.get(), method, &trace, nullptr, 0, 0, 0, 0, 0, {},
               {}};
      std::string line;
      uint64_t domains = 0;
      while (std::getline(in, line)) {
        U d = readset(line);
        auto a = s.run(d, profiles);
        out << "{\"found\":" << (!a.empty() ? "true" : "false")
            << ",\"partition\":[";
        for (size_t i = 0; i < a.size(); ++i) {
          if (i)
            out << ',';
          printset(a[i], out);
        }
        out << "]}\n";
        ++domains;
      }
      out.flush();
      trace.flush();
      if (!in.eof() || !out || !trace)
        throw std::runtime_error("completion IO");
      std::ofstream done(argv[8]);
      done << "complete\n";
      done.close();
      if (!done)
        throw std::runtime_error("done");
      std::cout << "{\"complete\":true,\"domains\":" << domains
                << ",\"found\":" << s.found << ",\"calls\":" << s.calls
                << ",\"queries\":" << s.queries << ",\"options\":" << s.options
                << ",\"leaves\":" << s.leaves << "}\n";
      return 0;
    }
    if (mode == "count") {
      if (argc != 7)
        throw std::runtime_error("count method anchors orbit weights cases");
      int method = integer(argv[2]);
      if (method < 0 || method > 1)
        throw std::runtime_error("method");
      Weights w(argv[5]);
      std::ofstream out(argv[6]);
      if (!out)
        throw std::runtime_error("output");
      Packing p(argv[4], w, nullptr, method, integer(argv[3]), 0, 1, out);
      p.run();
      std::cout << "{\"complete\":true,\"packings\":" << p.packings << "}\n";
      return 0;
    }
    if (mode != "sweep" || argc != 13)
      throw std::runtime_error("sweep method anchors orbit weights full_ten "
                               "shard parts cases trace terminals done");
    int method = integer(argv[2]);
    Weights w(argv[5]);
    Catalog c(argv[6], w, 10, 0, method);
    if (c.masks.size() != 17249580 ||
        *std::max_element(c.weights.begin(), c.weights.end()) > cap)
      throw std::runtime_error("full ten catalog");
    std::ofstream out(argv[9]), trace(argv[10], std::ios::binary),
        terminal(argv[11]);
    if (!out || !trace || !terminal)
      throw std::runtime_error("outputs");
    Solver s{w, &c, method, &trace, &terminal, 0, 0, 0, 0, 0, {}, {}};
    Packing p(argv[4], w, &s, method, integer(argv[3]), integer(argv[7]),
              integer(argv[8]), out);
    p.run();
    out.flush();
    trace.flush();
    terminal.flush();
    if (!out || !trace || !terminal)
      throw std::runtime_error("output completion");
    std::ofstream done(argv[12]);
    done << "complete\n";
    done.close();
    if (!done)
      throw std::runtime_error("done");
    std::cout << "{\"complete\":true,\"packings\":" << p.packings
              << ",\"found\":" << p.found << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
