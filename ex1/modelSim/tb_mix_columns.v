`timescale 1ns/1ps

module tb_mix_columns;

    reg  [63:0] msg;          // 64-bit input state
    wire [63:0] y;            // 64-bit output (4 columns)

    // Instantiate 4 MixColumns blocks (like in rounding)
    mix_columns mc0 (.msg(msg[63:48]),   .y(y[63:48]));
    mix_columns mc1 (.msg(msg[47:32]),  .y(y[47:32]));
    mix_columns mc2 (.msg(msg[31:16]),  .y(y[31:16]));
    mix_columns mc3 (.msg(msg[15:0]),  .y(y[15:0]));

    initial begin
        $display("=== MixColumns 64-bit Testbench ===");

        // -------------------------
        // Test Vector 1
        // -------------------------
        msg = 64'hB7C6_EF82_D049_15A3;
        #1;
        $display("\nInput  = %h", msg);
        $display("Col0   = %h", y[63:48]);
        $display("Col1   = %h", y[47:32]);
        $display("Col2   = %h", y[31:16]);
        $display("Col3   = %h", y[15:0]);
        $display("Output = %h", y);

        // -------------------------
        // Test Vector 2 (default)
        // -------------------------
        msg = 64'hA7E9_A7E9_A7E9_A7E9;   // same column repeated
        #1;
        $display("\nInput  = %h", msg);
        $display("Col0   = %h", y[63:48]);
        $display("Col1   = %h", y[47:32]);
        $display("Col2   = %h", y[31:16]);
        $display("Col3   = %h", y[15:0]);
        $display("Output = %h", y);

        $display("\n=== TEST FINISHED ===");
        $stop;
    end

endmodule

