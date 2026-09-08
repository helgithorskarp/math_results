#include <array>
#include <bitset>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
constexpr int M=632, W=10;
int main(int argc,char**argv){
 if(argc!=3) return 2;
 ifstream f(argv[1]); ofstream out(argv[2]);
 int n,e,k; if(!(f>>n>>e>>k)||n!=516||e!=2538||k!=53276)return 3;
 vector<int> labels(n); for(int &v:labels)f>>v;
 vector<pair<int,int>> edges(e); for(auto &a:edges)f>>a.first>>a.second;
 long long bad=0,good=0;
 for(int s=0;s<k;s++){
  array<int,M> map; for(int v=0;v<M;v++)map[v]=v;
  for(int j=0;j<4;j++){int c,u,v;f>>c>>u>>v;map[c]=-1;map[v]=u;}
  vector<int> active; for(int v:labels)if(map[v]==v)active.push_back(v);
  if(active.size()!=508)return 4;
  array<array<uint64_t,W>,M> a{};
  for(auto [x,y]:edges){int u=map[x],v=map[y];if(u<0||v<0)continue;if(u==v)return 5;
   a[u][v/64]|=uint64_t(1)<<(v%64);a[v][u/64]|=uint64_t(1)<<(u%64);}
  array<int,5> witness{}; bool found=false;
  for(size_t i=0;i<active.size()&&!found;i++)for(size_t j=i+1;j<active.size()&&!found;j++){
   int u=active[i],v=active[j],cnt=0;array<int,3> common{};
   for(int b=0;b<W && cnt<3;b++){
    uint64_t bits=a[u][b]&a[v][b];
    while(bits&&cnt<3){common[cnt++]=64*b+__builtin_ctzll(bits);bits&=bits-1;}
   }
   if(cnt==3){witness={u,v,common[0],common[1],common[2]};found=true;}
  }
  if(found){out<<witness[0]<<' '<<witness[1]<<' '<<witness[2]<<' '<<witness[3]<<' '<<witness[4]<<'\n';bad++;}
  else {out<<"-1\n";good++;}
 }
 string trailing;if(f>>trailing)return 6;
 cerr<<"cases "<<k<<" K23 "<<bad<<" survivors "<<good<<'\n';
}
