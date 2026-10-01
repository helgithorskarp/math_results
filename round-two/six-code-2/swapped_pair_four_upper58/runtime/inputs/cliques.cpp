#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
using Clock = std::chrono::steady_clock;
struct Set {
  std::array<std::uint64_t,4> w{};
  bool empty() const {return !(w[0]|w[1]|w[2]|w[3]);}
  int first() const {for(int k=0;k<4;k++) if(w[k]) return 64*k+__builtin_ctzll(w[k]); return -1;}
  void add(int x){w[x/64]|=std::uint64_t(1)<<(x%64);}
  void del(int x){w[x/64]&=~(std::uint64_t(1)<<(x%64));}
  bool has(int x) const {return (w[x/64]>>(x%64))&1U;}
  Set operator&(const Set& b) const {Set r;for(int k=0;k<4;k++)r.w[k]=w[k]&b.w[k];return r;}
  Set minus(const Set& b) const {Set r;for(int k=0;k<4;k++)r.w[k]=w[k]&~b.w[k];return r;}
};
std::vector<Set> adj;
std::vector<int> chosen;
std::uint64_t nodes=0,leaves=0;
std::uint64_t node_cap=3000000;
bool controls=false;
std::vector<std::vector<int>> saved;
int target;
auto start=Clock::now();
void visit(Set pool){
  if(++nodes>node_cap || std::chrono::duration<double>(Clock::now()-start).count()>30)
    throw std::runtime_error("INCOMPLETE fixed clique guard");
  if(int(chosen.size())==target){
    if(++leaves>200000)throw std::runtime_error("INCOMPLETE fixed leaf guard");
    auto out=chosen;std::sort(out.begin(),out.end());
    if(controls) { saved.push_back(out); }
    else { for(int x:out) { std::cout<<x<<' '; } std::cout<<'\n'; }
    return;
  }
  std::vector<int> order,bounds;
  Set left=pool;int color=0;
  while(!left.empty()){
    ++color;Set available=left;
    while(!available.empty()){
      int v=available.first();left.del(v);available.del(v);
      order.push_back(v);bounds.push_back(color);
      available=available.minus(adj[v]);
    }
  }
  for(int k=int(order.size())-1;k>=0;--k){
    if(int(chosen.size())+bounds[k]<target)return;
    int v=order[k];chosen.push_back(v);visit(pool&adj[v]);chosen.pop_back();pool.del(v);
  }
}
int main(int argc,char** argv){try{
  if(argc==2 && std::string(argv[1])=="--self-test"){
    controls=true;std::uint64_t cases=0,total_nodes=0;
    const int n=5;start=Clock::now();
    for(unsigned graph=0;graph<(1U<<10);++graph){
      adj.assign(n,Set{});int bit=0;
      for(int i=0;i<n;i++)for(int j=i+1;j<n;j++,bit++)
        if((graph>>bit)&1U){adj[i].add(j);adj[j].add(i);}
      for(target=0;target<=n;target++){
        std::vector<std::vector<int>> brute;
        for(unsigned mask=0;mask<(1U<<n);++mask){
          std::vector<int> row;for(int i=0;i<n;i++)if((mask>>i)&1U)row.push_back(i);
          if(int(row.size())!=target)continue;
          bool ok=true;for(int i:row)for(int j:row)if(i!=j && !adj[i].has(j))ok=false;
          if(ok)brute.push_back(row);
        }
        nodes=leaves=0;chosen.clear();saved.clear();Set pool;for(int i=0;i<n;i++)pool.add(i);visit(pool);
        std::sort(saved.begin(),saved.end());std::sort(brute.begin(),brute.end());
        if(saved!=brute)throw std::runtime_error("small brute-force disagreement");
        total_nodes+=nodes;++cases;
      }
    }
    std::cout<<"COMPLETE exhaustive-small "<<cases<<' '<<total_nodes<<'\n';return 0;
  }
  if(argc==2 && std::string(argv[1])=="--guard-zero")node_cap=0;
  else if(argc!=1)throw std::runtime_error("invalid command arguments");
  int n;if(!(std::cin>>n>>target)||n<1||n>256||target<0||target>n)throw std::runtime_error("bad graph header");
  adj.resize(n);
  for(int i=0;i<n;i++){
    int count;if(!(std::cin>>count)||count<0||count>=n)throw std::runtime_error("bad degree");
    for(int j=0;j<count;j++){int v;if(!(std::cin>>v)||v<0||v>=n||v==i||adj[i].has(v))throw std::runtime_error("bad edge");adj[i].add(v);}
  }
  for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(adj[i].has(j)!=adj[j].has(i))throw std::runtime_error("asymmetric edge");
  std::string extra;if(std::cin>>extra)throw std::runtime_error("trailing graph input");
  Set pool;for(int i=0;i<n;i++)pool.add(i);start=Clock::now();visit(pool);
  std::cerr<<"COMPLETE "<<nodes<<' '<<leaves<<' '<<std::chrono::duration<double>(Clock::now()-start).count()<<'\n';
  return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}}
