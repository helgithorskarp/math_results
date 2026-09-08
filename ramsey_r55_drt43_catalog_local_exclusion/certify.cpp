#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <vector>
#include "cadical.hpp"

using namespace std;
namespace fs = std::filesystem;
constexpr int N = 43;
constexpr int L = 21;
constexpr int PAIRS = L * (L - 1) / 2;
constexpr int VARS = PAIRS + L;

using Tournament = array<array<bool, N>, N>;

int pair_var(int a, int b) {
  if (a > b) swap(a, b);
  return 1 + a * (2 * L - a - 1) / 2 + (b - a - 1);
}
int before(int a, int b) { return a < b ? pair_var(a, b) : -pair_var(b, a); }

Tournament decode(const string &line) {
  if (line.size() != static_cast<size_t>(N * (N - 1) / 2))
    throw runtime_error("catalog record length is not 903");
  Tournament t{};
  size_t k = 0;
  for (int i = 0; i < N; ++i) for (int j = i + 1; j < N; ++j) {
    char c = line[k++];
    if (c != '0' && c != '1') throw runtime_error("non-bit in catalog record");
    t[i][j] = c == '1';
    t[j][i] = !t[i][j];
  }
  for (int i = 0; i < N; ++i) {
    int degree = 0;
    for (int j = 0; j < N; ++j) degree += t[i][j];
    if (degree != 21) throw runtime_error("record is not regular");
  }
  for (int i = 0; i < N; ++i) for (int j = i + 1; j < N; ++j) {
    int common = 0;
    for (int k2 = 0; k2 < N; ++k2) common += t[i][k2] && t[j][k2];
    if (common != 10) throw runtime_error("record is not doubly regular");
  }
  return t;
}

vector<vector<int>> clauses_for(const Tournament &t, int root) {
  vector<int> q;
  for (int v = 0; v < N; ++v) if (t[root][v]) q.push_back(v);
  if (q.size() != L) throw runtime_error("root outneighborhood has wrong size");
  vector<vector<int>> clauses;
  clauses.reserve(6500);
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) {
      clauses.push_back({-before(a,b), -before(b,c), before(a,c)});
      clauses.push_back({before(a,b), before(b,c), -before(a,c)});
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d) {
      array<int,4> x{a,b,c,d}, degree{};
      for (int i = 0; i < 4; ++i) for (int j = 0; j < 4; ++j)
        if (i != j) degree[i] += t[q[x[i]]][q[x[j]]];
      auto sorted = degree;
      sort(sorted.begin(), sorted.end());
      if (sorted != array<int,4>{0,1,2,3}) continue;
      array<int,4> seq{0,1,2,3};
      sort(seq.begin(), seq.end(), [&](int i, int j) { return degree[i] > degree[j]; });
      clauses.push_back({-before(x[seq[0]],x[seq[1]]),
                         -before(x[seq[1]],x[seq[2]]),
                         -before(x[seq[2]],x[seq[3]])});
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d)
      for (int e = d + 1; e < L; ++e) {
        array<int,5> x{a,b,c,d,e}, degree{};
        for (int i = 0; i < 5; ++i) for (int j = 0; j < 5; ++j)
          if (i != j) degree[i] += t[q[x[i]]][q[x[j]]];
        auto sorted = degree;
        sort(sorted.begin(), sorted.end());
        if (sorted != array<int,5>{0,1,2,3,4}) continue;
        array<int,5> seq{0,1,2,3,4};
        sort(seq.begin(), seq.end(), [&](int i, int j) { return degree[i] > degree[j]; });
        clauses.push_back({-before(x[seq[1]],x[seq[0]]),
                           -before(x[seq[2]],x[seq[1]]),
                           -before(x[seq[3]],x[seq[2]]),
                           -before(x[seq[4]],x[seq[3]])});
      }
  vector<int> selectors;
  for (int f = 0; f < L; ++f) selectors.push_back(PAIRS + f + 1);
  clauses.push_back(selectors);
  for (int f = 0; f < L; ++f) for (int j = 0; j < L; ++j) if (j != f)
    clauses.push_back({-(PAIRS + f + 1), before(f,j)});
  return clauses;
}

void emit_cnf(const vector<vector<int>> &clauses, const fs::path &path) {
  ofstream out(path);
  if (!out) throw runtime_error("cannot create CNF");
  out << "p cnf " << VARS << ' ' << clauses.size() << '\n';
  for (const auto &clause : clauses) {
    for (int literal : clause) out << literal << ' ';
    out << "0\n";
  }
  if (!out) throw runtime_error("failed writing CNF");
}

int solve_incrementally(const vector<vector<int>> &clauses, const fs::path &proof) {
  CaDiCaL::Solver solver;
  solver.set("quiet", 1);
  if (!solver.trace_proof(proof.c_str())) throw runtime_error("cannot create proof trace");
  for (const auto &clause : clauses) {
    for (int literal : clause) solver.add(literal);
    solver.add(0);
  }
  for (int first = 0; first < L; ++first) {
    solver.assume(PAIRS + first + 1);
    if (!solver.limit("conflicts", 100000)) throw runtime_error("cannot set conflict limit");
    int status = solver.solve();
    if (status != 20) {
      solver.close_proof_trace();
      return status;
    }
    solver.conclude();
  }
  if (!solver.limit("conflicts", 100000)) throw runtime_error("cannot set conflict limit");
  int status = solver.solve();
  if (status == 20) solver.conclude();
  solver.close_proof_trace();
  return status;
}

