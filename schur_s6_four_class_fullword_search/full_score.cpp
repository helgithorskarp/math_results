// Exploratory full-score search for a classical 537-colouring.
// All unordered triples, including doubling, are scored at every state.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
struct RNG {
 uint64_t s;
 uint64_t next() { uint64_t z=(s+=0x9e3779b97f4a7c15ULL); z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; return z^(z>>31); }
 int get(int n) { return int(next()%uint64_t(n)); }
};
struct Edge { short x,y,z; };
struct Search {
 int n=537, best=INT32_MAX;
 long long steps=0;
 vector<Edge> edges;
 vector<vector<int>> incidence;
 vector<int> colour, best_colour, weight, bad, position;
 RNG rng;
 Search(uint64_t seed): incidence(n+1),colour(n+1),rng{seed} {
  for(int x=1;x<=n;++x)for(int y=x;x+y<=n;++y){
   int id=edges.size(),z=x+y;edges.push_back({short(x),short(y),short(z)});
   incidence[x].push_back(id);if(y!=x)incidence[y].push_back(id);incidence[z].push_back(id);
  }
  weight.assign(edges.size(),1);position.assign(edges.size(),-1);
 }
 bool legal(int v,int d) const { return d!=colour[v]; }
 bool mono(int id) const { auto [x,y,z]=edges[id];return colour[x]==colour[y]&&colour[x]==colour[z]; }
 int other_colour(int id,int v) const {
  auto [x,y,z]=edges[id];int vertices[3]={x,y,z},other=-1;
  for(int u:vertices)if(u!=v){if(other<0)other=colour[u];else if(other!=colour[u])return -1;}
  return other;
 }
 array<int,6> potential(int v) const {
  array<int,6> p{};
  for(int id:incidence[v]) {int d=other_colour(id,v);if(d>=0)p[d]+=weight[id];}
  return p;
 }
 void add_bad(int id) {position[id]=bad.size();bad.push_back(id);}
 void remove_bad(int id) {int p=position[id],last=bad.back();bad[p]=last;position[last]=p;bad.pop_back();position[id]=-1;}
 void flip(int v,int d) {
  if(!legal(v,d))throw runtime_error("same-colour flip");
  colour[v]=d;
  for(int id:incidence[v]) {
   bool now=mono(id);
   if(now&&position[id]<0)add_bad(id);
   if(!now&&position[id]>=0)remove_bad(id);
  }
  ++steps;
  if(int(bad.size())<best){best=bad.size();best_colour=colour;cout<<"BEST steps="<<steps<<" defects="<<best<<"\n"<<flush;}
 }
 int count_all() const {
  int count=0;
  for(int x=1;x<=n;++x)for(int y=x;x+y<=n;++y)
   count+=colour[x]==colour[y]&&colour[x]==colour[x+y];
  return count;
 }
 void initialize(const vector<int>&source,int kick) {
  colour=source;
  fill(weight.begin(),weight.end(),1);
  for(int t=0;t<kick;++t){
   int v=1+rng.get(n),choices[6],length=0;
   for(int d=0;d<6;++d)if(legal(v,d))choices[length++]=d;
   colour[v]=choices[rng.get(length)];
  }
  bad.clear();fill(position.begin(),position.end(),-1);
  for(int id=0;id<int(edges.size());++id)if(mono(id))add_bad(id);
  if(count_all()!=int(bad.size()))throw runtime_error("initial defect mismatch");
  if(int(bad.size())<best){best=bad.size();best_colour=colour;cout<<"BEST steps="<<steps<<" defects="<<best<<"\n"<<flush;}
 }
 void run(const vector<int>&source,int restarts,int per_restart,int kick,int global_noise,int local_noise,int tabu) {
  vector<long long> last(n+1,-1000000000LL);
  for(int rep=0;rep<restarts&&best>0;++rep){
   bool fresh=(rep%10==0);
   initialize(fresh?source:best_colour,rep==0?0:(fresh?kick*2:kick));
   fill(last.begin(),last.end(),-1000000000LL);
   for(int t=0;t<per_restart&&best>0;++t){
    int chosen_v=-1,chosen_d=-1;
    bool global=rng.get(100)<global_noise;
    if(global){
     int v=1+rng.get(n),opts[6],length=0;
     for(int d=0;d<6;++d)if(legal(v,d))opts[length++]=d;
     chosen_v=v;chosen_d=opts[rng.get(length)];
    } else {
     auto [x,y,z]=edges[bad[rng.get(int(bad.size()))]];
     int vertices[3]={x,y,z};
     bool noisy=rng.get(100)<local_noise;
     if(noisy){
      int v=vertices[rng.get(3)],opts[6],length=0;
      for(int d=0;d<6;++d)if(legal(v,d))opts[length++]=d;
      chosen_v=v;chosen_d=opts[rng.get(length)];
     } else {
      int value=INT32_MAX,ties=0;
      for(int v:vertices){
       if(steps-last[v]<=tabu)continue;
       auto p=potential(v);
       for(int d=0;d<6;++d)if(legal(v,d)){
        int delta=p[d]-p[colour[v]];
        if(delta<value){value=delta;chosen_v=v;chosen_d=d;ties=1;}
        else if(delta==value&&rng.get(++ties)==0){chosen_v=v;chosen_d=d;}
       }
      }
      if(chosen_v<0){
       int v=vertices[rng.get(3)],opts[6],length=0;
       for(int d=0;d<6;++d)if(legal(v,d))opts[length++]=d;
       chosen_v=v;chosen_d=opts[rng.get(length)];
      }
     }
    }
    flip(chosen_v,chosen_d);last[chosen_v]=steps;
    if(t%500==499){for(int id:bad)weight[id]=min(weight[id]+1,100);}
    if(t%10000==9999){for(int &w:weight)w=max(1,w-1);}
   }
   cout<<"RESTART "<<rep<<" current="<<bad.size()<<" best="<<best<<"\n"<<flush;
  }
  colour=best_colour;
  cout<<"FINAL steps="<<steps<<" defects="<<best<<" direct="<<count_all()<<"\n";
  cout<<"BEST_COLOR ";for(int i=1;i<=n;++i)cout<<best_colour[i]+1;cout<<"\n";
 }
};
int main(int argc,char **argv){
 if(argc!=9){cerr<<"usage: executable 537word seed restarts steps kick global_noise local_noise tabu\n";return 2;}
 ifstream in(argv[1]);string digits;in>>digits;
 if(digits.size()!=537||digits.find_first_not_of("123456")!=string::npos)throw runtime_error("invalid input word");
 vector<int> source(538);for(int i=1;i<=537;++i)source[i]=digits[i-1]-'1';
 Search search(stoull(argv[2]));
 search.run(source,stoi(argv[3]),stoi(argv[4]),stoi(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]));
}
