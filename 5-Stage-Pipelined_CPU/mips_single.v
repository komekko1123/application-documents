//	Title: MIPS Single-Cycle Processor
//	Editor: Selene (Computer System and Architecture Lab, ICE, CYCU)
module mips_single( clk, rst );
	input clk, rst;
	
	// instruction bus
	wire[31:0] instr;
	
	// break out important fields from instruction
	wire [5:0] opcode, funct;
    wire [4:0] rs, rt, rd, shamt;
    wire [15:0] immed;
    wire [31:0] extend_immed, b_offset;
    wire [25:0] jumpoffset;
	
	// datapath signals
    wire [4:0] rfile_wn; // rfile_wn就是wn_4的意思
    wire [31:0] rfile_rd1, rfile_rd2, rfile_wd, alu_b, alu_ans, b_tgt, pc_next,
                pc, pc_incr, dmem_rdata, jump_addr, branch_addr,HiOut,LoOut;

	// control signals

    wire RegWrite, Branch, PCSrc, RegDst, MemtoReg, MemRead, MemWrite, ALUSrc, Zero, Jump, open;
    wire [1:0] ALUOp, ALU_Out_Sel,mul;
    wire [2:0] Operation;
	
	wire [63:0] mul_ans;

	// pipeline擴充
	wire [1:0] WB_reg_1, WB_reg_2, WB_reg_3, WB_reg_4;
	wire [1:0] MEM_reg_1, MEM_reg_2, MEM_reg_3;
	wire [3:0] EX_reg_1, EX_reg_2;
	wire [4:0] wn_2, wn_3, rt_out, rd_out, shamt_out;
	wire [5:0] funct_out;
	wire [31:0] rfile_rd1_out, rfile_rd2_out, rd2ToWD, aluToADDR, alu_out, ADDR_out, b_tgt_out, pc_incr_out, dmem_rdata_out,
				result_immd_out, instr_out;


	
	
    assign opcode = instr_out[31:26];
    assign rs = instr_out[25:21];
    assign rt = instr_out[20:16];
    assign rd = instr_out[15:11];
    assign shamt = instr_out[10:6];
    assign funct = instr_out[5:0];
    assign immed = instr_out[15:0];
    assign jumpoffset = instr_out[25:0];
	
	// branch offset shifter
    assign b_offset = extend_immed << 2;
	
	// jump offset shifter & concatenation
	assign jump_addr = { pc_incr[31:28], jumpoffset << 2 };
	
	// Control for pipeline datapath
	assign WB_reg_1 = { RegWrite, MemtoReg };   
	assign MEM_reg_1 = { MemRead, MemWrite };  
	assign EX_reg_1 = { RegDst, ALUOp, ALUSrc };   
	// module instantiations
	
	reg32 PC( .clk(clk), .rst(rst), .en_reg(1'b1), .d_in(pc_next), .d_out(pc),.mul(mul) );
	// sign-extender
	sign_extend SignExt( .immed_in(immed), .ext_immed_out(extend_immed) );
	
	add32 PCADD( .a(pc), .b(32'd4), .result(pc_incr) );

    add32 BRADD( .a(pc_incr_out), .b(b_offset), .result(b_tgt) );

    ALU AlU( .a(rfile_rd1_out), .b(alu_b), .ctl(Operation), .out(alu_ans), .shamt(shamt_out) );

	Multiplier  multiplier( .clk(clk), .in0(rfile_rd1_out), .in1(rfile_rd2_out), .out(mul_ans), .mul(mul), .reset(reset), .open(open) );
	
	HiLo Hilo( .clk(clk), .MulAns(mul_ans), .HiOut(HiOut), .LoOut(LoOut), .reset(reset), .mul(mul), .open(open) );
	
	branch_equ equ( .opcode(opcode), .zero(Zero), .a(rfile_rd1), .b(rfile_rd2) );
	
    and BR_AND(PCSrc, Branch, Zero);

    mux2 #(5) RFMUX( .sel(EX_reg_2[3]), .a(rt_out), .b(rd_out), .y(wn_2) ); // RegDst_MUX

    mux2 #(32) PCMUX( .sel(PCSrc), .a(pc_incr), .b(b_tgt), .y(branch_addr) ); // PcSrc_MUX
	
	mux2 #(32) JMUX( .sel(Jump), .a(branch_addr), .b(jump_addr), .y(pc_next) ); // Jump_MUX
	
    mux2 #(32) ALUMUX( .sel(EX_reg_2[0]), .a(rfile_rd2_out), .b(result_immd_out), .y(alu_b) ); // ALUSrc_MUX

    mux2 #(32) WRMUX( .sel(WB_reg_4[0]), .a(ADDR_out), .b(dmem_rdata_out), .y(rfile_wd) ); //  MemtoReg_MUX

	mux4 #(32) OUTMUX( .sel(ALU_Out_Sel), .a(alu_ans), .b(HiOut), .c(LoOut), .y(alu_out) ); // 選ALU還是HILO輸出

    control_single CTL(.opcode(opcode), .RegDst(RegDst), .ALUSrc(ALUSrc), .MemtoReg(MemtoReg), 
                       .RegWrite(RegWrite), .MemRead(MemRead), .MemWrite(MemWrite), .Branch(Branch), 
                       .Jump(Jump), .ALUOp(ALUOp) );

    alu_ctl ALUCTL( .ALUOp(EX_reg_2[2:1]), .Funct(funct_out), .ALUOperation(Operation), .mul(mul), .sel(ALU_Out_Sel) );
	

	reg_file RegFile( .clk(clk), .RegWrite(WB_reg_4[1]), .RN1(rs), .RN2(rt), .WN(rfile_wn), .WD(rfile_wd), .RD1(rfile_rd1), .RD2(rfile_rd2), .mul(mul) );

	memory InstrMem( .clk(clk), .MemRead(1'b1), .MemWrite(1'b0), .wd(32'd0), .addr(pc), .rd(instr), .mul(mul) );
	
	memory DatMem( .clk(clk), .MemRead(MEM_reg_3[1]), .MemWrite(MEM_reg_3[0]), .wd(rd2ToWD), .addr(aluToADDR), .rd(dmem_rdata), .mul(mul) );	   
	
	IF_ID IF_ID_Reg( .clk(clk), .rst(rst), .en_reg(1'b1), .pc_out(pc_incr_out), .ins_out(instr_out), .pc_in(pc_incr), .ins_in(instr), .mul(mul) );
	
	ID_EX ID_EX_Reg( .clk(clk), .rst(rst), .en_reg(1'b1), .WB_out(WB_reg_2), .MEM_out(MEM_reg_2), .EX_out(EX_reg_2), .shamt_out(shamt_out), .funct_out(funct_out),
					 .RD1_out(rfile_rd1_out), .RD2_out(rfile_rd2_out), .immed_out(result_immd_out), .rt_out(rt_out), .rd_out(rd_out),
					 .WB_in(WB_reg_1), .MEM_in(MEM_reg_1), .EX_in(EX_reg_1), .shamt_in(shamt), .funct_in(funct), .RD1_in(rfile_rd1), .RD2_in(rfile_rd2), 
					 .immed_in(extend_immed), .rt_in(rt), .rd_in(rd), .mul(mul) );
					 
	EX_MEM EX_MEM_Reg( .clk(clk), .rst(rst), .en_reg(1'b1), .WB_out(WB_reg_3), .MEM_out(MEM_reg_3), .alu_out(aluToADDR), .RD2_out(rd2ToWD), .WN_out(wn_3)
											, .mul(mul) , .WB_in(WB_reg_2), .MEM_in(MEM_reg_2), .alu_in(alu_out), .RD2_in(rfile_rd2_out), .WN_in(wn_2) );
	
	MEM_WB MEM_WB_Reg( .clk(clk), .rst(rst), .en_reg(1'b1), .WB_out(WB_reg_4), .RD_out(dmem_rdata_out), .ADDR_out(ADDR_out), .WN_out(rfile_wn)
														  ,	.WB_in(WB_reg_3), .RD_in(dmem_rdata), .ADDR_in(aluToADDR), .WN_in(wn_3), .mul(mul) );				 
					 
					 
					 
endmodule
