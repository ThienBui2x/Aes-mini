module shift_rows
	(
		input wire [63:0] before,
		output wire [63:0] after
	);	
	// 1st Row
	assign after[63:60] = before[63:60];
	assign after[47:44] = before[47:44];
	assign after[31:28] = before[31:28];
	assign after[15:12] = before[15:12];
	// 2nd Row
	assign after[59:56] = before[43:40];
	assign after[43:40] = before[27:24];
	assign after[27:24] = before[11:8];
	assign after[11:8]  = before[59:56];
	// 3rd Row
	assign after[55:52] = before[23:20];
	assign after[39:36] = before[7:4];
	assign after[23:20] = before[55:52];
	assign after[7:4]   = before[39:36];
	// 4th Row
	assign after[51:48]  = before[3:0];
	assign after[35:32]  = before[51:48];
	assign after[19:16]  = before[35:32];
	assign after[3:0]    = before[19:16];
	
endmodule