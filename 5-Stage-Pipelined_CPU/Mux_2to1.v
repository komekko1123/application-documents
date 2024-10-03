`timescale 1ns / 1ns

module Mux_2to1(in0, in1, sel, out);

    input  in0, in1,sel; 
    output out;
	assign out = (sel) ? in1 : in0;
endmodule
