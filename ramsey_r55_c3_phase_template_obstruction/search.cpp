// Exact finite-domain event objective and a bounded heuristic phase search.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
namespace fs=std::filesystem;
constexpr int N=43;
void need(bool b,const std::string& s){if(!b)throw std::runtime_error(s);}
using Graph=std::array<std::array<int,N>,N>;
Graph read(const fs::path& p){
 std::ifstream f(p);need(bool(f),"input");int n;need(bool(f>>n)&&n==43,"order");
 Graph a{};int u,v,prev=-1;
 while(f>>u){need(bool(f>>v),"pair arity");need(0<=u&&u<v&&v<N,"pair range");
  int key=N*u+v;need(key>prev,"canonical pairs");prev=key;a[u][v]=a[v][u]=1;}
 need(f.eof(),"input parse");
 for(int x=0;x<N;++x)for(int y=x+1;y<N;++y){
  int gx=x==42?42:3*(x/3)+(x+1)%3,gy=y==42?42:3*(y/3)+(y+1)%3;
  need(a[x][y]==a[gx][gy],"C3 action");
  if(y<42&&x/3==y/3)need(a[x][y]==int(x<21),"internal colors");}
 return a;
}
void save(const fs::path& p,const std::string& s){auto t=p.string()+".tmp";std::ofstream f(t);need(bool(f),"output");f<<s;f.close();need(bool(f),"close");fs::rename(t,p);}
struct Event{
 std::array<int,10> v{},mask{};int n=0,weight=1;
 bool operator<(const Event& e)const {if(n!=e.n)return n<e.n;if(v!=e.v)return v<e.v;return mask<e.mask;}
};
struct Model{
 Graph base;int nv=0;std::array<std::array<int,14>,14> id{};
 std::vector<std::array<int,2>> pairs;std::vector<int> count,initial;
 std::vector<Event> events;std::vector<std::vector<int>> occur;
 explicit Model(const Graph& a):base(a){
  for(auto& r:id)r.fill(-1);
  for(int i=0;i<14;++i)for(int j=i+1;j<14;++j){
   int c=0;for(int t=0;t<3;++t)c+=a[3*i][3*j+t];
   if(c==1||c==2){id[i][j]=nv++;pairs.push_back({i,j});count.push_back(c);
    int minority=c==1?1:0,phase=-1;for(int t=0;t<3;++t)if(a[3*i][3*j+t]==minority)phase=t;
    need(phase>=0,"minority phase");initial.push_back(phase);}}
  occur.resize(nv);std::vector<Event> raw;
  for(int a0=0;a0<N;++a0)for(int b=a0+1;b<N;++b)for(int c=b+1;c<N;++c)
  for(int d=c+1;d<N;++d)for(int e=d+1;e<N;++e){
   std::array<int,5> q{a0,b,c,d,e};
   for(int color=0;color<2;++color){Event ev;bool possible=true;
    for(int r=0;r<5&&possible;++r)for(int s=r+1;s<5;++s){
     int u=q[r],v=q[s],k=v<42?id[u/3][v/3]:-1;
     if(k<0){if(a[u][v]!=color){possible=false;break;}continue;}
     int t=(v%3-u%3+3)%3,m=color==(count[k]==1?1:0)?1<<t:7^(1<<t);
     int z=0;while(z<ev.n&&ev.v[z]!=k)++z;
     if(z==ev.n){need(ev.n<10,"event width");ev.v[z]=k;ev.mask[z]=7;++ev.n;}
     ev.mask[z]&=m;if(!ev.mask[z]){possible=false;break;}
    }
    if(!possible)continue;
    need(ev.n>0,"frozen monochromatic five-set");
    for(int r=1;r<ev.n;++r){int v=ev.v[r],m=ev.mask[r],s=r;while(s>0&&ev.v[s-1]>v){ev.v[s]=ev.v[s-1];ev.mask[s]=ev.mask[s-1];--s;}ev.v[s]=v;ev.mask[s]=m;}
    raw.push_back(ev);
   }
  }
  std::sort(raw.begin(),raw.end());for(const auto& e:raw){if(!events.empty()&&!(events.back()<e)&&!(e<events.back()))++events.back().weight;else events.push_back(e);}
  for(int i=0;i<int(events.size());++i)for(int j=0;j<events[i].n;++j)occur[events[i].v[j]].push_back(i);
 }
 Graph graph(const std::vector<int>& x)const{need(int(x.size())==nv,"phase length");Graph a=base;
  for(int k=0;k<nv;++k){need(0<=x[k]&&x[k]<3,"phase digit");auto [i,j]=pairs[k];
   for(int s=0;s<3;++s)for(int t=0;t<3;++t){int r=(t-s+3)%3;a[3*i+s][3*j+t]=a[3*j+t][3*i+s]=count[k]==1?int(r==x[k]):int(r!=x[k]);}}
  return a;}
};
std::string word(const std::vector<int>& x){std::string s;for(int d:x)s+=char('0'+d);return s;}
void edges(const fs::path& p,const Graph& a){std::string s="43\n";for(int u=0;u<N;++u)for(int v=u+1;v<N;++v)if(a[u][v])s+=std::to_string(u)+" "+std::to_string(v)+"\n";save(p,s);}
struct Random{std::uint64_t state;std::uint64_t next(){auto z=(state+=UINT64_C(0x9e3779b97f4a7c15));z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb);return z^(z>>31);}int pick(int n){need(n>0,"empty choice");return int(next()%unsigned(n));}};
struct State{
 const Model& m;std::vector<int> x,viol,xors,bad,pos;std::vector<std::array<int,3>> gain;int score=0;
 State(const Model& a,const std::vector<int>& b):m(a),x(b),viol(a.events.size()),xors(a.events.size()),pos(a.events.size(),-1),gain(a.nv){
  for(int i=0;i<int(m.events.size());++i){const auto& e=m.events[i];for(int j=0;j<e.n;++j)if(!(e.mask[j]&(1<<x[e.v[j]]))){++viol[i];xors[i]^=e.v[j];}update(i,1);}}
 void update(int i,int sign){const auto& e=m.events[i];
  if(viol[i]==0){score+=sign*e.weight;
   if(sign==1){pos[i]=int(bad.size());bad.push_back(i);}else{int p=pos[i],last=bad.back();bad[p]=last;pos[last]=p;bad.pop_back();pos[i]=-1;}
   for(int j=0;j<e.n;++j)for(int t=0;t<3;++t)if(!(e.mask[j]&(1<<t)))gain[e.v[j]][t]-=sign*e.weight;
  }else if(viol[i]==1){int v=xors[i],j=0;while(j<e.n&&e.v[j]!=v)++j;need(j<e.n,"unique violation");for(int t=0;t<3;++t)if(e.mask[j]&(1<<t))gain[v][t]+=sign*e.weight;}}
 void move(int v,int t){need(v>=0&&v<m.nv&&t>=0&&t<3&&x[v]!=t,"move");int expected=score+gain[v][t];
  for(int i:m.occur[v]){const auto& e=m.events[i];int j=0;while(j<e.n&&e.v[j]!=v)++j;need(j<e.n,"occurrence index");
   const int old_value=x[v];
   const int old_allowed=(e.mask[j]>>old_value)&1;
   const int new_allowed=(e.mask[j]>>t)&1;
   if(old_allowed==new_allowed)continue;
   if(viol[i]<=1){update(i,-1);}
   viol[i]+=old_allowed-new_allowed;xors[i]^=v;
   if(viol[i]<=1){update(i,1);}}
  x[v]=t;need(score==expected,"gain score expected "+std::to_string(expected)+" got "+std::to_string(score));need(score>=0&&score<=962598&&score%3==0,"score range/divisibility "+std::to_string(score));}
 void check()const{State b(m,x);need(score==b.score&&gain==b.gain&&viol==b.viol&&xors==b.xors,"state drift");auto l=bad,r=b.bad;std::sort(l.begin(),l.end());std::sort(r.begin(),r.end());need(l==r,"bad drift");for(int i=0;i<int(bad.size());++i)need(pos[bad[i]]==i,"bad position");for(int v=0;v<m.nv;++v)need(gain[v][x[v]]==0,"current gain");}
};
int main(int argc,char** argv){try{
 need(argc==7,"usage: search INPUT OUT RESTARTS STEPS SEED INTERVAL");Graph a=read(argv[1]);fs::path out=argv[2];int restarts=std::stoi(argv[3]),steps=std::stoi(argv[4]),interval=std::stoi(argv[6]);auto seed=std::stoull(argv[5]);need(restarts>0&&restarts<=1000&&steps>0&&steps<=1000000&&interval>0,"limits");need(!fs::exists(out),"fresh output required");fs::create_directories(out);auto start=std::chrono::steady_clock::now();Model m(a);need(m.nv>0,"no free phases");
 save(out/"model.json","{\"variables\":"+std::to_string(m.nv)+",\"events\":"+std::to_string(m.events.size())+"}\n");
 std::string records="restart\tseed\tinitial\tbest\tbest_step\tsteps_done\tphases\n";int overall=std::numeric_limits<int>::max();
 for(int r=0;r<restarts;++r){if(fs::exists(out/"STOP")){save(out/"status.json","{\"complete\":false,\"stopped\":true}\n");return 0;}
  Random rng{seed+unsigned(r)};auto x=m.initial;if(r)for(int& v:x)v=rng.pick(3);State s(m,x);int initial=s.score,best=s.score,bs=0,done=0;auto bx=x;std::vector<int> last(m.nv,-100);
  for(int step=1;step<=steps&&s.score>0;++step){int v=-1,t=-1,delta=std::numeric_limits<int>::max();std::vector<std::array<int,2>> ties;
   if(rng.pick(100)==0){v=rng.pick(m.nv);t=(s.x[v]+1+rng.pick(2))%3;}
   else{for(int k=0;k<m.nv;++k)for(int z=0;z<3;++z){if(z==s.x[k])continue;int d=s.gain[k][z];if(step-last[k]<=7&&s.score+d>=best)continue;if(d<delta){delta=d;ties.clear();}if(d==delta)ties.push_back({k,z});}
    need(!ties.empty(),"no move");auto p=ties[rng.pick(int(ties.size()))];v=p[0];t=p[1];
    if(delta>=0&&rng.pick(100)<20){const auto& e=m.events[s.bad[rng.pick(int(s.bad.size()))]];int j=rng.pick(e.n);v=e.v[j];std::vector<int> options;for(int z=0;z<3;++z)if(!(e.mask[j]&(1<<z)))options.push_back(z);t=options[rng.pick(int(options.size()))];}}
   s.move(v,t);last[v]=step;done=step;if(step%interval==0)s.check();if(s.score<best){best=s.score;bs=step;bx=s.x;}}
  s.check();State b(m,bx);need(b.score==best,"best score");records+=std::to_string(r)+"\t"+std::to_string(seed+unsigned(r))+"\t"+std::to_string(initial)+"\t"+std::to_string(best)+"\t"+std::to_string(bs)+"\t"+std::to_string(done)+"\t"+word(bx)+"\n";save(out/"restarts.tsv",records);if(best<overall){overall=best;edges(out/"best.edges",m.graph(bx));}std::cout<<r<<" initial "<<initial<<" best "<<best<<" step "<<bs<<std::endl;
  if(best==0){save(out/"status.json","{\"complete\":false,\"candidate_target\":true}\n");return 0;}}
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();save(out/"status.json","{\"complete\":true,\"candidate_target\":false,\"seconds\":"+std::to_string(sec)+"}\n");
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}return 0;}
