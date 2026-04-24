module s_box_4bit 
	(
		input wire [3:0] word,
		output wire [3:0] y
	);

	assign y = 	(word == 4'h0) ? 4'h6 :
					(word == 4'h1) ? 4'hB :
					(word == 4'h2) ? 4'h5 :
					(word == 4'h3) ? 4'h4 :
					(word == 4'h4) ? 4'h2 :
					(word == 4'h5) ? 4'hE :
					(word == 4'h6) ? 4'h7 :
					(word == 4'h7) ? 4'hA :
					(word == 4'h8) ? 4'h9 :
					(word == 4'h9) ? 4'hD :
					(word == 4'hA) ? 4'hF :
					(word == 4'hB) ? 4'hC :
					(word == 4'hC) ? 4'h3 :
					(word == 4'hD) ? 4'h1 :
					(word == 4'hE) ? 4'h0 :
										  4'h8;	
	
endmodule