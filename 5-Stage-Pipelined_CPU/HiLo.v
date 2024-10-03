module HiLo( clk, MulAns, HiOut, LoOut, reset, mul, open );
	input clk ;
	input reset,open ;
	input [63:0]  MulAns ;
	input [1:0]	  mul;
	output [31:0] HiOut ;
	output [31:0] LoOut ;
	reg [63:0] HiLo ;
	reg counter;
	always@( posedge clk or reset )  begin
	  if ( reset == 1'b1 )
		HiLo = 64'b0 ;
	  else if( open == 0 && mul > 0 && counter == 0 ) begin
	    if( mul == 2'b01 )
		  HiLo = MulAns ;
	    else if( mul == 2'b10 ) 
	      HiLo = HiLo + MulAns;
		counter = counter + 1;
	  end	
	end

	always@( open )  begin
	  counter = 0;
	end

	assign HiOut = HiLo[63:32] ;
	assign LoOut = HiLo[31:0] ;

endmodule