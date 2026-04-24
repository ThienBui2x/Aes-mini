module top_aes_mini 
	(
		input  wire [63:0] plaintext,
		input  wire [63:0] master_key,
		output wire [63:0] ciphertext
	);

	// ============================
	// 0. Initial AddRoundKey
	// ============================
	wire [63:0] round0;
	assign round0 = plaintext ^ master_key;

	// ============================
	// 1. Generate all round keys
	// ============================
	wire [63:0] key0 = master_key;
	wire [63:0] key1, key2, key3, key4, key5, key6, key7, key8, key9, key10;

	key_scheduler ks1  (.round(4'd1),  .prev_key(key0),  .next_key(key1));
	key_scheduler ks2  (.round(4'd2),  .prev_key(key1),  .next_key(key2));
	key_scheduler ks3  (.round(4'd3),  .prev_key(key2),  .next_key(key3));
	key_scheduler ks4  (.round(4'd4),  .prev_key(key3),  .next_key(key4));
	key_scheduler ks5  (.round(4'd5),  .prev_key(key4),  .next_key(key5));
	key_scheduler ks6  (.round(4'd6),  .prev_key(key5),  .next_key(key6));
	key_scheduler ks7  (.round(4'd7),  .prev_key(key6),  .next_key(key7));
	key_scheduler ks8  (.round(4'd8),  .prev_key(key7),  .next_key(key8));
	key_scheduler ks9  (.round(4'd9),  .prev_key(key8),  .next_key(key9));
	key_scheduler ks10 (.round(4'd10), .prev_key(key9),  .next_key(key10));

	// ============================
	// 2. Instantiate all 10 rounds
	// ============================
	wire [63:0] round1, round2, round3, round4, round5;
	wire [63:0] round6, round7, round8, round9, round10;

	rouding r1  (.round(4'd1),  .prev_round(round0), .prev_key(key1),  .next_round(round1));
	rouding r2  (.round(4'd2),  .prev_round(round1), .prev_key(key2),  .next_round(round2));
	rouding r3  (.round(4'd3),  .prev_round(round2), .prev_key(key3),  .next_round(round3));
	rouding r4  (.round(4'd4),  .prev_round(round3), .prev_key(key4),  .next_round(round4));
	rouding r5  (.round(4'd5),  .prev_round(round4), .prev_key(key5),  .next_round(round5));
	rouding r6  (.round(4'd6),  .prev_round(round5), .prev_key(key6),  .next_round(round6));
	rouding r7  (.round(4'd7),  .prev_round(round6), .prev_key(key7),  .next_round(round7));
	rouding r8  (.round(4'd8),  .prev_round(round7), .prev_key(key8),  .next_round(round8));
	rouding r9  (.round(4'd9),  .prev_round(round8), .prev_key(key9),  .next_round(round9));
	rouding r10 (.round(4'd10), .prev_round(round9), .prev_key(key10),  .next_round(round10));

	// ============================
	// 3. Final output
	// ============================
	assign ciphertext = round10;

endmodule
