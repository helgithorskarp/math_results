// six-reviewer-4: fresh physical-neighbor census from the defining proof.
// C++17, unsigned 22-bit neighborhoods, no target code or data dependencies.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U = std::uint32_t;
constexpr U ALL=(U(1)<<22)-1;
int pc(U a){return __builtin_popcount(a);}
U bit(int i){return U(1)<<i;}
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
struct Graph {
  std::array<U,22> red{};
  void edge(int a,int b){need(a!=b,"loop");red[a]|=bit(b);red[b]|=bit(a);}
  U blue(int a,U universe=ALL)const{return universe&~(red[a]|bit(a));}
  bool cap(int a,int b)const{
    return red[a]&bit(b) ? pc(red[a]&red[b])<=3 : pc(blue(a)&blue(b))<=6;
  }
};
struct Interface {
  int r; std::array<int,5> low;
  std::array<int,6> c,beta; std::array<int,2> sy;
  Graph g; std::array<int,16> q;
};
std::vector<int> subsets(int rank){std::vector<int> v;for(int a=0;a<64;++a)if(pc(a)==rank)v.push_back(a);return v;}
void connect_mask(Graph&g,int row,int first,int mask,int count){for(int j=0;j<count;++j)if(mask&(1<<j))g.edge(row,first+j);}
Graph fixed(int r,bool sy_present){
  Graph g;g.edge(0,1);g.edge(0,2);g.edge(1,2);
  for(int i=3;i<=10;++i)g.edge(0,i);
  for(int t=13;t<=15;++t)g.edge(2,t);
  g.edge(2,9);g.edge(2,10);
  const std::array<int,6> cyc={0,4,3,1,2,5};
  for(int j=0;j<6;++j)g.edge(3+cyc[j],3+cyc[(j+1)%6]);
  g.edge(9,6);g.edge(9,8);g.edge(10,5);g.edge(10,7);
  connect_mask(g,9,13,r==0?6:5,3);connect_mask(g,10,13,r==0?5:6,3);
  if(sy_present){
    for(int s=11;s<=12;++s){g.edge(1,s);g.edge(2,s);}
    connect_mask(g,11,13,6,3);connect_mask(g,12,13,3,3);
  }
  return g;
}
bool projected_caps(const Graph&g,U known,const std::array<int,22>&degrees,int omitted){
  std::array<int,22> q{};
  for(int i=0;i<22;++i)if(known&bit(i)){
    q[i]=degrees[i]-pc(g.red[i]&known);
    if(q[i]<0||q[i]>omitted)return false;
  }
  for(int i=0;i<22;++i)if(known&bit(i))for(int j=i+1;j<22;++j)if(known&bit(j)){
    if(g.red[i]&bit(j)){
      if(pc(g.red[i]&g.red[j]&known)+std::max(0,q[i]+q[j]-omitted)>3)return false;
    }else{
      if(pc(g.blue(i,known)&g.blue(j,known))+std::max(0,omitted-q[i]-q[j])>6)return false;
    }
  }
  return true;
}
void key(std::ostream&o,const Interface&f){
  o<<f.r;
  for(int a:f.low)o<<' '<<a;
  for(int a:f.c)o<<' '<<a;
  for(int a:f.sy)o<<' '<<a;
  for(int a:f.beta)o<<' '<<a;
}
std::vector<Interface> interfaces(std::ostream&out,std::ostream&meta){
  std::vector<Interface> fs;
  const U known14=((U(1)<<16)-1)&~(bit(11)|bit(12));
  const U known16=(U(1)<<16)-1;
  std::array<int,6> c{};std::array<int,2> s{};
  const std::array<int,6> minimum={2,2,1,1,1,1};
  std::vector<int> sr;for(int a=0;a<64;++a)if(pc(a)==3||pc(a)==4)sr.push_back(a);
  for(int r=0;r<2;++r){
    std::uint64_t words=0,tagwords=0,screen14=0,sywords=0,rankwords=0,final=0;
    std::function<void(int)> go=[&](int pos){
      if(pos<6){for(int a=1;a<8;++a)if(pc(a)>=minimum[pos]){c[pos]=a;go(pos+1);}return;}
      ++words;std::array<int,5> low{};std::array<int,6> k{};
      for(int t=0;t<3;++t){int rank=0;for(int a:c)rank+=(a>>t)&1;low[t]=(t==2?3:4)-rank;if(low[t]<0||low[t]>1)return;}
      ++tagwords;
      for(int i=0;i<6;++i)k[i]=pc(c[i])-minimum[i];
      std::array<int,22> deg{};deg.fill(10);deg[2]=9;for(int t=0;t<3;++t)deg[13+t]-=low[t];
      Graph base=fixed(r,false);for(int i=0;i<6;++i)connect_mask(base,3+i,13,c[i],3);
      if(!projected_caps(base,known14,deg,8))return;
      ++screen14;
      for(int a:sr)for(int b:sr){
        ++sywords;s={a,b};low[3]=4-pc(a);low[4]=4-pc(b);
        int m=0;for(int l:low)m+=l;if(m>3)continue;
        std::array<int,6> beta{};bool ranks=true;
        for(int i=0;i<6;++i){beta[i]=2-k[i]-((a>>i)&1)-((b>>i)&1);if(beta[i]<0||beta[i]>2)ranks=false;}
        if(!ranks)continue;
        ++rankwords;int sum=0;for(int e:beta)sum+=e;need(sum==1+m,"cut/excess bridge");
        Graph g=fixed(r,true);for(int i=0;i<6;++i)connect_mask(g,3+i,13,c[i],3);
        connect_mask(g,11,3,a,6);connect_mask(g,12,3,b,6);
        deg[11]=10-low[3];deg[12]=10-low[4];
        if(!projected_caps(g,known16,deg,6))continue;
        Interface f{r,low,c,beta,s,g,{}};
        for(int i=0;i<16;++i)f.q[i]=deg[i]-pc(g.red[i]);
        need(f.q[0]==0&&f.q[1]==6&&f.q[2]==0,"root ranks");
        for(int i=0;i<6;++i)need(f.q[3+i]==3+beta[i],"ordinary rank");
        need(f.q[9]==4&&f.q[10]==4&&f.q[11]==2&&f.q[12]==2,"special ranks");
        need(f.q[13]==3&&f.q[14]==2&&f.q[15]==3,"T ranks");
        key(out,f);out<<'\n';fs.push_back(f);++final;
      }
    };go(0);
    meta<<"x "<<r<<' '<<words<<' '<<tagwords<<' '<<screen14<<' '<<sywords<<' '<<rankwords<<' '<<final<<'\n';
  }
  return fs;
}
const std::array<int,7> ep={9,10,11,12,13,14,15};
std::uint64_t frames=0,viable=0,tuples=0,compatible=0,joins=0;
int minbad=100000,maxbad=0,minexcess=100000,maxexcess=0;
void endpoints(const Interface&f,std::ostream&fo,std::ostream&jo){
  const auto tw=subsets(2),th=subsets(3);
  for(int b:{51,23}){
    Graph base=f.g;connect_mask(base,1,16,63,6);connect_mask(base,9,16,15,6);connect_mask(base,10,16,b,6);
    need(base.cap(9,10),"prototype pair");
    std::array<std::vector<int>,3> tr;
    for(int t=0;t<3;++t)for(int a:t==1?tw:th){Graph g=base;connect_mask(g,13+t,16,a,6);if(g.cap(13+t,9)&&g.cap(13+t,10))tr[t].push_back(a);}
    for(int t0:tr[0])for(int t1:tr[1])for(int t2:tr[2]){
      if((t0|t1|t2)!=63)continue;
      Graph tg=base;connect_mask(tg,13,16,t0,6);connect_mask(tg,14,16,t1,6);connect_mask(tg,15,16,t2,6);
      if(!tg.cap(13,14)||!tg.cap(13,15)||!tg.cap(14,15))continue;
      std::array<std::vector<int>,2> sr;
      for(int si=0;si<2;++si)for(int a:tw){Graph g=tg;connect_mask(g,11+si,16,a,6);bool ok=true;for(int p:{9,10,13,14,15})if(!g.cap(11+si,p))ok=false;if(ok)sr[si].push_back(a);}
      for(int sy0:sr[0])for(int sy1:sr[1]){
        Graph g=tg;connect_mask(g,11,16,sy0,6);connect_mask(g,12,16,sy1,6);if(!g.cap(11,12))continue;
        // Audit every endpoint pair, including the previously checked ones.
        for(int i=0;i<7;++i)for(int j=i+1;j<7;++j)need(g.cap(ep[i],ep[j]),"endpoint coverage");
        const std::array<int,7> rows={15,b,sy0,sy1,t0,t1,t2};
        ++frames;key(fo,f);for(int a:rows)fo<<' '<<a;fo<<'\n';
        std::array<std::vector<int>,6> candidates;
        for(int i=0;i<6;++i)for(int a:subsets(f.q[3+i])){
          Graph h=g;connect_mask(h,3+i,16,a,6);bool ok=true;for(int p:ep)if(!h.cap(3+i,p))ok=false;
          if(ok)candidates[i].push_back(a);
        }
        bool good=true;for(const auto&v:candidates)if(v.empty())good=false;if(!good)continue;++viable;
        std::array<std::array<std::array<std::array<bool,64>,64>,6>,6> cp{};
        // Values indexed by masks (0..63), avoiding candidate ordering assumptions.
        for(int i=0;i<6;++i)for(int j=i+1;j<6;++j)for(int a:candidates[i])for(int c:candidates[j]){
          Graph h=g;connect_mask(h,3+i,16,a,6);connect_mask(h,3+j,16,c,6);cp[i][j][a][c]=h.cap(3+i,3+j);
        }
        std::array<int,6> xrow{};
        std::function<void(int)> join=[&](int pos){
          if(pos<6){for(int a:candidates[pos]){xrow[pos]=a;join(pos+1);}return;}
          ++tuples;for(int i=0;i<6;++i)for(int j=i+1;j<6;++j)if(!cp[i][j][xrow[i]][xrow[j]])return;
          ++compatible;int lowq=0;std::array<int,6> qlow{};
          for(int y=0;y<6;++y){int d=5+((15>>y)&1)+((b>>y)&1);for(int a:xrow)d+=(a>>y)&1;if(d<9||d>10)return;qlow[y]=10-d;lowq+=qlow[y];}
          int m=0;for(int l:f.low)m+=l;if(lowq!=3-m)return;
          ++joins;Graph h=g;for(int i=0;i<6;++i)connect_mask(h,3+i,16,xrow[i],6);
          int bad=0,excess=0,firsti=-1,firstj=-1;U firstpages=0;
          // Q-internal edges are UNSPECIFIED. Only assigned red spines are inspected.
          for(int i=0;i<22;++i)for(int j=i+1;j<22;++j)if(h.red[i]&bit(j)){
            U pages=h.red[i]&h.red[j];int n=pc(pages);if(n>3){++bad;excess+=n-3;if(firsti<0){firsti=i;firstj=j;firstpages=pages;}}
          }
          need(firsti>=0,"surviving partial graph has no red book");
          minbad=std::min(minbad,bad);maxbad=std::max(maxbad,bad);minexcess=std::min(minexcess,excess);maxexcess=std::max(maxexcess,excess);
          key(jo,f);for(int a:rows)jo<<' '<<a;for(int a:xrow)jo<<' '<<a;for(int a:qlow)jo<<' '<<a;
          jo<<' '<<firsti<<' '<<firstj<<' '<<firstpages<<' '<<bad<<' '<<excess<<'\n';
        };join(0);
      }
    }
  }
}
int main(int argc,char**argv){
  try{
    need(argc==2,"usage: census OUTPUT_PREFIX");std::string p=argv[1];
    std::ofstream xo(p+"-x.txt"),fo(p+"-frames.txt"),jo(p+"-joins.txt"),meta(p+"-meta.txt");
    need(xo.good()&&fo.good()&&jo.good()&&meta.good(),"output paths");
    auto fs=interfaces(xo,meta);xo.close();
    for(const auto&f:fs)endpoints(f,fo,jo);
    meta<<"endpoint_frames "<<frames<<"\nnonempty_frames "<<viable<<"\ncartesian_tuples "<<tuples<<"\ncompatible_tuples "<<compatible<<"\njoins "<<joins
        <<"\nviolating_red_spines_min "<<minbad<<"\nviolating_red_spines_max "<<maxbad<<"\nred_page_excess_min "<<minexcess<<"\nred_page_excess_max "<<maxexcess<<'\n';
    need(xo.good()&&fo.good()&&jo.good()&&meta.good(),"output write");
    std::cout<<"complete "<<fs.size()<<' '<<frames<<' '<<viable<<' '<<tuples<<' '<<joins<<'\n';
    return 0;
  }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
