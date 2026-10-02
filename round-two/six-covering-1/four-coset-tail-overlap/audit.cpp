// Independent literal-residue audit. No Python producer or bit-slice code.
#include <algorithm>
#include <array>
#include <bitset>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <vector>
using Mask=std::bitset<180>;
using Family=std::vector<std::vector<Mask>>;
using Hist=std::array<int,10>;
void need(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
int top(Hist h){int left=111,total=0;for(int k=9;k>=0;--k){int n=std::min(left,h[k]);left-=n;total+=n*k;}need(!left,"short target");return total;}
int main(){try{
 std::vector<int> target;
 for(int x=0;x<720;++x)if(x%4==0&&x%9!=6)target.push_back(x/4);
 need(target.size()==160,"target size");
 const std::vector<int> labels{8,3,6,12,5,10,20,9,18,36,16};
 std::map<int,Family> families;
 std::map<int,int> caps;
 long raw=0,points=0,productive=0;
 for(int d=2;d<=720;++d)if(720%d==0){
  const bool selected=std::find(labels.begin(),labels.end(),d)!=labels.end();
  int effective;
  // Determine the image of multiplication by four directly; no gcd formula.
  std::vector<int> phases;
  for(int r=0;r<180;++r)if(std::find(phases.begin(),phases.end(),4*r%d)==phases.end())phases.push_back(4*r%d);
  effective=static_cast<int>(phases.size());
  need(180%effective==0,"projected period");
  if(selected)families[d]=Family(7,std::vector<Mask>(effective));
  std::vector<std::vector<int>> assigned(7,std::vector<int>(effective));
  int maximum=0;
  for(int a=0;a<7*d;++a){
   ++raw;Mask physical;
   for(int x=a;x<5040;x+=7*d){++points;if(x%4==0&&x%9!=6)physical.set((x%720)/4);}
   maximum=std::max(maximum,static_cast<int>(physical.count()));
   int r=-1;
   for(int v=0;v<effective;++v)if(4*v%d==a%d){need(r==-1,"duplicate projected phase");r=v;}
   if(r<0){need(physical.none(),"unproductive original phase hits target");continue;}
   ++productive;Mask expected;
   for(int t:target)if(4*t%d==a%d)expected.set(t);
   need(physical==expected,"original progression/projected phase mismatch");
   if(selected){families[d][a%7][r]=physical;++assigned[a%7][r];}
  }
  if(selected)for(const auto& row:assigned)for(int n:row)need(n==1,"incomplete original class family");
  caps[d]=maximum;
 }
 int free_mass=0,other_mass=0,other_count=0;
 for(const auto& [d,cap]:caps)if(d!=2&&d!=4){free_mass+=cap;if(std::find(labels.begin(),labels.end(),d)==labels.end()){other_mass+=cap;++other_count;}}
 need(free_mass==600&&other_mass==144&&other_count==16,"capacity inventory");
 // Enumerate every labeled five-copy map, then canonicalize first appearances.
 std::set<std::array<int,7>> allocations;
 for(int code=0;code<78125;++code){int n=code,next=0;std::array<int,5> name;name.fill(-1);std::array<int,7> p;
  for(int i=0;i<7;++i){int s=n%5;n/=5;if(name[s]<0)name[s]=next++;p[i]=name[s];}allocations.insert(p);
 }
 need(allocations.size()==855,"copy-map quotient");
 long phase_count=0,cases=0,active=0,active9=0,joint=0,critical=0,controls=0,ordered=0,original_controls=0;
 int max7=0,prune7=0,prune9=0,expanded=0,max_union=0,min_loss=100;
 std::set<std::vector<int>> critical_states,critical_phases;
 const Hist equality_hist{40,20,20,30,15,15,10,5,5,0};
 for(int b=0;b<2;++b)for(int a0=0;a0<3;++a0)for(int a1=a0;a1<3;++a1)for(int a2=a1;a2<3;++a2)
 for(int c0=0;c0<5;++c0)for(int c1=c0;c1<5;++c1)for(int c2=c1;c2<5;++c2){
  ++phase_count;std::array<int,7> phase{b,a0,a1,a2,c0,c1,c2};
  for(const auto& p:allocations){
   ++cases;std::array<Mask,5> Q;
   for(int i=0;i<7;++i)Q[p[i]]|=families.at(labels[i])[p[i]][phase[i]];
   std::array<int,180> w0{};Hist h0{};
   for(int t:target){for(int s=0;s<5;++s)w0[t]+=Q[s][t];++h0[w0[t]];}
   int score7=top(h0);max7=std::max(max7,score7);
   if(score7+100<411){prune7=std::max(prune7,score7+100);continue;}
   ++active;
   for(int s9=0;s9<5;++s9)for(int r9=0;r9<9;++r9){
    Mask V=families.at(9)[s9][r9]&~Q[s9];std::array<int,180> w9{};Hist h9{};
    for(int t:target){w9[t]=w0[t]+3*V[t];++h9[w9[t]];}
    int score9=top(h9);
    if(score9+40<411){prune9=std::max(prune9,score9+40);continue;}
    ++active9;
    for(int s4=0;s4<5;++s4)for(int r4=0;r4<4;++r4){
     Mask W=families.at(16)[s4][r4]&~Q[s4];Hist h{};std::array<int,180> w{};
     for(int t:target){w[t]=w9[t]+W[t];++h[w[t]];}
     int score=top(h);++joint;expanded=std::max(expanded,score);need(score<=411,"joint bound exceeded");
     if(score!=411)continue;
     ++critical;need(a0==a1&&a1==a2&&a0!=0&&c0==c1&&c1==c2,"equality phases");
     need(p[0]==0&&p[1]==1&&p[2]==2&&p[3]==3,"equality first allocation");
     auto last=std::array<int,3>{p[4],p[5],p[6]};std::sort(last.begin(),last.end());
     need(last==std::array<int,3>{1,2,3},"equality latter allocation");
     need(s9==4&&s4==4&&r9%3==a0&&r4%2==b&&h==equality_hist,"equality selector/histogram");
     Mask A=families.at(3)[0][a0],B=families.at(8)[0][b],C=families.at(5)[0][c0],U=A|B|C,mandatory,positive;
     for(int t:target){if(w[t]>=2)mandatory.set(t);if(w[t]>0)positive.set(t);}
     need(U.count()==120&&mandatory.count()==100&&positive==U&&(A&~mandatory).none()&&(W&~mandatory).none(),"mandatory equality support");
     need(Q[0]==B&&Q[1]==(A|C)&&Q[2]==(A|C)&&Q[3]==(A|C)&&Q[4].none(),"literal Q structure");
     std::vector<int> state(phase.begin(),phase.end());state.insert(state.end(),p.begin(),p.end());critical_states.insert(state);
     critical_phases.insert(std::vector<int>(phase.begin(),phase.end()));
     std::array<std::vector<int>,3> full9;
     for(int j=0;j<3;++j)for(int s=0;s<5;++s)for(int r=0;r<9;++r){
      int gain=static_cast<int>((families.at(labels[7+j])[s][r]&U&~Q[s]).count());
      ++original_controls;if(j==0)++controls;need(gain<=20,"nine gain ceiling");
      if(gain==20){need(s==4&&r%3==a0,"non-forced original nine selector");full9[j].push_back(r);}
     }
     std::vector<int> full4;
     for(int s=0;s<5;++s)for(int r=0;r<4;++r){
      int gain=static_cast<int>((families.at(16)[s][r]&U&~Q[s]).count());++controls;++original_controls;
      need(gain<=40,"four gain ceiling");if(gain==40){need(s==4&&r%2==b,"non-forced original four selector");full4.push_back(r);}
     }
     for(const auto& row:full9)need(row.size()==3,"full nine domain");need(full4.size()==2,"full four domain");
     for(int r:full9[0])for(int q:full9[1])for(int z:full9[2])for(int v:full4){
      Mask uni=families.at(9)[4][r]|families.at(18)[4][q]|families.at(36)[4][z]|families.at(16)[4][v];
      int size=static_cast<int>(uni.count());++ordered;max_union=std::max(max_union,size);min_loss=std::min(min_loss,100-size);
      need(size<=85,"physical equality overlap loss absent");
     }
    }
   }
  }
 }
 need(std::max({prune7,prune9,expanded})==411&&critical>0&&max_union==85&&min_loss==15,"boundary loss conclusion");
 // A separate literal first-stage audit for the82-point positive tail.
 Mask K;
 for(int t:target)if(t%3==1||(t%2==0&&t%5==0&&t%3!=1)||t%30==26||t%90==2||t==8||t==68||t==128||t==44)K.set(t);
 need(K.count()==82,"positive target definition");
 std::bitset<720> residual;
 for(int x=0;x<720;++x)if(x%8!=5&&x%9!=6&&x%18!=3&&!(x%4==0&&K[x/4]))residual.set(x);
 std::map<int,std::vector<std::bitset<720>>> first;
 for(int m=8;m<=720;++m)if(720%m==0&&m!=8&&m!=9){
  first[m]=std::vector<std::bitset<720>>(m);
  for(int a=0;a<m;++a)for(int x=a;x<720;x+=m)if(residual[x])first[m][a].set(x);
 }
 const std::array<std::array<int,2>,7> pairs{{{10,18},{12,15},{16,20},{24,30},{36,40},{45,48},{60,72}}};
 const std::array<int,8> singles{80,90,120,144,180,240,360,720};
 std::vector<int> group_capacities;long pair_checks=0,single_checks=0;int group_capacity=0;
 for(auto pair:pairs){int maximum=0;for(const auto& u:first.at(pair[0]))for(const auto& v:first.at(pair[1])){++pair_checks;maximum=std::max(maximum,static_cast<int>((u|v).count()));}group_capacity+=maximum;group_capacities.push_back(maximum);}
 for(int m:singles){int maximum=0;for(const auto& u:first.at(m)){++single_checks;maximum=std::max(maximum,static_cast<int>(u.count()));}group_capacity+=maximum;group_capacities.push_back(maximum);}
 need(residual.count()==448&&group_capacity==427&&group_capacity<static_cast<int>(residual.count()),"first-stage template does not have strict physical group bound");
 need(group_capacities==std::vector<int>{81,101,68,53,36,29,22,8,8,6,5,4,3,2,1},"physical first-stage group capacities");
 std::cout<<"{\"canonical_phase_multisets\":"<<phase_count<<",\"canonical_copy_partitions\":"<<allocations.size()
 <<",\"canonical_cases\":"<<cases<<",\"active_seven_profiles\":"<<active<<",\"pruned_seven_profiles\":"<<cases-active
 <<",\"nine_selectors_examined\":"<<45*active<<",\"active_nine_selectors\":"<<active9<<",\"pruned_nine_selectors\":"<<45*active-active9
 <<",\"joint_profiles\":"<<joint<<",\"maximum_seven_score\":"<<max7<<",\"maximum_pruned_seven_ceiling\":"<<prune7
 <<",\"maximum_pruned_nine_ceiling\":"<<prune9<<",\"maximum_expanded_joint_score\":"<<expanded
 <<",\"critical_joint_profiles\":"<<critical<<",\"critical_seven_profiles\":"<<critical_states.size()<<",\"critical_phase_multisets\":"<<critical_phases.size()
 <<",\"literal_equality_copy_phase_controls\":"<<controls<<",\"ordered_nine_and_four_equality_controls\":"<<ordered
 <<",\"maximum_equality_union_extra_hits\":"<<max_union<<",\"minimum_equality_overlap_loss\":"<<min_loss
 <<",\"other_resource_mass\":"<<other_mass<<",\"necessary_hole_upper_bound\":110"
 <<",\"positive_template_first_demand\":"<<residual.count()<<",\"positive_template_first_group_capacity\":"<<group_capacity<<",\"positive_template_raw_pair_checks\":"<<pair_checks<<",\"positive_template_singleton_phase_checks\":"<<single_checks
 <<",\"raw_original_phase_families\":"<<raw<<",\"literal_progression_points\":"<<points<<",\"original_equality_copy_phase_controls\":"<<original_controls<<"}\n";
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
