module key_scheduler
	(
		input wire [3:0]	round,		// maximum 10 rounds
		input wire [63:0] prev_key,	// key_i = { key_i,1 | key_i,2 | ... | key_i,15 }
		output wire [63:0] next_key
		
	);
	wire [15:0] temp;	

	// ========================= //
	// = Multiply over GF(2^4) = //
	// ========================= //
	function [3:0] Mul;
		input [3:0] _word;
		input [1:0] _coe;   // 1, 2 or 3
		reg [3:0] _mul_temp;
		begin
			// multiply by x in GF(2^4) with poly x^4 + x + 1 (0b0011)
			_mul_temp = (_word[3] == 1'b1) ? ((_word << 1) ^ 4'b0011) : (_word << 1);

			case (_coe)
				2'b01: Mul = _word;        		// *1
				2'b10: Mul = _mul_temp;           // *2
				2'b11: Mul = _mul_temp ^ _word;   // *3
				default: Mul = 4'b0000;
			endcase
		end
	endfunction

	// ========================= //
	//  Last 16bits of prev key  //
	// ========================= //	
		sub_bytes_64bits u_temp 
			( 
				.msg({prev_key[3:0], prev_key[7:4], prev_key[11:8], prev_key[15:12]}), 
				.y(temp) 
			);
	
	// ========================= //
	// =    Round Constant     = //
	// ========================= //
	function [15:0] Rcon_col;
		input [3:0] _round;   		// round = 1..10
		reg [3:0] _rcon_temp;
		integer i;
		
		begin
			_rcon_temp = 4'b0001;	// rcon(1) = 1    
			// compute rcon(round) = x^(round-1)
			for (i = 1; i < _round; i = i + 1)
				_rcon_temp = Mul(_rcon_temp, 2'b10);   // multiply by x (2) in GF(2^4)
				
			Rcon_col = {_rcon_temp, 12'b0}; 
		end
	endfunction
	
	// ========================= //
	// = Next-key calculation  = //
	// ========================= //
	function [63:0] Key_calc;
		input [63:0]	_prev_key;
		input [15:0] 	_temp;
		input [3:0] 	_round;
		
		reg [15:0] _col0, _col1, _col2, _col3;
		
		begin
			_col0 = _prev_key[63:48] ^ _temp ^ Rcon_col(_round);
			_col1 = _col0 ^ _prev_key[47:32];
			_col2 = _col1 ^ _prev_key[31:16];
			_col3 = _col2 ^ _prev_key[15:0];

			// pack into 64-bit output
			Key_calc = {_col0, _col1, _col2, _col3};																
		end
	endfunction
	
	assign next_key = Key_calc(prev_key, temp, round);
		
endmodule