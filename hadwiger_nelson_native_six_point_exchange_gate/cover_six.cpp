#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
using M=array<uint64_t,4>;
struct Key { M m; int k; bool operator==(const Key&x)const{return m==x.m&&k==x.k;} };
struct Hash {size_t operator()(const Key&x)const{uint64_t h=x.k;for(auto a:x.m)h^=a+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
int w,blocks;vector<M> masks;vector<int> costs,chosen;vector<vector<vector<int>>> hits(3);vector<vector<int>> order(3);unordered_set<Key,Hash> failed;uint64_t nodes=0;
bool empty(const M&r){for(int j=0;j<blocks;++j)if(r[j])return false;return true;}
bool search(M r,int cap){
 ++nodes;if(empty(r))return true;if(!cap)return false;
 Key key{r,cap};if(cap>1&&failed.count(key))return false;
 int level=min(cap,2),row=-1;for(int i:order[level])if((r[i/64]>>(i%64))&1){row=i;break;}
 if(row<0)return false;
 for(int a:hits[level][row]){M t{};for(int j=0;j<blocks;++j)t[j]=r[j]&~masks[a][j];
  if(costs[a]==cap){if(empty(t)){chosen.push_back(a);return true;}}
  else if(search(t,cap-costs[a])){chosen.push_back(a);return true;}
 }
 if(cap>1&&failed.size()<4000000)failed.insert(key);
 return false;
}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 ifstream in(argv[1]);int n,budget;in>>w>>n>>budget;
 if(!in||w<1||w>256||n<0||budget<0||budget>6)return 3;
 blocks=(w+63)/64;masks.resize(n);costs.resize(n);
 for(int a=0;a<n;++a){in>>costs[a];if(costs[a]<1||costs[a]>2)return 4;for(int b=0;b<blocks;++b)in>>masks[a][b];}if(!in)return 5;
 for(int level=1;level<=2;++level){hits[level].resize(w);order[level].resize(w);iota(order[level].begin(),order[level].end(),0);for(int a=0;a<n;++a)if(costs[a]<=level)for(int i=0;i<w;++i)if(masks[a][i/64]>>(i%64)&1)hits[level][i].push_back(a);sort(order[level].begin(),order[level].end(),[level](int a,int b){return hits[level][a].size()!=hits[level][b].size()?hits[level][a].size()<hits[level][b].size():a<b;});}
 M all{};for(int i=0;i<w;++i)all[i/64]|=uint64_t(1)<<(i%64);
 bool ok=search(all,budget);ofstream out(argv[2]);out<<(ok?"SAT":"UNSAT")<<'\n';for(int a:chosen)out<<a<<' ';out<<'\n'<<nodes<<' '<<failed.size()<<'\n';cout<<(ok?"SAT":"UNSAT")<<" nodes "<<nodes<<" states "<<failed.size()<<'\n';
}