int run(const vector<string> &args, const fs::path &log) {
  pid_t pid = fork();
  if (pid < 0) throw runtime_error("fork failed");
  if (pid == 0) {
    int fd = open(log.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) _exit(125);
    if (dup2(fd, STDOUT_FILENO) < 0 || dup2(fd, STDERR_FILENO) < 0) _exit(125);
    close(fd);
    vector<char*> argv;
    for (const auto &arg : args) argv.push_back(const_cast<char*>(arg.c_str()));
    argv.push_back(nullptr);
    execv(argv[0], argv.data());
    _exit(127);
  }
  int status = 0;
  if (waitpid(pid, &status, 0) < 0) throw runtime_error("waitpid failed");
  if (!WIFEXITED(status)) return 128;
  return WEXITSTATUS(status);
}

bool contains(const fs::path &path, const string &needle) {
  ifstream in(path);
  string text((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
  return text.find(needle) != string::npos;
}

int main(int argc, char **argv) try {
  if (argc < 2) throw runtime_error("usage: --emit DATA RECORD ROOT CNF | --certify DATA FIRST COUNT ROOTS DRAT TMP SUMMARY");
  string mode = argv[1];
  ifstream input(argv[2]);
  if (!input) throw runtime_error("cannot open catalog");
  vector<string> lines;
  string line;
  while (input >> line) lines.push_back(line);
  if (mode == "--emit") {
    if (argc != 6) throw runtime_error("bad --emit arguments");
    int record = stoi(argv[3]), root = stoi(argv[4]);
    if (record < 0 || record >= static_cast<int>(lines.size()) || root < 0 || root >= N)
      throw runtime_error("record/root out of range");
    auto t = decode(lines[record]);
    auto clauses = clauses_for(t, root);
    emit_cnf(clauses, argv[5]);
    cout << "EMITTED " << record << ' ' << root << ' ' << VARS << ' ' << clauses.size() << '\n';
    return 0;
  }
  if (mode != "--certify" || argc != 9) throw runtime_error("bad --certify arguments");
  int first = stoi(argv[3]), count = stoi(argv[4]), roots = stoi(argv[5]);
  string drat = argv[6];
  fs::path temp = argv[7], summary = argv[8];
  if (first < 0 || count < 0 || first + count > static_cast<int>(lines.size()) || roots < 1 || roots > N)
    throw runtime_error("range out of bounds");
  fs::create_directories(temp);
  ofstream result(summary);
  if (!result) throw runtime_error("cannot create summary");
  result << "record\troots\tunsat\tclauses\tproof_bytes\n";
  uint64_t tested = 0, unsat = 0, total_clauses = 0, total_proof_bytes = 0;
  fs::path stem = temp / ("certify-" + to_string(getpid()));
  fs::path cnf = stem; cnf += ".cnf";
  fs::path proof = stem; proof += ".drat";
  fs::path verify_log = stem; verify_log += ".verify";
  for (int record = first; record < first + count; ++record) {
    auto t = decode(lines[record]);
    uint64_t rec_clauses = 0, rec_bytes = 0, rec_unsat = 0;
    for (int root = 0; root < roots; ++root) {
      auto clauses = clauses_for(t, root);
      emit_cnf(clauses, cnf);
      int sr = solve_incrementally(clauses, proof);
      ++tested;
      if (sr == 10) {
        cerr << "SAT record " << record << " root " << root << " artifacts " << stem << '\n';
        return 10;
      }
      if (sr != 20) {
        cerr << "UNKNOWN record " << record << " root " << root << " solver_status " << sr << " artifacts " << stem << '\n';
        return 2;
      }
      int vr = run({drat, cnf.string(), proof.string()}, verify_log);
      if (vr != 0 || !contains(verify_log, "s VERIFIED")) {
        cerr << "PROOF_FAILURE record " << record << " root " << root << " verifier_rc " << vr << " artifacts " << stem << '\n';
        return 3;
      }
      auto bytes = fs::file_size(proof);
      ++unsat; ++rec_unsat;
      total_clauses += clauses.size(); rec_clauses += clauses.size();
      total_proof_bytes += bytes; rec_bytes += bytes;
      fs::remove(cnf); fs::remove(proof); fs::remove(verify_log);
    }
    result << record << '\t' << roots << '\t' << rec_unsat << '\t' << rec_clauses << '\t' << rec_bytes << '\n';
    result.flush();
    cerr << "record " << record << " roots " << roots << " checked " << tested << '\n';
  }
  result << "TOTAL\t" << tested << '\t' << unsat << '\t' << total_clauses << '\t' << total_proof_bytes << '\n';
  cout << "CERTIFIED tested " << tested << " unsat " << unsat << " clauses " << total_clauses
       << " proof_bytes " << total_proof_bytes << '\n';
  return 0;
} catch (const exception &e) {
  cerr << "error: " << e.what() << '\n';
  return 1;
}
