#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
using M=array<uint64_t,2>;
int n,w;M all;vector<int> fv,db;vector<vector<int>> adj;vector<uint8_t> edge;vector<M> mask;
array<int,6>s{},par{};int shape;array<uint64_t,6> visits{},valid{},hits{};
bool linked(int a,int b){return edge[size_t(a)*n+b]!=0;}
bool order_ok(int k){
 // Canonicalize automorphisms of each spanning tree, independently of vertex-set ESU.
 if(shape==0&&k>=2&&s[k]<s[k-1])return false; // star: leaves increasing
 if(shape==1&&k==5&&s[5]<s[0])return false; // path orientation
 if(shape==2&&k>=4&&s[k]<s[k-1])return false; // broom: three short leaves
 if(shape==3&&((k==1&&s[1]<s[0])||(k==3&&s[3]<s[2])||(k==5&&s[5]<s[4])))return false;
 if(shape==4&&k==5&&s[5]<s[4])return false; // arms 3,1,1
 if(shape==5&&k==3&&s[3]<s[1])return false; // arms 2,2,1
 return true;
}
void dfs(int k,M m){
 if(k==6){++visits[shape];for(int v:s){int d=db[v];for(int u:s)d+=linked(u,v);if(d<4)return;}++valid[shape];if(m==all){++hits[shape];for(int v:s)cerr<<v<<' ';cerr<<'\n';}return;}
 for(int v:adj[s[par[k]]]){
  bool used=false;for(int j=0;j<k;++j)if(s[j]==v){used=true;break;}if(used)continue;s[k]=v;if(!order_ok(k))continue;
  bool possible=true;for(int j=0;j<=k;++j){int d=db[s[j]];for(int z=0;z<=k;++z)d+=linked(s[j],s[z]);if(d+5-k<4){possible=false;break;}}if(!possible)continue;
  dfs(k+1,{m[0]|mask[v][0],m[1]|mask[v][1]});
 }
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 ifstream in(argv[1]);int f;in>>n>>f>>w;if(!in||n<1||n>10000||w<1||w>128)return 3;
 all={w>=64?~uint64_t(0):(uint64_t(1)<<w)-1,w<=64?0:(w==128?~uint64_t(0):(uint64_t(1)<<(w-64))-1)};
 db.resize(n);adj.resize(n);mask.resize(n);edge.assign(size_t(n)*n,0);
 for(int j=0;j<f;++j){int v,d,t;uint64_t a,b;in>>v>>d>>a>>b>>t;if(!in||v<0||v>=n||t<0||t>=n)return 4;fv.push_back(v);db[v]=d;mask[v]={a,b};for(int l=0;l<t;++l){int u;in>>u;if(!in||u<0||u>=n)return 5;adj[v].push_back(u);edge[size_t(v)*n+u]=1;}}
 array<array<int,6>,6> parents{{{{-1,0,0,0,0,0}},{{-1,0,1,2,3,4}},{{-1,0,1,0,0,0}},{{-1,0,0,0,1,1}},{{-1,0,1,2,0,0}},{{-1,0,1,0,3,0}}}};
 for(shape=0;shape<6;++shape){par=parents[shape];int roots=0;for(int v:fv){s[0]=v;dfs(1,mask[v]);if(++roots%500==0)cerr<<"shape "<<shape<<" roots "<<roots<<" qualified "<<valid[shape]<<'\n';}cout<<shape<<' '<<visits[shape]<<' '<<valid[shape]<<' '<<hits[shape]<<'\n'<<flush;}
 for(auto h:hits)if(h)return 10;
}
