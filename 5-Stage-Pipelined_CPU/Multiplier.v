module Multiplier( in0, in1, out, reset, clk, mul, open ) ;

    input       [31:0] in0, in1 ;
	input       reset, clk ;
	input       [1:0] mul;
	output reg  [63:0] out ;
	output reg 	open;
	reg         [6:0] count ;
	reg         [63:0] MCND, PROD ;
	reg         [31:0] MPY ;
    initial
	begin
	    MCND = 0 ;
		MPY = 0 ;
		PROD = 0 ;
	    count = 1 ;
		out = 0 ;
		open = 0 ;
	end

	always @( mul ) begin 
	  if ( mul > 0 ) begin
		count = 1 ;
		MCND = { 32'b0, in0 } ;
		MPY  = in1 ;
		PROD = 0;
		open = 1;
		out = 0 ;
	  end
	end
	
	always @ ( posedge reset or clk )
	begin
	    if( reset )
		begin
		    MCND = 0 ;
		    MPY = 0 ;
		    PROD = 0 ;
	        count = 1 ;
		    out = 0 ;
			open = 0 ;
	    end
		
		else if( clk )
		begin
		    if( count < 32 && open == 1 )
		    begin	
		        if( MPY[0] == 1'b1 )
				begin
			        PROD = PROD + MCND ;
				end
				count <= count + 1 ;
				if( count > 0 ) begin
			      MCND <= MCND << 1 ;
			      MPY  <= MPY  >> 1 ;
				end
			end
			
			if( count == 32 )
			begin
			  if( MPY[0] == 1'b1 )
			    PROD = PROD + MCND ;
			  MPY  = MPY  >> 1 ;
			  open = 0;
			  count = 0 ;
			  out = PROD ;
			end
			
		end
		
	end

endmodule