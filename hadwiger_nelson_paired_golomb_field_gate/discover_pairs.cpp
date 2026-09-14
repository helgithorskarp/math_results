#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <algorithm>
#include <string>
#include <unordered_map>
#include <cstdint>
using U=uint32_t;using V=uint64_t;
struct Answer{std::string word;int status;};
long long nodes;std::array<int,18>colour;std::array<U,18>adj;
bool rec(std::array<U,18>d,U live){if(++nodes>1000000)return false;if(!live)return true;
int v=-1,best=5,deg=-1;for(int i=0;i<18;i++)if(live>>i&1){int n=__builtin_popcount(d[i]),k=__builtin_popcount(adj[i]&live);if(n<best||(n==best&&k>deg)){v=i;best=n;deg=k;}}
if(best==0)return false;
U options=d[v];while(options){U bit=options&-options;options-=bit;auto dd=d;U nbr=adj[v]&live;while(nbr){int j=__builtin_ctz(nbr);nbr&=nbr-1;dd[j]&=~bit;}colour[v]=__builtin_ctz(bit);if(rec(dd,live&~(1U<<v)))return true;if(nodes>1000000)return false;}return false;}
int main(int argc,char**argv){if(argc!=3)return 2;std::ifstream f(argv[1]);int n,e,k;f>>n>>e>>k;if(!f||n<9||n>100000||e<0||k<1||k>20000)return 2;
std::vector<U>dom(n);for(auto&x:dom){f>>x;if(!f||x>15)return 2;}
std::vector<std::vector<int>>g(n),own(n);for(int i=0;i<e;i++){int a,b;f>>a>>b;if(!f||a<0||a>=b||b>=n)return 2;g[a].push_back(b);g[b].push_back(a);}for(auto&v:g)std::sort(v.begin(),v.end());
std::vector<std::vector<int>>copies(k,std::vector<int>(9));for(int c=0;c<k;c++)for(auto&x:copies[c]){f>>x;if(!f||x<0||x>=n)return 2;own[x].push_back(c);}for(auto&v:copies)if(!std::is_sorted(v.begin(),v.end())||std::adjacent_find(v.begin(),v.end())!=v.end())return 2;
int blocks=(k+63)/64;std::vector<std::vector<V>>pairs(k,std::vector<V>(blocks));
auto connect=[&](int a,int b){if(a==b)return;if(a>b)std::swap(a,b);pairs[a][b/64]|=1ULL<<(b%64);};
for(int v=0;v<n;v++){for(auto a:own[v])for(auto b:own[v])connect(a,b);for(auto u:g[v])if(v<u)for(auto a:own[v])for(auto b:own[u])connect(a,b);}
std::unordered_map<std::string,int>cache;std::vector<Answer>ans;std::ofstream templates(std::string(argv[2])+"_templates.txt"),results(std::string(argv[2])+"_pairs.txt"),bad(std::string(argv[2])+"_obstructions.txt");
long long tested=0,sat=0,unsat=0,unknown=0,totalnodes=0;int maxn=0;std::array<long long,19>sizes{};
auto query=[&](int a,int b){std::vector<int>vs=copies[a];if(b>=0){vs.insert(vs.end(),copies[b].begin(),copies[b].end());std::sort(vs.begin(),vs.end());vs.erase(std::unique(vs.begin(),vs.end()),vs.end());}int m=vs.size();if(m>18)throw 2;
std::array<U,18>d{};adj.fill(0);std::string key(1,static_cast<char>(m));for(int i=0;i<m;i++){d[i]=dom[vs[i]];key.push_back(static_cast<char>(d[i]));for(int j=0;j<i;j++)if(std::binary_search(g[vs[i]].begin(),g[vs[i]].end(),vs[j])){adj[i]|=1U<<j;adj[j]|=1U<<i;}}
for(int i=0;i<m;i++)for(int s=0;s<3;s++)key.push_back(static_cast<char>((adj[i]>>(8*s))&255));
int id;auto it=cache.find(key);if(it!=cache.end())id=it->second;else{nodes=0;colour.fill(-1);bool ok=rec(d,(1U<<m)-1);int status=ok?1:(nodes>1000000?-1:0);std::string word;
if(ok){for(int i=0;i<m;i++)word.push_back('0'+colour[i]);}
id=ans.size();ans.push_back({word,status});cache.emplace(key,id);totalnodes+=nodes;templates<<id<<' '<<m<<' '<<status<<' '<<(ok?word:"-");for(int i=0;i<m;i++)templates<<' '<<d[i];for(int i=0;i<m;i++)templates<<' '<<adj[i];templates<<'\n';}
auto z=ans[id];if(z.status==1){for(int i=0;i<m;i++){int c=z.word[i]-'0';if(!(d[i]>>c&1))throw 3;for(int j=0;j<i;j++)if((adj[i]>>j&1)&&z.word[i]==z.word[j])throw 4;}sat++;}else if(z.status==0){unsat++;bad<<a<<' '<<b<<' '<<id<<'\n';}else{unknown++;bad<<a<<' '<<b<<' '<<id<<" UNKNOWN\n";}
results<<a<<' '<<b<<' '<<id<<'\n';tested++;sizes[m]++;maxn=std::max(maxn,m);};
for(int a=0;a<k;a++)query(a,-1);
for(int a=0;a<k;a++){for(int b=a+1;b<k;b++)if(pairs[a][b/64]>>(b%64)&1)query(a,b);if(a%250==0)std::cerr<<"at "<<a<<" tested "<<tested<<" SAT "<<sat<<" UNSAT_LIST "<<unsat<<" UNKNOWN "<<unknown<<" templates "<<ans.size()<<'\n';}
std::cerr<<"DONE tested "<<tested<<" SAT "<<sat<<" UNSAT_LIST "<<unsat<<" UNKNOWN "<<unknown<<" templates "<<ans.size()<<" nodes "<<totalnodes<<" maxn "<<maxn<<'\n';for(int i=0;i<=18;i++)if(sizes[i])std::cerr<<"SIZE "<<i<<' '<<sizes[i]<<'\n';return unknown?5:0;}
