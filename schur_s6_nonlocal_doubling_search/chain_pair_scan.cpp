// Exhaust two colour transpositions, each on one complete doubling chain.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <vector>
using namespace std;

struct Edge { int x, y, z; };
struct Change { int v, color; };
struct Move { int root, a, b, delta; vector<Change> changes; };
constexpr int N = 537;
constexpr int W = N + 1;

int main(int argc, char** argv) {
  bool full_root1=argc==3 && string(argv[2])=="--full-root1";
  bool full_all=argc==3 && string(argv[2])=="--full-all";
  if (argc != 2 && !full_root1 && !full_all) {
    cerr << "usage: chain_pair_scan 537word [--full-root1|--full-all]\n"; return 2;
  }
  ifstream input(argv[1]); string word; input >> word;
  if (word.size() != N || word.find_first_not_of("123456") != string::npos) {
    cerr << "expected 537 colours in 1..6\n"; return 2;
  }
  vector<int> base(W);
  for (int i = 1; i <= N; ++i) base[i] = word[i-1]-'0';
  for (int i = 1; i*2 <= N; ++i)
    if (base[i] == base[2*i]) { cerr << "input violates doubling\n"; return 2; }

  vector<Edge> edges;
  vector<vector<int>> incident(W);
  // Each pair of distinct vertices belongs to at most two distinct-summand triples.
  vector<array<int,2>> pair_edges(W*W, {-1,-1});
  auto add_pair = [&](int a, int b, int id) {
    if (a>b) swap(a,b);
    auto &slot=pair_edges[a*W+b];
    if (slot[0]<0) slot[0]=id;
    else if (slot[1]<0) slot[1]=id;
    else { cerr << "unexpected triple multiplicity\n"; exit(3); }
  };
  for (int x=1; x<=N; ++x) for (int y=x+1; x+y<=N; ++y) {
    int z=x+y, id=edges.size(); edges.push_back({x,y,z});
    for (int v : {x,y,z}) incident[v].push_back(id);
    add_pair(x,y,id); add_pair(x,z,id); add_pair(y,z,id);
  }
  auto mono = [&](int id, const Move* a, const Move* b) {
    auto [x,y,z]=edges[id];
    auto color = [&](int v) {
      if (a) for (auto ch:a->changes) if (ch.v==v) return ch.color;
      if (b) for (auto ch:b->changes) if (ch.v==v) return ch.color;
      return base[v];
    };
    return color(x)==color(y) && color(y)==color(z);
  };
  int baseline=0;
  for (int id=0; id<(int)edges.size(); ++id) baseline+=mono(id,nullptr,nullptr);
  vector<Move> moves;
  vector<int> seen(edges.size(),0);
  int stamp=0;
  auto add_move = [&](Move m) {
      if (m.changes.empty()) return;
      ++stamp;
      for (auto ch:m.changes) for (int id:incident[ch.v]) if (seen[id]!=stamp) {
        seen[id]=stamp;
        m.delta+=mono(id,&m,nullptr)-mono(id,nullptr,nullptr);
      }
      moves.push_back(move(m));
  };
  for (int root=1; root<=N; root+=2) for (int a=1; a<=6; ++a)
    for (int b=a+1; b<=6; ++b) {
      if (full_all || (full_root1 && root==1)) continue;
      Move m{root,a,b,0,{}};
      for (int v=root; v<=N; v*=2)
        if (base[v]==a) m.changes.push_back({v,b});
        else if (base[v]==b) m.changes.push_back({v,a});
      add_move(move(m));
    }
  int permutations=0;
  if (full_root1 || full_all) {
    for (int root=1;root<=N;root+=2) {
      if (full_root1 && root!=1) continue;
      array<int,6> p{1,2,3,4,5,6};
      set<string> seen_words;
      do {
        Move m{root,0,permutations,0,{}};
        string chain_word;
        for (int v=root;v<=N;v*=2) {
          int d=p[base[v]-1];
          chain_word+=char('0'+d);
          if (d!=base[v]) m.changes.push_back({v,d});
        }
        if (seen_words.insert(chain_word).second) {
          add_move(move(m));
          ++permutations;
        }
      } while (next_permutation(p.begin(),p.end()));
    }
  }
  auto direct_score = [&](const Move* a, const Move* b) {
    vector<int> color=base;
    if (a) for (auto ch:a->changes) color[ch.v]=ch.color;
    if (b) for (auto ch:b->changes) color[ch.v]=ch.color;
    for (int v=1;v*2<=N;++v) if (color[v]==color[2*v]) {
      cerr << "audited move violates doubling\n"; exit(4);
    }
    int score=0;
    for (auto [x,y,z]:edges) score+=(color[x]==color[y] && color[y]==color[z]);
    return score;
  };
  long long single_audits=0;
  for (const auto &m:moves) {
    if (full_all && single_audits%10!=0) { ++single_audits; continue; }
    ++single_audits;
    if (direct_score(&m,nullptr)==baseline+m.delta) continue;
    cerr << "single move incremental score mismatch\n"; return 4;
  }
  int single_best=baseline;
  for (const auto &m:moves) single_best=min(single_best,baseline+m.delta);
  int best=baseline, best_i=-1, best_j=-1;
  long long tested=0, improving=0, pair_audits=0;
  for (int i=0; i<(int)moves.size(); ++i) for (int j=i+1; j<(int)moves.size(); ++j) {
    const auto &a=moves[i], &b=moves[j];
    if (a.root==b.root) continue;
    ++tested;
    int score=baseline+a.delta+b.delta;
    // Only triples containing a changed vertex from each chain need a correction.
    // Distinct chains have at most 10 and 8 vertices, and a vertex pair
    // belongs to at most two triples, so 256 exceeds the maximum 160 ids.
    int shared[256], nshared=0;
    for (auto ca:a.changes) for (auto cb:b.changes) {
      int u=min(ca.v,cb.v), v=max(ca.v,cb.v);
      for (int id:pair_edges[u*W+v]) if (id>=0) {
        bool novel=true;
        for (int k=0;k<nshared;++k) if (shared[k]==id) { novel=false; break; }
        if (novel) {
          if (nshared==256) { cerr << "shared buffer overflow\n"; return 3; }
          shared[nshared++]=id;
        }
      }
    }
    for (int k=0;k<nshared;++k) {
      int id=shared[k];
      score+=mono(id,&a,&b)-mono(id,&a,nullptr)-mono(id,nullptr,&b)+mono(id,nullptr,nullptr);
    }
    if (tested%(full_all?100003:997)==0) {
      ++pair_audits;
      if (direct_score(&a,&b)!=score) {
        cerr << "pair incremental score mismatch\n"; return 4;
      }
    }
    if (score<baseline) ++improving;
    if (score<best) { best=score; best_i=i; best_j=j; }
  }
  cout << "triples=" << edges.size() << " baseline=" << baseline
       << " nontrivial_chain_moves=" << moves.size()
       << " unique_chain_permutations=" << permutations
       << " single_best=" << single_best
       << " distinct_chain_pairs=" << tested
       << " directly_audited_pairs=" << pair_audits
       << " improving_pairs=" << improving << " best=" << best << '\n';
  if (best_i>=0) {
    auto &a=moves[best_i], &b=moves[best_j];
    string result=word;
    for (auto ch:a.changes) result[ch.v-1]=char('0'+ch.color);
    for (auto ch:b.changes) result[ch.v-1]=char('0'+ch.color);
    int direct=0;
    vector<int> color(W);
    for (int v=1;v<=N;++v)color[v]=result[v-1]-'0';
    for (auto [x,y,z]:edges) direct+=(color[x]==color[y]&&color[y]==color[z]);
    if (direct!=best) { cerr << "incremental score mismatch\n"; return 4; }
    cout << "best_moves=" << a.root << ':' << a.a << ':' << a.b << ','
         << b.root << ':' << b.a << ':' << b.b << " direct=" << direct << '\n';
    cout << result << '\n';
  }
}
