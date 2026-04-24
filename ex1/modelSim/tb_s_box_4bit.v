`timescale 1ns/1ps

module tb_s_box_4bit;

    reg  [3:0] word;
    wire [3:0] y;

    // Instantiate the DUT (Device Under Test)
    s_box_4bit dut (
        .word(word),
        .y(y)
    );

    integer i;

    initial begin
        $display("Starting S-Box test...");

        // Loop through all 16 possible inputs
        for (i = 0; i < 16; i = i + 1) begin
            word = i[3:0];
            #1; // small delay to allow combinational logic to settle

            $display("Input = %h  |  Output = %h", word, y);
        end

        $display("Test finished.");
        $stop;
    end

endmodule
