`timescale 1ns/1ps

module tb_sub_bytes_64bits;

    reg  [15:0] msg;
    wire [15:0] y;

    sub_bytes_64bits dut (
        .msg(msg),
        .y(y)
    );

    initial begin
        $display("Starting SubBytes 16?bit test...");

        // Case 1
        msg = 16'h0000;
        #1 $display("msg = %h  ->  y = %h", msg, y);

        // Case 2
        msg = 16'h1234;
        #1 $display("msg = %h  ->  y = %h", msg, y);

        // Case 3
        msg = 16'hABCD;
        #1 $display("msg = %h  ->  y = %h", msg, y);

        // Case 4
        msg = 16'hF00F;
        #1 $display("msg = %h  ->  y = %h", msg, y);

        // Case 5
        msg = 16'hDEAD;
        #1 $display("msg = %h  ->  y = %h", msg, y);

        $display("Test finished.");
        $stop;
    end

endmodule

