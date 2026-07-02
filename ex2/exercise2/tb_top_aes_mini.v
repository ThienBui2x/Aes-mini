`timescale 1ns/1ps

module tb_top_aes_mini;

    reg  [63:0] plaintext;
    reg  [63:0] master_key;

    reg         fault_en;
    reg  [63:0] fault_inj;

    wire [63:0] ciphertext;

    reg [63:0] ct_correct;
    reg [63:0] ct_faulty;

    // DUT
    top_aes_mini dut (
        .plaintext(plaintext),
        .master_key(master_key),
        .fault_en(fault_en),
        .fault_inj(fault_inj),
        .ciphertext(ciphertext)
    );

    initial begin
        $display("===== AES-MINI FAULT ATTACK TEST =====");

        // =========================
        // Input vector
        // =========================
        plaintext  = 64'h0000_0000_0000_0000;
        master_key = 64'hFEDC_BA98_7654_3210;

        fault_inj  = 64'h0000_0000_0000_0001;

        // =========================
        // 1. Correct encryption
        // =========================
        fault_en = 0;
        #20;
        ct_correct = ciphertext;

        $display("\n--- CORRECT RUN ---");
        $display("Ciphertext = %X", ct_correct);

        // =========================
        // 2. Faulty encryption
        // =========================
        fault_en = 1;
        #20;
        ct_faulty = ciphertext;

        $display("\n--- FAULTY RUN ---");
        $display("Ciphertext = %X", ct_faulty);

        // =========================
        // 3. Difference (DFA observable)
        // =========================
        $display("\n--- DIFFERENCE ---");
        $display("CT XOR     = %X", ct_correct ^ ct_faulty);
        $stop;
    end

endmodule
