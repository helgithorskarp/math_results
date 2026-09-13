#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int n,w;uint64_t all0,all1;vector<int>fv,db;vector<vector<int>>adj;vector<uint8_t>edge;vector<array<uint64_t,2>>mask;vector<uint64_t>three,four;array<uint64_t,3>valid5{};
bool E(int a,int b){return edge[size_t(a)*n+b]!=0;}
void check(array<int,5>s,int k,int tree){
 for(int i=0;i<k;++i)for(int j=0;j<i;++j)if(s[i]==s[j])return;
 for(int i=0;i<k;++i){int d=db[s[i]];for(int j=0;j<k;++j)if(E(s[i],s[j]))++d;if(d<4)return;}
 if(k==5){++valid5[tree];uint64_t a=0,b=0;for(int v:s){a|=mask[v][0];b|=mask[v][1];}if(a==all0&&b==all1){cerr<<"uncovered group";for(int v:s)cerr<<' '<<v;cerr<<'\n';exit(7);}return;}
 for(int i=1;i<k;++i){for(int j=i;j>0&&s[j]<s[j-1];--j)swap(s[j],s[j-1]);}
 uint64_t code=0;for(int i=0;i<k;++i)code|=uint64_t(s[i])<<(12*i);(k==3?three:four).push_back(code);
}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 ifstream in(argv[1]);int f;in>>n>>f>>w;if(!in||n<=0||n>4096||w<=0||w>128)return 3;
 all0=w>=64?~uint64_t(0):(uint64_t(1)<<w)-1;all1=w<=64?0:(w==128?~uint64_t(0):(uint64_t(1)<<(w-64))-1);
 adj.resize(n);db.resize(n);mask.resize(n);edge.assign(size_t(n)*n,0);
 for(int j=0;j<f;++j){int v,t;uint64_t a,b;in>>v;if(v<0||v>=n)return 4;in>>db[v]>>a>>b>>t;mask[v]={a,b};fv.push_back(v);for(int l=0;l<t;++l){int u;in>>u;if(!in||u<0||u>=n)return 5;adj[v].push_back(u);edge[size_t(v)*n+u]=1;}}
 for(int a:fv){
  const auto&N=adj[a];
  for(size_t i=0;i<N.size();++i)for(size_t j=0;j<i;++j){
   int b=N[i],c=N[j];check({a,b,c,0,0},3,0);
   for(size_t h=0;h<j;++h){int d=N[h];check({a,b,c,d,0},4,0);for(size_t l=0;l<h;++l)check({a,b,c,d,N[l]},5,0);}
   for(int d:N)if(d!=b&&d!=c)for(int e:adj[d])if(e!=a&&e!=b&&e!=c)check({a,b,c,d,e},5,1);
  }
  for(int b:N)for(int c:adj[b])if(c!=a)for(int d:adj[c])if(d!=a&&d!=b){
   if(a<d)check({a,b,c,d,0},4,0);
   for(int e:adj[d])if(e!=a&&e!=b&&e!=c&&a<e)check({a,b,c,d,e},5,2);
  }
 }
 for(int k:{3,4}){auto&v=k==3?three:four;sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());ofstream out(string(argv[2])+"-"+to_string(k)+".txt");for(uint64_t c:v){for(int j=0;j<k;++j)out<<((c>>(12*j))&4095)<<' ';out<<'\n';}cout<<"unique "<<k<<' '<<v.size()<<'\n';}
 cout<<"qualified five-point spanning-tree maps "<<valid5[0]<<' '<<valid5[1]<<' '<<valid5[2]<<'\n';
}
