// Separate literal ORIGINAL-phase audit; no canonicalisation algorithm or LP.
#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using Mask=std::bitset<720>;
using Phases=std::array<int,6>;
const std::array<int,6> core={10,12,15,16,18,20};
const std::array<std::array<int,2>,8> pairs={{{24,30},{36,40},{45,48},{60,72},{80,90},{120,144},{180,240},{360,720}}};
const std::array<int,5> limits={34,34,34,34,27};
void need(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
int mod(int x,int n){int r=x%n;return r<0?r+n:r;}
std::uint64_t key(const Phases& p){std::uint64_t x=0;for(int a:p)x=(x<<5)|static_cast<unsigned>(a);return x;}
struct Row {Phases p{};int f=0,s=0,raw=0;std::array<int,8> cap{},accepted{};};
struct Data {
 Mask R,F,S;std::array<Mask,5>B;std::array<std::vector<Mask>,721> phase;
 Data(){
  for(int x=0;x<720;++x){
   bool r=x%8!=5&&x%9!=6&&x%18!=3;
   if(r){R.set(x);if(x%4){F.set(x);}else{S.set(x);}}
   if(x%4==0&&(x/4)%9!=6){
    int t=x/4;
    for(int p=0;p<2;++p)for(int b=1;b<=2;++b)if(t%2!=p&&t%3!=b)B[2*p+b-1].set(x);
    if(t%3==0)B[4].set(x);
   }
  }
  need(R.count()==530&&F.count()==370&&S.count()==160,"physical point sets differ");
  for(int m=8;m<=720;++m)if(720%m==0){
   phase[m].resize(m+1);
   for(int a=0;a<m;++a)for(int x=a;x<720;x+=m)if(R[x])phase[m][a].set(x);
  }
 }
 bool allowed(const Mask& mask)const{
  for(int i=0;i<5;++i)if((mask&B[i]).count()>static_cast<unsigned>(limits[i]))return false;
  return true;
 }
 Mask mask(const Phases& p)const{Mask out;for(int i=0;i<6;++i)out|=phase[core[i]][p[i]];return out;}
};
int point_map(int x,int u,int v,const std::array<int,5>& pi){
 int y=mod(u*(x%144)+v,144),f=pi[x%5];
 return y+144*mod(4*(f-y),5);
}
Mask permute_mask(const Mask& mask,const std::array<int,720>& map){Mask out;for(int x=0;x<720;++x)if(mask[x])out.set(map[x]);return out;}

int main(int argc,char** argv){try{
 need(argc==2,"usage: audit certificate.txt");std::ifstream input(argv[1]);need(bool(input),"certificate unreadable");
 int n=0;input>>n;need(n==14,"wrong canonical core count");std::vector<Row> rows(n);
 for(auto& row:rows){
  for(int i=0;i<6;++i){input>>row.p[i];need(row.p[i]>=0&&row.p[i]<core[i],"core phase outside ORIGINAL modulus");}
  input>>row.f>>row.s>>row.raw;
  for(int& c:row.cap)input>>c;
  for(int& a:row.accepted)input>>a;
  need(bool(input),"certificate missing integers");need(row.p[1]>0,"core12 phase0");
 }
 std::string trailing;need(!(input>>trailing),"unexpected certificate suffix");
 Data d;std::unordered_map<std::uint64_t,int> images;std::uint64_t progression_points=0,map_points=0,transport_controls=0;
 for(int k=0;k<12;++k)for(int e=0;e<2;++e){
  int u=1+12*k,v=36*(k%2)+72*e;std::array<int,5> pi={0,1,2,3,4};
  do{
   std::array<int,720> map{};std::bitset<720> seen;
   for(int x=0;x<720;++x){int y=point_map(x,u,v,pi);need(y>=0&&y<720&&!seen[y],"map not a permutation");map[x]=y;seen.set(y);++map_points;}
   need(permute_mask(d.R,map)==d.R&&permute_mask(d.F,map)==d.F&&permute_mask(d.S,map)==d.S,"map does not preserve physical sets");
   for(int b=0;b<5;++b){Mask target=permute_mask(d.B[b],map);bool match=false;
    for(int c=0;c<5;++c)if(limits[b]==limits[c]&&target==d.B[c])match=true;
    need(match,"map does not permute equal-cap targets");}
   // All ORIGINAL labels/phases under six physical generators.
   bool generator=(k==1&&e==0&&pi==std::array<int,5>{0,1,2,3,4})||
                  (k==0&&e==1&&pi==std::array<int,5>{0,1,2,3,4});
   if(k==0&&e==0){for(int s=0;s<4;++s){std::array<int,5> t={0,1,2,3,4};std::swap(t[s],t[s+1]);if(pi==t)generator=true;}}
   if(generator){for(int m=8;m<=720;++m)if(720%m==0)for(int a=0;a<m;++a){int newa=map[a]%m;
    for(int x=a;x<720;x+=m){need(map[x]%m==newa,"generator does not transport original class");++transport_controls;}}}
   for(int j=0;j<n;++j){Phases p{};
    for(int i=0;i<6;++i){p[i]=map[rows[j].p[i]]%core[i];
     for(int x=rows[j].p[i];x<720;x+=core[i]){need(map[x]%core[i]==p[i],"original core class transport fails");++progression_points;}}
    need(p[1]==rows[j].p[1],"original12 residue not fixed");
    Mask mask=d.mask(p);need(d.allowed(mask)&&(mask&d.F).count()>=204,"core image violates restrictions");
    auto [it,inserted]=images.emplace(key(p),j);need(inserted||it->second==j,"different core rows have intersecting symmetry orbits");
   }
  }while(std::next_permutation(pi.begin(),pi.end()));
 }
 need(map_points==2073600&&transport_controls==103680,"full physical map/generator inventory differs");
 need(images.size()==2560,"expanded symmetry cores differ in size");
 std::array<int,14> orbit_counts{};
 for(const auto& item:images)++orbit_counts[item.second];
 for(int j=0;j<n;++j){need(orbit_counts[j]==rows[j].raw,"literal expanded core orbit count differs");Mask m=d.mask(rows[j].p);
  need((m&d.F).count()==static_cast<unsigned>(rows[j].f)&&(m&d.S).count()==static_cast<unsigned>(rows[j].s),"core gain differs");}
 // Direct original phases, including omissions, independent of RGS/mask aliasing.
 std::uint64_t raw_visited=0,raw_accepted=0;std::unordered_set<std::uint64_t> found;
 for(int a=0;a<=10;++a)for(int b=1;b<12;++b){Mask m2=d.phase[10][a]|d.phase[12][b];
  for(int c=0;c<=15;++c){Mask m3=m2|d.phase[15][c];
   for(int f=0;f<=16;++f){Mask m4=m3|d.phase[16][f];
    for(int g=0;g<=18;++g){Mask m5=m4|d.phase[18][g];
     for(int h=0;h<=20;++h){++raw_visited;Mask mask=m5|d.phase[20][h];
      if((mask&d.F).count()<204||!d.allowed(mask))continue;
      Phases p={a,b,c,f,g,h};for(int i=0;i<6;++i)need(p[i]<core[i],"admissible original core resource omitted");
      ++raw_accepted;need(images.count(key(p))==1,"raw admissible core not in14 symmetry orbits");found.insert(key(p));
 }}}}}
 need(raw_visited==13131888&&raw_accepted==2560&&found.size()==images.size(),"raw original core inventory incomplete");
 std::uint64_t pair_tuples=0;
 for(int j=0;j<n;++j){Mask cmask=d.mask(rows[j].p),target=d.F&~cmask;int total=0;
  for(int t=0;t<8;++t){int m=pairs[t][0],f=pairs[t][1],best=-1,accepted=0;
   for(int a=0;a<=m;++a)for(int b=0;b<=f;++b){++pair_tuples;Mask pair=d.phase[m][a]|d.phase[f][b];
    if(!d.allowed(cmask|pair)){continue;}
    ++accepted;
    best=std::max(best,static_cast<int>((pair&target).count()));}
   need(best==rows[j].cap[t]&&accepted==rows[j].accepted[t],"direct original pair maximum/count differs");total+=best;
  }
  need(total<static_cast<int>(target.count()),"core is not strictly excluded");
 }
 std::cout<<"{\"status\":\"RAW_ORIGINAL_CORE_AND_PAIR_AUDIT_PASSED\",\"raw_core_visited\":"<<raw_visited
          <<",\"raw_core_accepted\":"<<raw_accepted<<",\"canonical_cores\":14,\"pair_tuples\":"<<pair_tuples
          <<",\"map_points\":"<<map_points<<",\"transport_controls\":"<<transport_controls
          <<",\"core_progression_points\":"<<progression_points<<",\"all14_strict_exclusions\":true}"<<'\n';
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
