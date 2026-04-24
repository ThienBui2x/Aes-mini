`timescale 1ns/1ps

module tb_shift_rows;

    reg  [63:0] before;
    wire [63:0] after;

    shift_rows dut (
        .before(before),
        .after(after)
    );

    initial begin
        $display("=== ShiftRows TB ===");

        before = 64'hB542_E7A9_DFC3_1086; 
        #1 $display("before = %h  ->  after = %h", before, after);

        before = 64'h6801_3CFD_9A7E_245B;
        #1 $display("before = %h  ->  after = %h", before, after);

        $display("=== Done ===");
        $stop;
    end

endmodule
