module sub_bytes_64bits
(
    input  wire [15:0] msg,
    output wire [15:0] y
);

    s_box_4bit nibble0  ( .word(msg[15:12]), .y(y[15:12]) );
    s_box_4bit nibble1  ( .word(msg[11:8]),  .y(y[11:8]) );
    s_box_4bit nibble2  ( .word(msg[7:4]),   .y(y[7:4]) );
    s_box_4bit nibble3  ( .word(msg[3:0]),  .y(y[3:0]) );

endmodule