#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
using M=array<uint64_t,4>;struct K{M m;int k;bool operator==(const K&x)const{return m==x.m&&k==x.k;}};struct Hash{size_t operator()(const K&x)const{uint64_t h=x.k;for(auto v:x.m)h^=v+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);return h;}};
int blocks;bool empty(M x){for(int j=0;j<blocks;++j)if(x[j])return false;return true;}
int w;vector<M>H,P;vector<vector<int>>hits;vector<int>order,chosen;unordered_set<K,Hash>memo;uint64_t nodes=0,cache=0;M ALL;
M minusmask(M x,M y){for(int j=0;j<blocks;++j)x[j]&=~y[j];return x;}
bool cover(M r,int k){
 ++nodes;if(empty(r))return true;if(k==0)return false;K key{r,k};if(k>1&&memo.count(key)){++cache;return false;}
 int c=-1;for(int i:order)if((r[i/64]>>(i%64)&1)){c=i;break;}
 if(c<0)return false;
 for(int v:hits[c]){M t=minusmask(r,H[v]);if(k==1){if(empty(t)){chosen.push_back(v);return true;}}else if(cover(t,k-1)){chosen.push_back(v);return true;}}
 if(k>1&&memo.size()<4000000)memo.insert(key);
 return false;
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 ifstream in(argv[1]);int h,p;in>>w>>h>>p;if(!in||w<1||w>256||h<0||p<0)return 3;blocks=(w+63)/64;H.resize(h);P.resize(p);for(auto&m:H)for(int j=0;j<blocks;++j)in>>m[j];for(auto&m:P)for(int j=0;j<blocks;++j)in>>m[j];if(!in)return 4;
 for(int i=0;i<w;++i)ALL[i/64]|=uint64_t(1)<<(i%64);
 hits.resize(w);order.resize(w);iota(order.begin(),order.end(),0);
 for(int i=0;i<w;++i)for(int v=0;v<h;++v)if((H[v][i/64]>>(i%64)&1))hits[i].push_back(v);
 sort(order.begin(),order.end(),[](int a,int b){return hits[a].size()!=hits[b].size()?hits[a].size()<hits[b].size():a<b;});
 if(cover(ALL,6)){cout<<"SAT 0";for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}cout<<"closed 0 pairs nodes "<<nodes<<'\n'<<flush;
 for(int i=0;i<p;++i)if(cover(minusmask(ALL,P[i]),4)){cout<<"SAT 1 "<<i;for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}
 cout<<"closed 1 pair nodes "<<nodes<<'\n'<<flush;
 for(int i=0;i<p;++i)for(int j=0;j<i;++j)if(cover(minusmask(minusmask(ALL,P[i]),P[j]),2)){cout<<"SAT 2 "<<j<<' '<<i;for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}
 cout<<"closed 2 pairs nodes "<<nodes<<'\n'<<flush;
 for(int i=0;i<p;++i)for(int j=0;j<i;++j){M r=minusmask(minusmask(ALL,P[i]),P[j]);for(int k=0;k<j;++k)if(empty(minusmask(r,P[k]))){cout<<"SAT 3 "<<k<<' '<<j<<' '<<i<<'\n';return 10;}}
 cout<<"UNSAT nodes "<<nodes<<" cached "<<cache<<" states "<<memo.size()<<'\n';return 20;
}
