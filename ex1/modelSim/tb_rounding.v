`timescale 1ns/1ps

module tb_rouding;

    reg  [3:0]  round;
    reg  [63:0] prev_round;
    reg  [63:0] prev_key;
    wire [63:0] next_round;

    // DUT
    rouding dut (
        .round(round),
        .prev_round(prev_round),
        .prev_key(prev_key),
        .next_round(next_round)
    );

    initial begin
        $display("===== ROUNDING MODULE TEST =====");

        // -----------------------------------------
        // Test Case 1
        // -----------------------------------------
        round      = 4'd1;
        prev_round = 64'h0000_0000_0000_0000;
        prev_key   = 64'h1111_2222_3333_4444;
        #5;

        $display("\n--- Test Case 1 ---");
        $display("Round       = %0d", round);
        $display("Prev State  = %h", prev_round);
        $display("Prev Key    = %h", prev_key);
        $display("Next State  = %h", next_round);

        // -----------------------------------------
        // Test Case 2
        // -----------------------------------------
        round      = 4'd5;
        prev_round = 64'h1234_5678_9ABC_DEF0;
        prev_key   = 64'hEDCC_1233_1233_7455;
        #5;

        $display("\n--- Test Case 2 ---");
        $display("Round       = %0d", round);
        $display("Prev State  = %h", prev_round);
        $display("Prev Key    = %h", prev_key);
        $display("Next State  = %h", next_round);

        // -----------------------------------------
        // Test Case 3
        // -----------------------------------------
        round      = 4'd3;
        prev_round = 64'hB542_E7A9_DFC3_1086;
        prev_key   = 64'h64D0_76F3_CA59_26E2;
        #5;

        $display("\n--- Test Case 3 ---");
        $display("Round       = %0d", round);
        $display("Prev State  = %h", prev_round);
        $display("Prev Key    = %h", prev_key);
        $display("Next State  = %h", next_round);

        // -----------------------------------------
        // Test Case 4 (Round 10: No MixColumns)
        // -----------------------------------------
        round      = 4'd10;
        prev_round = 64'hDEAD_BEEF_1234_5678;
        prev_key   = 64'hCAFEBABE_0000_1111;
        #5;

        $display("\n--- Test Case 4 (Round 10: No MixColumns) ---");
        $display("Round       = %0d", round);
        $display("Prev State  = %h", prev_round);
        $display("Prev Key    = %h", prev_key);
        $display("Next State  = %h", next_round);

        $display("\n===== TEST FINISHED =====");
        $stop;
    end

endmodule

