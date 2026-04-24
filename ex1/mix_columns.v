module mix_columns
	(
		input wire [15:0] msg,
		output wire [15:0] y
	);
	
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
	

	assign y[15:12]   = Mul(msg[15:12], 2) ^ Mul(msg[11:8], 3) ^ Mul(msg[7:4], 1) ^ Mul(msg[3:0], 1);	
	assign y[11:8]   = Mul(msg[15:12], 1) ^ Mul(msg[11:8], 2) ^ Mul(msg[7:4], 3) ^ Mul(msg[3:0], 1);	
	assign y[7:4]   = Mul(msg[15:12], 1) ^ Mul(msg[11:8], 1) ^ Mul(msg[7:4], 2) ^ Mul(msg[3:0], 3);	
	assign y[3:0]   = Mul(msg[15:12], 3) ^ Mul(msg[11:8], 1) ^ Mul(msg[7:4], 1) ^ Mul(msg[3:0], 2);	

endmodule