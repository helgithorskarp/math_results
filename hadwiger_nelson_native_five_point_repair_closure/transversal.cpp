#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <unordered_set>
#include <vector>
using namespace std;
struct M{uint64_t a,b;};struct K{uint64_t a,b;int k;bool operator==(const K&x)const{return a==x.a&&b==x.b&&k==x.k;}};struct Hash{size_t operator()(const K&x)const{return size_t(x.a^(x.b+0x9e3779b97f4a7c15ULL+(x.a<<6)+(x.a>>2))^(uint64_t(x.k)*0x9e3779b97f4a7c15ULL));}};
int w;vector<M>H,P;vector<vector<int>>hits;vector<int>order,chosen;unordered_set<K,Hash>memo;uint64_t nodes=0,cache=0;M ALL;
M minusmask(M x,M y){return {x.a&~y.a,x.b&~y.b};}
bool cover(M r,int k){
 ++nodes;if(!r.a&&!r.b)return true;if(k==0)return false;K key{r.a,r.b,k};if(k>1&&memo.count(key)){++cache;return false;}
 int c=-1;for(int i:order)if(i<64?(r.a>>i&1):(r.b>>(i-64)&1)){c=i;break;}
 if(c<0)return false;
 for(int v:hits[c]){M t=minusmask(r,H[v]);if(k==1){if(!t.a&&!t.b){chosen.push_back(v);return true;}}else if(cover(t,k-1)){chosen.push_back(v);return true;}}
 if(k>1)memo.insert(key);
 return false;
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 ifstream in(argv[1]);int h,p;in>>w>>h>>p;if(!in||w<1||w>128||h<0||p<0)return 3;H.resize(h);P.resize(p);for(auto&m:H)in>>m.a>>m.b;for(auto&m:P)in>>m.a>>m.b;if(!in)return 4;
 ALL={w>=64?~uint64_t(0):(uint64_t(1)<<w)-1,w<=64?0:(w==128?~uint64_t(0):(uint64_t(1)<<(w-64))-1)};hits.resize(w);order.resize(w);iota(order.begin(),order.end(),0);
 for(int i=0;i<w;++i)for(int v=0;v<h;++v)if(i<64?(H[v].a>>i&1):(H[v].b>>(i-64)&1))hits[i].push_back(v);
 sort(order.begin(),order.end(),[](int a,int b){return hits[a].size()!=hits[b].size()?hits[a].size()<hits[b].size():a<b;});
 if(cover(ALL,5)){cout<<"SAT 0";for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}cout<<"closed 0 pairs nodes "<<nodes<<'\n'<<flush;
 for(int i=0;i<p;++i)if(cover(minusmask(ALL,P[i]),3)){cout<<"SAT 1 "<<i;for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}
 cout<<"closed 1 pair nodes "<<nodes<<'\n'<<flush;
 for(int i=0;i<p;++i)for(int j=0;j<i;++j)if(cover(minusmask(minusmask(ALL,P[i]),P[j]),1)){cout<<"SAT 2 "<<j<<' '<<i;for(int v:chosen)cout<<' '<<v;cout<<'\n';return 10;}
 cout<<"NO_COVER nodes "<<nodes<<" cached "<<cache<<" states "<<memo.size()<<'\n';return 0;
}
