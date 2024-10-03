/*
	Title: 32-Bit Register with Synchronous Reset
	Editor: Selene (Computer System and Architecture Lab, ICE, CYCU)
	
	Input Port
		1. clk
		2. rst: 重置訊號
		3. en_reg: 控制暫存器是否可寫入
		4. d_in: 欲寫入的暫存器資料
	Output Port
		1. d_out: 所讀取的暫存器資料
*/
module reg32 ( clk, rst, en_reg, d_in, d_out, mul );
    input clk, rst, en_reg;
	input [1:0] mul;
    input[31:0]	d_in;
    output[31:0] d_out;
    reg [31:0] d_out;
	reg [7:0] counter;
	input [1:0] mul;
	initial begin
	  counter = 0;
	end
    always @(mul)  begin
	  counter = 0;
	end
    always @( posedge clk ) begin
        if ( rst )
			d_out <= 32'b0;
		else if ( mul > 0 && counter < 32 )
		  counter = counter + 1;
        else if ( en_reg )
			d_out <= d_in;
    end

endmodule
	
