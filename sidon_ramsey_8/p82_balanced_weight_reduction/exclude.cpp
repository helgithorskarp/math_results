#include "search.hpp"
void add(uint64_t &x, uint64_t y) {
  if (x > UINT64_MAX - y)
    throw std::runtime_error("counter overflow");
  x += y;
}
int main(int argc, char **argv) {
  try {
    if (argc != 13)
      throw std::runtime_error("method weights full_ten orbit minimum maximum "
                               "shard parts budget cases trace done");
    int method = integer(argv[1]), minimum = integer(argv[5]),
        maximum = integer(argv[6]), shard = integer(argv[7]),
        parts = integer(argv[8]);
    uint64_t budget = std::stoull(argv[9]);
    if ((method != 0 && method != 1) || minimum < 0 || maximum > 4107 ||
        minimum > maximum || parts < 1 || parts > 64 || shard < 0 ||
        shard >= parts || budget < 1 || budget > 1000000000)
      throw std::runtime_error("parameters");
    auto start = std::chrono::steady_clock::now();
    Weights w(argv[2]);
    if (w(universe) != total_weight ||
        !std::equal(w.w.begin(), w.w.end(), w.w.rbegin()))
      throw std::runtime_error("weights");
    Catalog global(argv[3], w, 10, 0, method);
    if (global.masks.size() != 17249580 ||
        *std::max_element(global.weights.begin(), global.weights.end()) > cap)
      throw std::runtime_error("full ten catalog");
    std::vector<U> elevens;
    std::vector<int> ws;
    std::ifstream in(argv[4]);
    std::string line;
    while (std::getline(in, line)) {
      U a = readset(line);
      if (pop(a) != 11 || !sidon(a, method) || w(a) > cap)
        throw std::runtime_error("eleven");
      elevens.push_back(a);
      ws.push_back(w(a));
    }
    if (!in.eof() || elevens.size() != 8214 ||
        !std::is_sorted(ws.begin(), ws.end(), std::greater<>()))
      throw std::runtime_error("eleven catalog");
    for (size_t i = 0; i < elevens.size(); i += 2) {
      U reflect = 0;
      for (int x = 0; x < 82; ++x)
        if (elevens[i] & (U(1) << x))
          reflect |= U(1) << (81 - x);
      if (reflect != elevens[i + 1] || elevens[i] >= reflect ||
          (i && ws[i] == ws[i - 2] && elevens[i] <= elevens[i - 2]))
        throw std::runtime_error("canonical order");
    }
    std::ofstream out(argv[10]), stream(argv[11], std::ios::binary);
    if (!out || !stream)
      throw std::runtime_error("outputs");
    Trace trace{stream};
    out << "orbit,packings,unsat,unknown,sat,calls,queries,options,leaves,max_"
           "calls,parent_rows,trace_end\n";
    uint64_t packings = 0, found = 0, unknown = 0;
    for (int q = maximum; q-- > minimum;) {
      if (q % parts != shard)
        continue;
      size_t i = size_t(2 * q);
      U a = elevens[i];
      std::vector<size_t> partners;
      for (size_t j = i + 1; j < elevens.size(); ++j) {
        if (ws[i] + ws[j] < total_weight - 6 * cap)
          break;
        if (!(a & elevens[j]))
          partners.push_back(j);
      }
      uint64_t unsat_count = 0, unknown_count = 0, sat_count = 0, calls = 0,
               queries = 0, options = 0, leaves = 0, max_calls = 0,
               parent_rows = 0;
      std::unique_ptr<Catalog> parent;
      if (!partners.empty()) {
        int cutoff = std::max(0, w(universe ^ a) - ws[i] - 5 * cap);
        auto rows = global.query(universe ^ a, cutoff, cap);
        parent_rows = rows.size();
        parent = std::make_unique<Catalog>(std::move(rows), w, 10, cutoff, 1);
      }
      for (size_t j : partners) {
        U d = universe ^ (a | elevens[j]);
        int lower = std::max(0, w(d) - 5 * cap);
        if (lower < parent->minweight)
          throw std::runtime_error("root cutoff");
        trace.word(1);
        trace.word(i);
        trace.word(j);
        Search s{w, *parent, method, budget, &trace};
        int status = 0;
        try {
          status = s.visit(d, 6, cap) ? 2 : 0;
        } catch (Limit &) {
          status = 1;
        }
        trace.word(4);
        trace.word(uint64_t(status));
        trace.word(s.calls);
        trace.word(s.queries);
        trace.word(s.options);
        trace.word(s.leaves);
        if (status == 0) {
          ++unsat_count;
          if (s.calls != 1 + s.options)
            throw std::runtime_error("complete call identity");
        }
        if (status == 1)
          ++unknown_count;
        if (status == 2) {
          ++sat_count;
          std::cerr << "{\"partition\":[";
          printset(a, std::cerr);
          std::cerr << ',';
          printset(elevens[j], std::cerr);
          for (U x : s.chosen) {
            std::cerr << ',';
            printset(x, std::cerr);
          }
          std::cerr << "]}\n";
        }
        add(calls, s.calls);
        add(queries, s.queries);
        add(options, s.options);
        add(leaves, s.leaves);
        max_calls = std::max(max_calls, s.calls);
      }
      packings += partners.size();
      found += sat_count;
      unknown += unknown_count;
      out << q << ',' << partners.size() << ',' << unsat_count << ','
          << unknown_count << ',' << sat_count << ',' << calls << ',' << queries
          << ',' << options << ',' << leaves << ',' << max_calls << ','
          << parent_rows << ',' << trace.bytes << '\n';
      out.flush();
      if (!out)
        throw std::runtime_error("case write");
    }
    trace.flush();
    stream.flush();
    out.flush();
    if (!stream || !out)
      throw std::runtime_error("output completion");
    std::ofstream done(argv[12]);
    done << "complete\n";
    done.close();
    if (!done)
      throw std::runtime_error("done write");
    std::cout << "{\"complete\":true,\"packings\":" << packings
              << ",\"sat\":" << found << ",\"unknown\":" << unknown
              << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
