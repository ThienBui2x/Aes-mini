module rouding
	(
		input wire [3:0] round,
		input wire [63:0] prev_round,
		input wire [63:0] prev_key,
		input wire [63:0] fault_inj,
		input wire 		  fault_en,
		output wire [63:0] next_round
	);
	
	wire [63:0] s_bytes_res;
	wire [63:0] s_bytes_fault_res;
	wire [63:0] s_rows_res;
	wire [63:0] m_cols_res;
	wire [63:0] m_cols_fault_res;
	
	// ========================= //
	// =    Calc Sub Bytes     = //
	// ========================= //	
	sub_bytes_64bits sb_u1 ( .msg(prev_round[63:48]) , .y(s_bytes_res[63:48]) );
	sub_bytes_64bits sb_u2 ( .msg(prev_round[47:32]) , .y(s_bytes_res[47:32]) );
	sub_bytes_64bits sb_u3 ( .msg(prev_round[31:16]) , .y(s_bytes_res[31:16]) );
	sub_bytes_64bits sb_u4 ( .msg(prev_round[15:0]) , .y(s_bytes_res[15:0]) );

	// ========================= //
	// = Add Fault at round 9  = //
	// ========================= //
	assign s_bytes_fault_res = (round == 4'd9 && fault_en) ? (s_bytes_res ^ fault_inj) : s_bytes_res;
	// assign s_bytes_fault_res = s_bytes_res;
	
	// ========================= //
	// =    Calc Shift Rows    = //
	// ========================= //
	shift_rows sr_u1 ( .before(s_bytes_fault_res), .after(s_rows_res) );
	
	// ========================= //
	// =   Calc Mix Columns    = //
	// ========================= //
	mix_columns mc_u1 (.msg(s_rows_res[63:48]) , .y(m_cols_res[63:48]) );
	mix_columns mc_u2 (.msg(s_rows_res[47:32]) , .y(m_cols_res[47:32]) );
	mix_columns mc_u3 (.msg(s_rows_res[31:16]) , .y(m_cols_res[31:16]) );
	mix_columns mc_u4 (.msg(s_rows_res[15:0]) , .y(m_cols_res[15:0]) );
	
	// ========================= //
	// = Add Fault at round 9  = //
	// ========================= //
	// assign m_cols_fault_res = (round == 4'd9 && fault_en) ? (m_cols_res ^ fault_inj) : m_cols_res;
	assign m_cols_fault_res = m_cols_res;
	
	// ========================= //
	// =    Add Round Key      = //
	// ========================= //
	assign next_round = ((round == 4'd10) ? s_rows_res : m_cols_fault_res) ^ prev_key;
	
endmodule
	