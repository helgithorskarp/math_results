// Exact conditional quadratic model for two ordinary QR617 residue columns.
// This is an objective evaluator, not a global existence/nonexistence solver.
#ifndef VDW_COLUMN_BLOCK12_HPP
#define VDW_COLUMN_BLOCK12_HPP
#include <array>
#include <algorithm>
#include <cstdint>
#include <stdexcept>

namespace vdw {
struct Cost {
    std::int64_t raw=0, weighted=0;
    Cost& operator+=(Cost rhs) { raw+=rhs.raw; weighted+=rhs.weighted; return *this; }
    Cost& operator-=(Cost rhs) { raw-=rhs.raw; weighted-=rhs.weighted; return *this; }
};
inline bool less(Cost a,Cost b) {
    return a.weighted<b.weighted || (a.weighted==b.weighted && a.raw<b.raw);
}
struct Minimum { bool feasible=false; unsigned mask=0; Cost value{}; };
struct Block12 {
    std::array<int,12> point{};
    std::array<Cost,12> linear{};
    std::array<std::array<Cost,6>,6> cross{};
    Block12(int r,int s) {
        if(r<2 || r>=617 || s<2 || s>=617 || r==s)
            throw std::invalid_argument("block requires two distinct residues in2..616");
        for(int k=0;k<6;++k) { point[k]=r+617*k; point[k+6]=s+617*k; }
    }
    Cost pair(int a,int b) const {
        if((a<6)==(b<6)) return {};
        return a<6?cross[a][b-6]:cross[b][a-6];
    }
    Cost evaluate(unsigned mask) const {
        if(mask>=4096) throw std::invalid_argument("non-12-bit mask");
        Cost result;
        for(int i=0;i<12;++i) if(mask&(1U<<i)) {
            result+=linear[i];
            for(int j=0;j<i;++j) if(mask&(1U<<j)) result+=pair(i,j);
        }
        return result;
    }
    template<class Visitor> void all(Visitor visit) const {
        unsigned previous=0; Cost value;
        visit(0U,value);
        for(unsigned index=1;index<4096;++index) {
            const unsigned mask=index^(index>>1), changed=mask^previous;
            int bit=0; while(!(changed&(1U<<bit))) ++bit;
            Cost change=linear[bit];
            for(int j=0;j<12;++j) if(j!=bit && (mask&(1U<<j))) change+=pair(bit,j);
            if(mask&changed) value+=change; else value-=change;
            visit(mask,value); previous=mask;
        }
    }
    // Exact minimum with optional forbidden flips and original-class edit
    // floors. Once the left column is fixed, the right objective is linear.
    // In final-edit variables its constraints reduce to one lower cardinality
    // bound, handled by choosing the cheapest permitted edited positions.
    Minimum minimum(const std::array<int,2>& classes,
                    const std::array<int,2>& outside,
                    const std::array<int,12>& edited,
                    unsigned allowed=4095U) const {
        if((classes[0]!=0 && classes[0]!=1) || (classes[1]!=0 && classes[1]!=1) ||
           outside[0]<0 || outside[1]<0 || allowed>=4096)
            throw std::invalid_argument("invalid edit-floor input");
        for(int e:edited) if(e!=0 && e!=1) throw std::invalid_argument("nonbinary edit flag");
        Minimum best;
        for(unsigned left=0;left<64;++left) {
            if(left&~allowed) continue;
            Cost base;
            auto fixed=outside;
            for(int i=0;i<6;++i) {
                if(left&(1U<<i)) base+=linear[i];
                fixed[classes[0]]+=edited[i]^static_cast<int>((left>>i)&1U);
            }
            const int right_class=classes[1];
            if(fixed[1-right_class]<30) continue;
            int required=std::max({0,30-fixed[right_class],65-fixed[0]-fixed[1]});
            struct Option { Cost change; int bit; };
            std::array<Option,6> options{};
            int size=0;
            unsigned mask=left;
            for(int j=0;j<6;++j) {
                Cost coefficient=linear[j+6];
                for(int i=0;i<6;++i) if(left&(1U<<i)) coefficient+=cross[i][j];
                if(!(allowed&(1U<<(j+6)))) {
                    required-=edited[j+6];
                    continue;
                }
                // Temporarily set final edited-status z_j=0, f_j=edited_j.
                if(edited[j+6]) { base+=coefficient; mask|=1U<<(j+6); }
                Cost change=coefficient;
                if(edited[j+6]) { change.raw=-change.raw; change.weighted=-change.weighted; }
                options[size++]={change,j+6};
            }
            if(required>size) continue;
            const auto cheaper=[](Option a,Option b) {
                return less(a.change,b.change) || (!less(b.change,a.change) && a.bit<b.bit);
            };
            for(int i=1;i<size;++i) {
                const auto value=options[i]; int j=i;
                while(j>0 && cheaper(value,options[j-1])) { options[j]=options[j-1]; --j; }
                options[j]=value;
            }
            for(int i=0;i<size;++i) if(i<required || less(options[i].change,Cost{})) {
                base+=options[i].change; mask^=1U<<options[i].bit;
            }
            if(!best.feasible || less(base,best.value) ||
               (!less(best.value,base) && mask<best.mask)) best={true,mask,base};
        }
        return best;
    }
};
}
#endif
