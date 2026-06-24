`timescale 1ns/1ps
/*
module tb_top_aes_mini;

    reg  [63:0] plaintext;
    reg  [63:0] master_key;
    wire [63:0] ciphertext;

    // Expected output
    localparam [0:63] EXPECTED_CT = 64'h609B_6227_BA39_3803;

    // DUT
    top_aes_mini dut (
        .plaintext(plaintext),
        .master_key(master_key),
        .ciphertext(ciphertext)
    );

    initial begin
        $display("===== AES-MINI TOP MODULE TEST =====");

        // Apply test vector
        plaintext  = 64'h0000_0000_0000_0000;
        master_key = 64'hFEDC_BA98_7654_3210;

        #20;  // allow combinational logic to settle

        $display("\n--- Test Case ---");
        $display("Plaintext   = %h", plaintext);
        $display("Master Key  = %h", master_key);
        $display("Ciphertext  = %h", ciphertext);
        $display("Expected    = %h", EXPECTED_CT);

        if (ciphertext === EXPECTED_CT)
            $display("\n*** PASS: Ciphertext matches expected value ***");
        else
            $display("\n*** FAIL: Ciphertext does NOT match expected value ***");

        $display("\n===== TEST FINISHED =====");
        $stop;
    end

endmodule
*/

module tb_top_aes_mini;

    // ==================================================
    // DUT Inputs
    // ==================================================

    reg         clk;
    reg         rst;
    reg         start;

    reg [63:0]  plaintext;
    reg [63:0]  master_key;

    // ==================================================
    // DUT Outputs
    // ==================================================

    wire [63:0] ciphertext;
    wire        done;

    // ==================================================
    // Instantiate DUT
    // ==================================================

    top_aes_mini dut (
        .clk(clk),
        .rst(rst),
        .start(start),

        .plaintext(plaintext),
        .master_key(master_key),

        .ciphertext(ciphertext),
        .done(done)
    );

    // ==================================================
    // Clock generation
    // ==================================================

    initial begin
        clk = 0;
        forever #5 clk = ~clk;     // 100 MHz
    end

    // ==================================================
    // Stimulus
    // ==================================================

    initial begin

        // ----------------------------------------------
        // Initialize
        // ----------------------------------------------

        rst        = 1;
        start      = 0;

        plaintext  = 64'h0123456789ABCDEF;
        master_key = 64'h0F1E2D3C4B5A6978;

        // ----------------------------------------------
        // Reset
        // ----------------------------------------------

        #20;
        rst = 0;

        // ----------------------------------------------
        // Start encryption
        // ----------------------------------------------

        @(posedge clk);
        start = 1;

        @(posedge clk);
        start = 0;

        // ----------------------------------------------
        // Wait for completion
        // ----------------------------------------------

        wait(done == 1);

        $display("====================================");
        $display("Encryption Finished");
        $display("Plaintext  = %h", plaintext);
        $display("Key        = %h", master_key);
        $display("Ciphertext = %h", ciphertext);
        $display("Time       = %0t ns", $time);
        $display("====================================");

        #20;

        $stop;
    end
endmodule
