`timescale 1ns/1ps

module tb_key_scheduler;

    reg  [3:0]  round;
    reg  [63:0] prev_key;
    wire [63:0] next_key;

    // Expected output for comparison
    localparam [63:0] EXPECTED_KEY5 = 64'h3A3A_1A16_EA45_4C2B;

    // DUT
    key_scheduler dut (
        .round(round),
        .prev_key(prev_key),
        .next_key(next_key)
    );

    initial begin
        $display("===== KEY SCHEDULER TEST: key_4 ? key_5 =====");

        // -----------------------------------------
        // Test Case 1 (official expected vector)
        // -----------------------------------------
        round    = 4'd5;
        prev_key = 64'h0D45_202C_F053_A66E;
        #10;

        $display("\n--- Test Case 1 ---");
        $display("Round     = %0d", round);
        $display("Prev Key  = %h", prev_key);
        $display("Next Key  = %h", next_key);
        $display("Expected  = %h", EXPECTED_KEY5);

        if (next_key === EXPECTED_KEY5)
            $display("*** PASS: next_key matches expected key_5 ***");
        else
            $display("*** FAIL: next_key does NOT match expected key_5 ***");

        // -----------------------------------------
        // Test Case 2 (custom)
        // -----------------------------------------
        round    = 4'd5;
        prev_key = 64'h1234_5678_9ABC_DEF0;
        #10;

        $display("\n--- Test Case 2 ---");
        $display("Round     = %0d", round);
        $display("Prev Key  = %h", prev_key);
        $display("Next Key  = %h", next_key);

        // -----------------------------------------
        // Test Case 3 (custom)
        // -----------------------------------------
        round    = 4'd5;
        prev_key = 64'h64D0_76F3_CA59_26E2;
        #10;

        $display("\n--- Test Case 3 ---");
        $display("Round     = %0d", round);
        $display("Prev Key  = %h", prev_key);
        $display("Next Key  = %h", next_key);

        $display("\n===== TEST FINISHED =====");
        $stop;
    end

endmodule

