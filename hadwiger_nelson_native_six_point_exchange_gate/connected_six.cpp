#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int n,w; uint64_t all0,all1; vector<int> freev,db; vector<vector<int>> adj; vector<uint8_t> edge; vector<array<uint64_t,2>> mask; array<uint64_t,7> visits{},valid{},kept{}; array<ofstream,7> out;
bool linked(int a,int b){return edge[size_t(a)*n+b]!=0;}
void emit(const vector<int>&s,int k){auto v=s;sort(v.begin(),v.end());for(int a:v)out[k]<<a<<' ';out[k]<<'\n';++kept[k];}
void dfs(vector<int>&s,vector<int> ext,uint64_t m0,uint64_t m1){
 int k=int(s.size());++visits[k];bool ok=true;
 for(int v:s){int d=db[v];for(int u:s)if(linked(v,u))++d;if(d<4)ok=false;if(d+6-k<4)return;}
 if(ok){++valid[k];if(k==6&&(m0==all0&&m1==all1))emit(s,k);}
 if(k==6)return;
 while(!ext.empty()){
  int v=ext.back();ext.pop_back();vector<int> next=ext;
  for(int u:adj[v])if(u>s[0]){
   bool seen=false;for(int z:s)if(u==z||linked(u,z)){seen=true;break;}
   if(!seen)next.push_back(u);
  }
  s.push_back(v);dfs(s,move(next),m0|mask[v][0],m1|mask[v][1]);s.pop_back();
 }
}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 ifstream in(argv[1]);int f;in>>n>>f>>w;
 if(!in||n<1||n>10000||w<1||w>128)return 3;
 all0=w>=64?~uint64_t(0):(uint64_t(1)<<w)-1;all1=w<=64?0:(w==128?~uint64_t(0):(uint64_t(1)<<(w-64))-1);
 db.resize(n);adj.resize(n);mask.resize(n);edge.assign(size_t(n)*n,0);
 for(int j=0;j<f;++j){int v,d,t;uint64_t a,b;in>>v>>d>>a>>b>>t;if(!in||v<0||v>=n||t<0||t>=n)return 4;freev.push_back(v);db[v]=d;mask[v]={a,b};for(int l=0;l<t;++l){int u;in>>u;if(!in||u<0||u>=n)return 5;adj[v].push_back(u);edge[size_t(v)*n+u]=1;}}
 for(int k=1;k<=6;++k){out[k].open(string(argv[2])+"-"+to_string(k)+".txt");if(!out[k])return 6;}
 int i=0;for(int v:freev){vector<int>s{v},ex;for(int u:adj[v])if(u>v)ex.push_back(u);dfs(s,move(ex),mask[v][0],mask[v][1]);if(++i%200==0){cerr<<"roots "<<i<<" visits6 "<<visits[6]<<" valid6 "<<valid[6]<<" kept6 "<<kept[6]<<'\n';}}
 for(int k=1;k<=6;++k)cout<<k<<' '<<visits[k]<<' '<<valid[k]<<' '<<kept[k]<<'\n';
}
