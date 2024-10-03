
module ID_EX ( clk, rst, en_reg, WB_out, MEM_out, EX_out, shamt_out, funct_out, RD1_out, RD2_out, immed_out, rt_out, rd_out,
							mul, WB_in,  MEM_in,  EX_in,  shamt_in,  funct_in,  RD1_in,  RD2_in,  immed_in,  rt_in,  rd_in );
    input clk, rst, en_reg;
	input [1:0]  WB_in;
	input [1:0]  MEM_in;
	input [3:0]  EX_in;
	input [4:0]	 rt_in, rd_in, shamt_in;
	input [5:0]  funct_in;
    input [31:0] RD1_in, RD2_in, immed_in;
	
	output reg[1:0]  WB_out;
	output reg[1:0]  MEM_out;
	output reg[3:0]  EX_out;
	output reg[4:0]  rt_out, rd_out, shamt_out;
	output reg[5:0]  funct_out;
    output reg[31:0] RD1_out, RD2_out, immed_out;
   
   	reg [7:0] counter;
	input [1:0] mul;
	
    always @(mul)  begin
	  counter = 0;
	end
	
	
    always @( posedge clk ) begin
    if ( rst ) begin
		WB_out    <= 2'b0;
		MEM_out   <= 2'b0;
		EX_out	  <= 4'b0;
		shamt_out <= 5'b0;
		funct_out <= 6'b0;
		RD1_out   <= 32'b0;
		RD2_out   <= 32'b0; 
		immed_out <= 32'b0; 
		rt_out    <= 5'b0; 
		rd_out    <= 5'b0;
	end
	else if ( mul > 0 && counter < 32 )
	  counter = counter + 1;
    else if ( en_reg ) begin
		WB_out    <=  WB_in;
		MEM_out   <=  MEM_in;
		EX_out	  <=  EX_in;
		shamt_out <=  shamt_in;
		funct_out <=  funct_in;
		RD1_out   <=  RD1_in;
		RD2_out   <=  RD2_in; 
		immed_out <=  immed_in; 
		rt_out    <=  rt_in; 
		rd_out    <=  rd_in;
	end
    end
endmodule
	

