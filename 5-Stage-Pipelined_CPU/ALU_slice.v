module ALU_slice( a, b, cin, inv, less, op, cout, out, sum );
	input a,b,cin,inv,less; 
	input [1:0] op;
	output cout, out,sum;
	wire bi,and1,or1,temp,sum;	


	xor(bi,inv,b);
	and(and1,a,b);
	or(or1,a,b);
	
	FA FA( .a(a), .b(bi), .c(cin), .cout(cout), .sum(sum) ); // sum = add和sum 
	assign out = ( op[1] ) ? ( op[0] ? less : sum ) : ( op[0] ? or1 : and1 ); // 11 less -- 10 add,sum -- 01 or -- 00 and 
	
endmodule