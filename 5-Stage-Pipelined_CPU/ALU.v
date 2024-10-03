module ALU( ctl, a, b, out, shamt );

  input [31:0] a,b;
  input [2:0] ctl;
  input [4:0] shamt;
  output [31:0] out;
  wire cout,inv;
  wire [1:0] op;
  wire [31:0] c,sum,temp,srl_out; // 32接線
  assign op = ctl[1:0];
  assign inv = ctl[2];
  ALU_slice i0( .a(a[0]), .b(b[0]), .cin(inv), .inv(inv), .op(op), .less(sum[31]),  .cout(c[0]), .out(temp[0]), .sum(sum[0]) );
  ALU_slice i1( .a(a[1]), .b(b[1]), .cin(c[0]), .inv(inv), .op(op), .less(1'b0), .cout(c[1]), .out(temp[1]), .sum(sum[1]));
  ALU_slice i2( .a(a[2]), .b(b[2]), .cin(c[1]), .inv(inv), .op(op), .less(1'b0), .cout(c[2]), .out(temp[2]), .sum(sum[2]));
  ALU_slice i3( .a(a[3]), .b(b[3]), .cin(c[2]), .inv(inv), .op(op), .less(1'b0), .cout(c[3]), .out(temp[3]), .sum(sum[3]));	
  ALU_slice i4( .a(a[4]), .b(b[4]), .cin(c[3]), .inv(inv), .op(op), .less(1'b0), .cout(c[4]), .out(temp[4]), .sum(sum[4]));
  ALU_slice i5( .a(a[5]), .b(b[5]), .cin(c[4]), .inv(inv), .op(op), .less(1'b0), .cout(c[5]), .out(temp[5]), .sum(sum[5]));
  ALU_slice i6( .a(a[6]), .b(b[6]), .cin(c[5]), .inv(inv), .op(op), .less(1'b0), .cout(c[6]), .out(temp[6]), .sum(sum[6]));
  ALU_slice i7( .a(a[7]), .b(b[7]), .cin(c[6]), .inv(inv), .op(op), .less(1'b0), .cout(c[7]), .out(temp[7]), .sum(sum[7]));	
  ALU_slice i8( .a(a[8]), .b(b[8]), .cin(c[7]), .inv(inv), .op(op), .less(1'b0), .cout(c[8]), .out(temp[8]), .sum(sum[8]));
  ALU_slice i9( .a(a[9]), .b(b[9]), .cin(c[8]), .inv(inv), .op(op), .less(1'b0), .cout(c[9]), .out(temp[9]), .sum(sum[9]));
  ALU_slice i10( .a(a[10]), .b(b[10]), .cin(c[9]), .inv(inv), .op(op), .less(1'b0), .cout(c[10]), .out(temp[10]), .sum(sum[10]));
  ALU_slice i11( .a(a[11]), .b(b[11]), .cin(c[10]), .inv(inv), .op(op), .less(1'b0), .cout(c[11]), .out(temp[11]), .sum(sum[11]));
  ALU_slice i12( .a(a[12]), .b(b[12]), .cin(c[11]), .inv(inv), .op(op), .less(1'b0), .cout(c[12]), .out(temp[12]), .sum(sum[12]));
  ALU_slice i13( .a(a[13]), .b(b[13]), .cin(c[12]), .inv(inv), .op(op), .less(1'b0), .cout(c[13]), .out(temp[13]), .sum(sum[13]));	
  ALU_slice i14( .a(a[14]), .b(b[14]), .cin(c[13]), .inv(inv), .op(op), .less(1'b0), .cout(c[14]), .out(temp[14]), .sum(sum[14]));
  ALU_slice i15( .a(a[15]), .b(b[15]), .cin(c[14]), .inv(inv), .op(op), .less(1'b0), .cout(c[15]), .out(temp[15]), .sum(sum[15]));
  ALU_slice i16( .a(a[16]), .b(b[16]), .cin(c[15]), .inv(inv), .op(op), .less(1'b0), .cout(c[16]), .out(temp[16]), .sum(sum[16]));
  ALU_slice i17( .a(a[17]), .b(b[17]), .cin(c[16]), .inv(inv), .op(op), .less(1'b0), .cout(c[17]), .out(temp[17]), .sum(sum[17]));	
  ALU_slice i18( .a(a[18]), .b(b[18]), .cin(c[17]), .inv(inv), .op(op), .less(1'b0), .cout(c[18]), .out(temp[18]), .sum(sum[18]));
  ALU_slice i19( .a(a[19]), .b(b[19]), .cin(c[18]), .inv(inv), .op(op), .less(1'b0), .cout(c[19]), .out(temp[19]), .sum(sum[19]));
  ALU_slice i20( .a(a[20]), .b(b[20]), .cin(c[19]), .inv(inv), .op(op), .less(1'b0), .cout(c[20]), .out(temp[20]), .sum(sum[20]));
  ALU_slice i21( .a(a[21]), .b(b[21]), .cin(c[20]), .inv(inv), .op(op), .less(1'b0), .cout(c[21]), .out(temp[21]), .sum(sum[21]));
  ALU_slice i22( .a(a[22]), .b(b[22]), .cin(c[21]), .inv(inv), .op(op), .less(1'b0), .cout(c[22]), .out(temp[22]), .sum(sum[22]));
  ALU_slice i23( .a(a[23]), .b(b[23]), .cin(c[22]), .inv(inv), .op(op), .less(1'b0), .cout(c[23]), .out(temp[23]), .sum(sum[23]));	
  ALU_slice i24( .a(a[24]), .b(b[24]), .cin(c[23]), .inv(inv), .op(op), .less(1'b0), .cout(c[24]), .out(temp[24]), .sum(sum[24]));
  ALU_slice i25( .a(a[25]), .b(b[25]), .cin(c[24]), .inv(inv), .op(op), .less(1'b0), .cout(c[25]), .out(temp[25]), .sum(sum[25]));
  ALU_slice i26( .a(a[26]), .b(b[26]), .cin(c[25]), .inv(inv), .op(op), .less(1'b0), .cout(c[26]), .out(temp[26]), .sum(sum[26]));
  ALU_slice i27( .a(a[27]), .b(b[27]), .cin(c[26]), .inv(inv), .op(op), .less(1'b0), .cout(c[27]), .out(temp[27]), .sum(sum[27]));	
  ALU_slice i28( .a(a[28]), .b(b[28]), .cin(c[27]), .inv(inv), .op(op), .less(1'b0), .cout(c[28]), .out(temp[28]), .sum(sum[28]));
  ALU_slice i29( .a(a[29]), .b(b[29]), .cin(c[28]), .inv(inv), .op(op), .less(1'b0), .cout(c[29]), .out(temp[29]), .sum(sum[29]));
  ALU_slice i30( .a(a[30]), .b(b[30]), .cin(c[29]), .inv(inv), .op(op), .less(1'b0), .cout(c[30]), .out(temp[30]), .sum(sum[30]));
  ALU_slice i31( .a(a[31]), .b(b[31]), .cin(c[30]), .inv(inv), .op(op), .less(1'b0), .cout(c[31]), .out(temp[31]), .sum(sum[31]));
  
   
  Shifter shifter( .in(b), .shamt(shamt), .out(srl_out) );
  
  assign out = (ctl == 3'b011) ? srl_out : temp ;  // shifter的狀況
  
endmodule