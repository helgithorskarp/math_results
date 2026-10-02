// Different complete literal-AP, labeled-copy quotient, direct-weight audit.
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
using Hist=std::array<int,11>;
void need(bool ok,const char* s){if(!ok)throw std::runtime_error(s);}
int top(const Hist& h){int left=117,score=0;for(int k=10;k>=0;--k){int n=std::min(left,h[k]);left-=n;score+=n*k;}need(left==0,"short literal target");return score;}
int main(){try{
 std::vector<int> target;for(int x=0;x<720;++x)if(x%4==3&&x%9!=6)target.push_back((x-3)/4);
 need(target.size()==160,"literal S3 support");
 const std::vector<int> chosen_labels{8,3,6,12,5,10,20,9,18,36,16};
 std::map<int,Family> families;std::map<int,int> capacity;
 long original_phases=0,original_points=0,productive_phase_checks=0;
 for(int d=2;d<=720;++d)if(720%d==0){
  std::vector<int> visible;for(int t=0;t<180;++t)if(std::find(visible.begin(),visible.end(),(4*t+3)%d)==visible.end())visible.push_back((4*t+3)%d);
  int effective=static_cast<int>(visible.size());need(180%effective==0,"literal projected period");
  bool chosen=std::find(chosen_labels.begin(),chosen_labels.end(),d)!=chosen_labels.end();
  std::vector<std::vector<int>> assigned(7,std::vector<int>(effective));
  if(chosen)families[d]=Family(7,std::vector<Mask>(effective));
  int maximum=0;
  for(int a=0;a<7*d;++a){
   ++original_phases;Mask literal;
   for(int x=a;x<5040;x+=7*d){++original_points;if(x%4==3&&x%9!=6)literal.set((x%720-3)/4);}
   maximum=std::max(maximum,static_cast<int>(literal.count()));
   int r=-1;for(int t=0;t<effective;++t)if((4*t+3)%d==a%d){need(r==-1,"nonunique visible original phase");r=t;}
   if(r<0){need(literal.none(),"invisible original phase hits S");continue;}
   ++productive_phase_checks;
   Mask expected;for(int t:target)if((4*t+3)%d==a%d)expected.set(t);
   need(literal==expected,"literal original AP differs from projected family");
   if(chosen){families[d][a%7][r]=literal;++assigned[a%7][r];}
  }
  if(chosen)for(const auto& row:assigned)for(int count:row)need(count==1,"missing original visible phase");
  capacity[d]=maximum;
 }
 int total=0,other=0,other_count=0;
 for(const auto& [d,c]:capacity)if(d!=2&&d!=4){total+=c;if(std::find(chosen_labels.begin(),chosen_labels.end(),d)==chosen_labels.end()){other+=c;++other_count;}}
 need(total==600&&other==144&&other_count==16,"complete original resource capacities");
 std::set<std::array<int,7>> parts;
 for(int code=0;code<78125;++code){int n=code,next=0;std::array<int,5> names;names.fill(-1);std::array<int,7> p;
  for(int j=0;j<7;++j){int s=n%5;n/=5;if(names[s]<0)names[s]=next++;p[j]=names[s];}parts.insert(p);
 }
 need(parts.size()==855,"all labeled-copy maps quotient");
 long phases=0,cases=0,active=0,active9=0,joint=0,equalities=0,full_controls=0,ordered=0;
 int max7=0,prune7=0,prune9=0,expanded=0,max_union=0,min_loss=80;
 std::set<std::vector<int>> equality_states,equality_phases;
 const Hist equality_hist{8,36,36,6,29,36,9,0,0,0,0};
 for(int b=0;b<2;++b)for(int a0=0;a0<3;++a0)for(int a1=a0;a1<3;++a1)for(int a2=a1;a2<3;++a2)
 for(int c0=0;c0<5;++c0)for(int c1=c0;c1<5;++c1)for(int c2=c1;c2<5;++c2){
  ++phases;std::array<int,7> phase{b,a0,a1,a2,c0,c1,c2};
  for(const auto& p:parts){
   ++cases;std::array<Mask,5> Q;
   for(int j=0;j<7;++j)Q[p[j]]|=families.at(chosen_labels[j])[p[j]+2][phase[j]];
   std::array<int,180> w0{};Hist h0{};
   for(int t:target){for(const auto& q:Q)w0[t]+=q[t];++h0[w0[t]];}
   int base=top(h0);max7=std::max(max7,base);
   if(base+120<441){prune7=std::max(prune7,base+120);continue;}++active;
   for(int s9=0;s9<5;++s9)for(int r9=0;r9<9;++r9){
    Mask V=families.at(9)[s9+2][r9]&~Q[s9];std::array<int,180> w9{};Hist h9{};
    for(int t:target){w9[t]=w0[t]+4*V[t];++h9[w9[t]];}
    int score9=top(h9);if(score9+40<441){prune9=std::max(prune9,score9+40);continue;}++active9;
    for(int s4=0;s4<5;++s4)for(int r4=0;r4<4;++r4){
     Mask W=families.at(16)[s4+2][r4]&~Q[s4];Hist hist{};std::array<int,180> w{};
     for(int t:target){w[t]=w9[t]+W[t];++hist[w[t]];}
     int score=top(hist);++joint;expanded=std::max(expanded,score);need(score<=441,"literal majorizer exceeds441");
     if(score!=441)continue;
     ++equalities;need(a0==a1&&a1==a2&&a0!=0&&c0<c1&&c1<c2,"literal equality phases");
     need(p==std::array<int,7>{0,1,2,3,4,4,4},"literal equality allocations");
     need(s9>=1&&s9<=3&&r9%3!=a0&&r9!=3&&s4==0&&r4%2!=b&&hist==equality_hist,"literal equality selector/histogram");
     Mask mandatory,optional;for(int t:target){if(w[t]>=2)mandatory.set(t);else if(w[t]==1)optional.set(t);}
     need(mandatory.count()==116&&optional.count()==36,"literal equality117 mandatory/optional support");
     std::vector<int> state(phase.begin(),phase.end());state.insert(state.end(),p.begin(),p.end());equality_states.insert(state);
     equality_phases.insert(std::vector<int>(phase.begin(),phase.end()));
     // Separate all three real fine9 original labels and the virtual63 label.
     std::array<std::vector<std::array<int,2>>,4> full;
     const std::array<int,4> labels{9,18,36,9};
     for(int j=0;j<4;++j)for(int s=0;s<5;++s)for(int r=0;r<9;++r){
      Mask candidate=families.at(labels[j])[s+2][r]&~Q[s];
      int possible=static_cast<int>((candidate&mandatory).count())+std::min(1,static_cast<int>((candidate&optional).count()));
      ++full_controls;need(possible<=20,"literal fine9 possible gain exceeds20");if(possible==20)full[j].push_back({s,r});
     }
     const std::vector<std::array<int,2>> expected{{1,r9},{2,r9},{3,r9}};
     for(const auto& f:full)need(f==expected,"original full20 domain not forced");
     for(const auto& aa:full[0])for(const auto& bb:full[1])for(const auto& cc:full[2])for(const auto& dd:full[3]){
      const std::array<std::array<int,2>,4> choices{aa,bb,cc,dd};std::array<Mask,5> union_hits;
      for(int j=0;j<4;++j){int s=choices[j][0],r=choices[j][1];union_hits[s]|=families.at(labels[j])[s+2][r]&~Q[s];}
      int count=0;for(const auto& hits:union_hits)count+=static_cast<int>(hits.count());++ordered;
      need(count<=60,"four literal resources avoid compulsory overlap");max_union=std::max(max_union,count);min_loss=std::min(min_loss,80-count);
     }
    }
   }
  }
 }
 need(cases==598500&&equalities==1200&&equality_states.size()==40&&equality_phases.size()==40,"complete equality census differs");
 need(std::max({prune7,prune9,expanded})==441&&max_union==60&&min_loss==20,"virtual9 subset117 excluded");
 std::cout<<"{\"status\":\"DIFFERENT_LITERAL_VIRTUAL9_UPPER116_AUDIT_PASSED\",\"target_K\":117,\"threshold\":441"
  <<",\"original_phase_checks\":"<<original_phases<<",\"original_progression_points\":"<<original_points
  <<",\"productive_original_phase_checks\":"<<productive_phase_checks<<",\"physical_total_capacity\":"<<total<<",\"other_resource_capacity\":"<<other
  <<",\"canonical_phases\":"<<phases<<",\"copy_partitions\":"<<parts.size()<<",\"canonical_cases\":"<<cases
  <<",\"active_seven\":"<<active<<",\"V_selectors\":"<<45*active<<",\"active_V\":"<<active9<<",\"joint_profiles\":"<<joint
  <<",\"max_seven_score\":"<<max7<<",\"pruned_seven_ceiling\":"<<prune7<<",\"pruned_V_ceiling\":"<<prune9<<",\"max_expanded_score\":"<<expanded
  <<",\"all_cases_ceiling\":441,\"at_or_above_threshold\":"<<equalities<<",\"equality_seven_states\":"<<equality_states.size()<<",\"equality_phase_states\":"<<equality_phases.size()
  <<",\"equality_full9_controls\":"<<full_controls<<",\"ordered_four_resource_controls\":"<<ordered
  <<",\"equality_max_extra_union\":"<<max_union<<",\"equality_min_overlap_loss\":"<<min_loss<<",\"equality117_excluded\":true,\"implied_K_upper\":116}\n";
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
