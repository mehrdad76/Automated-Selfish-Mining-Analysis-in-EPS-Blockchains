dtmc
const double x = 0.3;
const double y = 0.5;
const double cq = 0.3759765625;
const int d = 4;
const int w = 5;


// n is total number of private adv. blocks
formula n = (n0+n1+n2+n3+n4+n5+n6);
formula total = (n*x+1);

module SelfishMiningChia

	// ni is the number of private blocks at level i
	n0 : [0..w] init 0;
	n1 : [0..w] init 0;
	n2 : [0..w] init 0;
	n3 : [0..w] init 0;
	n4 : [0..w] init 0;
	n5 : [0..w] init 0;
	n6 : [0..w] init 0;

	// h is the lead of the adv
	h : [0..d] init 0;

	// c is the number of adv branches in a race condition
	c : [0..w] init 0;

	// rewards
	adv : [0..2] init 0;
	honest : [0..2] init 0;


	[] h=0 & c=0 -> x : (n0'=1) & (h'=1) & (adv'=0) & (honest'=0) +
			(1-x) : (adv'=0) & (honest'=1); //DONE!


	[] h=1 & c=0 -> x/total : (n0'=min(w,n0+1)) & (adv'=0) & (honest'=0)  +
			n0*x/total : (n1'=1) & (h'=2) & (adv'=0) & (honest'=0)  +
			(1-x)/total : (c'=n0) & (n0'=0) & (h'=0) & (adv'=0) & (honest'=0) ;


	[] c>0 & h=0 -> (x*c)/(x*c+1-x) : (c'=0) & (adv'=2) & (honest'=0) +
			(1-x)*y/(x*c+1-x) : (c'=0) & (adv'=1) & (honest'=1) +
			(1-x)*(1-y)/(x*c+1-x) : (c'=0) & (adv'=0) & (honest'=2);


	[] h=2 & c=0 -> (1-x)/total : (n0'=0) & (n1'=0) & (n2'=0) & (n3'=0) & (n4'=0) & (n5'=0) & (n6'=0) & (h'=0) & (adv'=2) & (honest'=0) +
			x/total : (n0'=min(w,n0+1)) & (adv'=0) & (honest'=0) +
			n0*x/total : (n1'=min(w,n1+1)) & (adv'=0) & (honest'=0) +
			n1*x/total : (n2'=min(w,n2+1)) & (h'=h+1-min(1,n2)) & (adv'=0) & (honest'=0) +
			n2*x/total : (n3'=min(w,n3+1)) & (h'=h+1-min(1,n3)) & (adv'=0) & (honest'=0) +
			n3*x/total : (n4'=min(w,n4+1)) & (h'=h+1-min(1,n4)) & (adv'=0) & (honest'=0) +
			n4*x/total : (n5'=min(w,n5+1)) & (h'=h+1-min(1,n5)) & (adv'=0) & (honest'=0) +
			n5*x/total : (n6'=min(w,n6+1)) & (h'=h+1-min(1,n6)) & (adv'=0) & (honest'=0) +
			n6*x/total : (n0'=n1) & (n1'=n2) & (n2'=n3) & (n3'=n4) & (n4'=n5) & (n5'=n6) & (n6'=1) & (adv'=1) & (honest'=0); //TODO


	[] h>2 & c=0 -> (1-x)/total : (h'=h-1) & (adv'=1) & (honest'=0) +
			x/total : (n0'=min(w,n0+1)) & (adv'=0) & (honest'=0) +
			n0*x/total : (n1'=min(w,n1+1)) & (adv'=0) & (honest'=0) +
			n1*x/total : (n2'=min(w,n2+1)) & (adv'=0) & (honest'=0) +
			n2*x/total : (n3'=min(w,n3+1)) & (h'=h+1-min(1,n3)) & (adv'=0) & (honest'=0) +
			n3*x/total : (n4'=min(w,n4+1)) & (h'=h+1-min(1,n4)) & (adv'=0) & (honest'=0) +
			n4*x/total : (n5'=min(w,n5+1)) & (h'=h+1-min(1,n5)) & (adv'=0) & (honest'=0) +
			n5*x/total : (n6'=min(w,n6+1)) & (h'=h+1-min(1,n6)) & (adv'=0) & (honest'=0) +
			n6*x/total : (n0'=n1) & (n1'=n2) & (n2'=n3) & (n3'=n4) & (n4'=n5) & (n5'=n6) & (n6'=1) & (adv'=1) & (honest'=0); //TODO

endmodule

//rewards
  //  	[] true : adv;
    	//[] true : honest + adv;
//endrewards


rewards
	[] true : adv * (1-cq);
	[] true : honest * (-cq);
endrewards
