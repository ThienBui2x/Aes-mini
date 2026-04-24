# Small Scale AES Implementation  #

## Exercise 1 - Description ##
###         Goals          ###
- The goal of the exercise sheets is to design a smaller variant of the Advanced
Encryption Standard (AES), which is widely used for encryption. This smaller version of the AES
is called small scale AES. 
- In the exercises, we will first focus on implementing, in verilog, an SR∗(10, 4, 4, 4) variant. That is to say, a "full size" AES (4 ∗ 4 state matrix) but with 4 bit SBoxes.
###  Brief Introduction    ###
- The AES, and by extension the small scale AES, is a substitution–permutation network (SPN) block cipher. It is composed of several operations that modify a state matrix. In the case of the AES, it is a 4 ∗ 4 state matrix with 8 bit words (FIPS 197 Component Ordering). The operations are the following:
    * SubBytes: substitution of all words in the state matrix using a Substitution Box (SBox),usually implemented as a lookup table
    * ShiftRows: left shift of all lines of the state matrix, according to their index
    * MixColumns: multiplication of each column by a Maximum Distance Separable (MDS) matrix and primary source of diffusion
    * AddRoundKey: round key XOR
- All small scale variants are defined as follows, SR(n, r, c, e) or SR∗(n, r, c, e):
    * ∗ specifies the possible omission of the mix column operation in the last round
    * n is the number of rounds, from 1 to 10
    * r and c are, respectively, the number of rows and columns of the state matrix, either 1, 2 or 4
    * e is the word size, 4 or 8 bits

## Exercise 2 - Description ##
###         Goals          ###
###  Brief Introduction    ###

## Exercise 3 - Description ##
###         Goals          ###
###  Brief Introduction    ###
