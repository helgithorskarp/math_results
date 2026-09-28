// Deterministic bounded local search. Search scores are not mathematical
// certificates; check.py validates the committed strings from the definition.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
struct RNG { uint64_t s; uint64_t next(){ uint64_t z=(s+=0x9e3779b97f4a7c15ULL); z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; return z^(z>>31); } int get(int n){return int(next()%uint64_t(n));} };
// x <= y and x+y=z. The representation includes x=y explicitly.
struct Edge {short x,y,z;};
struct Search {
 int n,k; vector<Edge> e; vector<vector<int>> inc; vector<int> col, bad, pos; RNG rng; long long steps=0; int best=INT32_MAX; vector<int> best_col;
 Search(int n_,int k_,uint64_t seed):n(n_),k(k_),inc(n_+1),col(n_+1),rng{seed} {
  // Store an edge once per unordered pair, and an incidence once per distinct
  // vertex. Thus x+x=2x has two incidences, not three.
  for(int x=1;x<=n;++x)for(int y=x;x+y<=n;++y){int z=x+y,id=e.size();e.push_back({short(x),short(y),short(z)});inc[x].push_back(id);if(y!=x)inc[y].push_back(id);inc[z].push_back(id);}
  pos.assign(e.size(),-1);
 }
 bool mono(int i)const{auto [x,y,z]=e[i];return col[x]==col[y]&&col[x]==col[z];}
 void add_bad(int i){pos[i]=bad.size();bad.push_back(i);}
 void remove_bad(int i){int p=pos[i],last=bad.back();bad[p]=last;pos[last]=p;bad.pop_back();pos[i]=-1;}
 void reset(const vector<int>& source,int extra,int perturb){
  col=source;col[n]=extra;
  for(int i=0;i<perturb;++i){int v=1+rng.get(n);col[v]=rng.get(k);}
  bad.clear();fill(pos.begin(),pos.end(),-1);for(int i=0;i<(int)e.size();++i)if(mono(i))add_bad(i);
  update_best();
 }
 void update_best(){if((int)bad.size()<best){best=bad.size();best_col=col;cout<<"BEST steps="<<steps<<" cost="<<best<<"\n"<<flush;}}
 // If changing v to a colour would make edge i monochromatic, return that
 // colour; otherwise return -1. The doubling case has just one other vertex.
 int others(int i,int v)const{
  auto [x,y,z]=e[i];
  if(x==y)return v==x?col[z]:col[x];
  if(v==x)return col[y]==col[z]?col[y]:-1;
  if(v==y)return col[x]==col[z]?col[x]:-1;
  return col[x]==col[y]?col[x]:-1;
 }
 array<int,6> potential(int v)const{
  array<int,6> cnt{};
  for(int id:inc[v]){int d=others(id,v);if(d>=0)++cnt[d];}
  return cnt;
 }
 void flip(int v,int d){
  col[v]=d;
  for(int id:inc[v]){bool now=mono(id);if(now&&pos[id]<0)add_bad(id);else if(!now&&pos[id]>=0)remove_bad(id);}
  ++steps;update_best();
 }
 void run(const vector<int>& source,int repeats,int per_restart,int kick,int noise_percent,int tabu_tenure){
  vector<long long> last(n+1,-1000000000LL);
  for(int rep=0;rep<repeats&&best>0;++rep){
   bool fresh=(rep%10==0);
   int extra=fresh?source[n]:best_col[n];
   reset(fresh?source:best_col,extra,rep==0?0:kick);
   fill(last.begin(),last.end(),-1000000000LL);
   for(int t=0;t<per_restart&&best>0;++t){
    if(bad.empty())break;
    auto [x,y,z]=e[bad[rng.get((int)bad.size())]];
    int vertices[3]={x,y,z};int nv=x==y?2:3;if(x==y)vertices[1]=z;
    int best_delta=INT32_MAX,chosen_v=-1,chosen_d=-1, ties=0;
    bool noisy=rng.get(100)<noise_percent;
    if(noisy){int v=vertices[rng.get(nv)],d=rng.get(k-1);if(d>=col[v])++d;chosen_v=v;chosen_d=d;}
    else{
     for(int a=0;a<nv;++a){int v=vertices[a];if(steps-last[v]<=tabu_tenure)continue;auto cnt=potential(v);for(int d=0;d<k;++d)if(d!=col[v]){
      int delta=cnt[d]-cnt[col[v]];
      if(delta<best_delta){best_delta=delta;chosen_v=v;chosen_d=d;ties=1;}
      else if(delta==best_delta&&rng.get(++ties)==0){chosen_v=v;chosen_d=d;}
     }}
     if(chosen_v<0){int v=vertices[rng.get(nv)],d=rng.get(k-1);if(d>=col[v])++d;chosen_v=v;chosen_d=d;}
    }
    flip(chosen_v,chosen_d);last[chosen_v]=steps;
   }
   cout<<"RESTART "<<rep<<" current="<<bad.size()<<" best="<<best<<"\n"<<flush;
  }
  cout<<"FINAL steps="<<steps<<" best="<<best<<"\n";
  {cout<<"BEST_COLOR ";for(int i=1;i<=n;++i)cout<<best_col[i]+1;cout<<"\n";}
 }
};
int main(int argc,char**argv){
 if(argc!=9){cerr<<"usage: schur_walk baseline n seed restarts steps_per_restart kick noise_percent tabu_tenure\n";return 2;}
 string baseline=argv[1];int n=stoi(argv[2]);uint64_t seed=stoull(argv[3]);int restarts=stoi(argv[4]),each=stoi(argv[5]),kick=stoi(argv[6]),noise=stoi(argv[7]),tabu=stoi(argv[8]);
 if(n<2||n>1000||restarts<1||each<1||noise<0||noise>100||tabu<0)throw runtime_error("invalid args");
 ifstream in(baseline);string digits;in>>digits;if((int)digits.size()!=n-1&&(int)digits.size()!=n)throw runtime_error("expected n-1 or n digits");
 vector<int> base(n+1);for(int i=1;i<=(int)digits.size();++i){if(digits[i-1]<'1'||digits[i-1]>'6')throw runtime_error("bad baseline digit");base[i]=digits[i-1]-'1';}if((int)digits.size()==n-1)base[n]=4;
 Search search(n,6,seed);search.run(base,restarts,each,kick,noise,tabu);
}
