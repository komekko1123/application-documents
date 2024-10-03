
module IF_ID ( clk, rst, en_reg, pc_out, ins_out, pc_in, ins_in, mul  );
    input clk, rst, en_reg;
    input[31:0]	pc_in, ins_in;
    output[31:0] pc_out, ins_out;
    reg [31:0] pc_out, ins_out;
   
   	reg [7:0] counter;
	input [1:0] mul;
	
	
    always @(mul)  begin
	  counter = 0;
	end
	
    always @( posedge clk ) begin
      if ( rst ) begin
		pc_out  <= 32'b0;
		ins_out <= 32'b0;
	  end
	  else if ( mul > 0 && counter < 32 )
	    counter = counter + 1;
      else if ( en_reg ) begin
		pc_out  <= pc_in;
		ins_out <= ins_in;
	  end
    end
endmodule
	

