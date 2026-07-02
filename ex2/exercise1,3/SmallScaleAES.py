from numpy import uint8,uint32
from typing import List
from InverseSBOX import InverseSBOX
from SBOX import SBOX

class SmallScaleAES:
    def __init__(self, rounds:uint8, rows:uint8, cols:uint8 ,wordSize:uint8):
        self.m_NoRounds = rounds
        self.m_NoRows = rows
        self.m_NoCols = cols
        self.m_WordSize = wordSize
        self.m_SkipLastMc = True
        self.m_ReverseBitOrder = False
        self.m_NoBlocks = rows*cols
        self.m_Data = None
        self.m_Key = None

        # S-Box
        self.m_SBox = SBOX(self.m_WordSize)
        # Inverse S-Box
        self.m_InverseSBox = InverseSBOX(self.m_WordSize)
        # Round Constants
        self.m_RoundConstant = [0x1, 0x2, 0x4, 0x8, 0x3, 0x6, 0xC, 0xB, 0x5, 0xA] 
    
    def Encrypt(self,data:List[uint8], key:List[uint8]):
        self.m_Data = data.copy()
        self.m_Key = key.copy()

        for b in range(0,self.m_NoBlocks):
            self.m_Data[b] = self.m_Data[b] ^  self.m_Key[b]
        
        for round in range(0, self.m_NoRounds):

            # Compute Key Schedule for this round
            self.UpdateKeySchedule(round)
            
            # Perform S-Box Substitution
            self.SubBytes()

            # Shift Rows
            self.ShiftRows()

            # Mix Columns
            if not (self.m_SkipLastMc) or not(round == self.m_NoRounds - 1):
                self.MixColumns()

            # Add Round Key
            for b in range(self.m_NoBlocks):
                self.m_Data[b] = self.m_Data[b] ^ self.m_Key[b]

    def ShiftRows(self):
        if self.m_NoRows == 1 or self.m_NoCols == 1:
            return
        for r in range(1, self.m_NoRows):
            for shift in range(r):
                if self.m_NoCols == 2:
                    #swap the two elements
                    self.SwapDataElements(r, r + self.m_NoRows)

                else:
                    self.SwapDataElements(r, r + self.m_NoRows)
                    self.SwapDataElements(r + self.m_NoRows, r + 2*self.m_NoRows)
                    self.SwapDataElements(r + 2*self.m_NoRows, r + 3*self.m_NoRows)
    
    def SwapDataElements(self,e1:uint8,e2:uint8):
        temp = self.m_Data[e1]
        self.m_Data[e1] = self.m_Data[e2]
        self.m_Data[e2] = temp
              
    def SubBytes(self):
        for b in range(self.m_NoBlocks):
            self.m_Data[b] = self.m_SBox[self.m_Data[b]] 
    
    def UpdateKeySchedule(self, round:uint8):

        if self.m_NoCols == 1:
            self.KeyScheduleFunction(round, 0)

        elif self.m_NoCols == 2:
            col1: uint32 = self.TransferKeyColToInteger(0)
            col2: uint32 = self.TransferKeyColToInteger(1)

            #perform the key schedule function on the 2nd column
            self.KeyScheduleFunction(round, 1)

            col2afterKS: uint32 = self.TransferKeyColToInteger(1)
            temp1: uint32 = col1 ^ col2afterKS

            # the first column is XOR
            self.TransferIntegerToKeyCol(0,temp1)

            temp2: uint32 = temp1 ^ col2
            self.TransferIntegerToKeyCol(1, temp2)

        elif self.m_NoCols == 4:
            col1: uint32 = self.TransferKeyColToInteger(0)
            col2: uint32 = self.TransferKeyColToInteger(1)
            col3: uint32 = self.TransferKeyColToInteger(2)
            col4: uint32 = self.TransferKeyColToInteger(3)

            #perform the key schedule function on the 4th column
            self.KeyScheduleFunction(round, 3)

            col4afterKS: uint32 = self.TransferKeyColToInteger(3)

            temp1: uint32 = col1 ^ col4afterKS
            temp2: uint32 = temp1 ^ col2
            temp3: uint32 = temp2 ^ col3
            temp4: uint32 = temp3 ^ col4

            self.TransferIntegerToKeyCol(0, temp1)
            self.TransferIntegerToKeyCol(1, temp2)
            self.TransferIntegerToKeyCol(2, temp3)
            self.TransferIntegerToKeyCol(3, temp4)

    def KeyScheduleFunction(self, round:uint8, col:uint8):
        e1 = col*self.m_NoRows
        e2 = col*self.m_NoRows + 1
        e3 = col*self.m_NoRows + 2
        e4 = col*self.m_NoRows + 3

        # Apply S-box
        self.m_Key[e1] = self.m_SBox[self.m_Key[e1]]
        
        if (self.m_NoRows >= 2):
            self.m_Key[e2] = self.m_SBox[self.m_Key[e2]]
        if (self.m_NoRows >= 4):
            self.m_Key[e3] = self.m_SBox[self.m_Key[e3]]
            self.m_Key[e4] = self.m_SBox[self.m_Key[e4]]

        # Swap elements
        if (self.m_NoRows == 2):
            self.SwitchKeyElements(e1, e2)
        elif (self.m_NoRows == 4):
            self.SwitchKeyElements(e1, e4)
            self.SwitchKeyElements(e2, e3)

        # Add round constant
        self.m_Key[e1] = self.m_Key[e1] ^ self.m_RoundConstant[round]


    def SwitchKeyElements(self,e1:uint8,e2:uint8):
        temp = self.m_Key[e1]
        self.m_Key[e1] = self.m_Key[e2]
        self.m_Key[e2] = temp

        
    def TransferKeyColToInteger(self, col: uint8) -> uint32:
        e1 = col * self.m_NoRows
        e2 = col * self.m_NoRows + 1
        e3 = col * self.m_NoRows + 2
        e4 = col * self.m_NoRows + 3

        target = self.m_Key[e1] << 24

        if self.m_NoRows >= 2:
            target |= self.m_Key[e2] << 16
        if self.m_NoRows >= 4:
            target |= self.m_Key[e3] << 8
            target |= self.m_Key[e4]

        return target

    
    def TransferIntegerToKeyCol(self,col:uint8, value:uint32):

        e1:uint8 = col*self.m_NoRows
        e2:uint8 = col*self.m_NoRows + 1
        e3:uint8 = col*self.m_NoRows + 2
        e4:uint8 = col*self.m_NoRows + 3   

        self.m_Key[e1] = (value >> 24) & 0xFF
        
        if self.m_NoRows >= 2:
            self.m_Key[e2] = (value >> 16) & 0xFF
        if self.m_NoRows >= 4:
            self.m_Key[e3] = (value >> 8) & 0xFF
            self.m_Key[e4] = value & 0xFF

    def MixColumns(self):
        if self.m_NoCols == 1:
            return
        for c in range(self.m_NoCols):
            if self.m_NoRows == 2:
                self.MixColumn_2(c*self.m_NoRows , c*self.m_NoRows+1)
            else:
                self.MixColumn_4(c*self.m_NoRows,c*self.m_NoRows+1,c*self.m_NoRows+2,c*self.m_NoRows+3)

    def MixColumn_2(self,e1:uint8,e2:uint8):
        #Read the data
        val1:uint8 = self.m_Data[e2]
        val2:uint8 = self.m_Data[e1]

        # Temporary variables
        val1d:uint8 = val1 << 1
        val2d:uint8 = val2 << 1
        if self.m_WordSize == 4:
            if (val1 & 0x8) != 0:
                val1d = val1d ^ 0x13
            if (val2 & 0x8) != 0:
                val2d = val2d ^ 0x13
        else:
            if (val1 & 128) != 0:
                val1d = val1d ^ 27
            if (val2 & 128) != 0:
                val2d = val2d ^ 27

        val1t:uint8 = val1d ^ val1
        val2t:uint8 = val2d ^ val2

        self.m_Data[e2] = val1t ^ val2d
        self.m_Data[e1] = val2t ^ val1d

    def MixColumn_4(self,e1:uint8,e2:uint8,e3:uint8,e4:uint8):
        #Read the data
        val1:uint8 = self.m_Data[e4]
        val2:uint8 = self.m_Data[e3]
        val3:uint8 = self.m_Data[e2]
        val4:uint8 = self.m_Data[e1]

        # Temporary variables
        val1d:uint8 = val1 << 1
        val2d:uint8 = val2 << 1
        val3d:uint8 = val3 << 1
        val4d:uint8 = val4 << 1

        if self.m_WordSize == 4:
            if (val1 & 0x8) != 0:
                val1d = val1d ^ 0x13
            if (val2 & 0x8) != 0:
                val2d = val2d ^ 0x13
            if (val3 & 0x8) != 0:
                val3d = val3d ^ 0x13
            if (val4 & 0x8) != 0:
                val4d = val4d ^ 0x13
        else:
            if (val1 & 128) != 0:
                val1d = val1d ^ 0x1B
            if (val2 & 128) != 0:
                val2d = val2d ^ 0x1B
            if (val3 & 128) != 0:
                val3d = val3d ^ 0x1B
            if (val4 & 128) != 0:
                val4d = val4d ^ 0x1B

        val1t:uint8 = val1d ^ val1
        val2t:uint8 = val2d ^ val2
        val3t:uint8 = val3d ^ val3
        val4t:uint8 = val4d ^ val4

        self.m_Data[e4] = val4t ^ val3  ^ val2  ^ val1d
        self.m_Data[e3] = val4  ^ val3  ^ val2d ^ val1t
        self.m_Data[e2] = val4  ^ val3d ^ val2t ^ val1
        self.m_Data[e1] = val4d ^ val3t ^ val2  ^ val1


    def EncryptWithFault(self,data:List,key:List,targetRound:int,fault:List):
        self.m_Data = data.copy();
        self.m_Key = key.copy();

        # print("Initial Data:", self.m_Data)

        for b in range(0,self.m_NoBlocks):
            self.m_Data[b] = self.m_Data[b] ^  self.m_Key[b]
        
        for round in range(0, self.m_NoRounds):

            if round == targetRound - 1:
                for b in range(self.m_NoBlocks):
                    self.m_Data[b] ^= fault[b]

            # Compute Key Schedule for this round
            self.UpdateKeySchedule(round)
            
            # Perform S-Box Substitution
            self.SubBytes()

            # Shift Rows
            self.ShiftRows()

            # Mix Columns
            if not (self.m_SkipLastMc) or not(round == self.m_NoRounds - 1):
                self.MixColumns()

            # Add Round Key
            for b in range(self.m_NoBlocks):
                self.m_Data[b] = self.m_Data[b] ^ self.m_Key[b]
            

    def ReverseKeySchedule(self, key: List[uint8], startRound: uint8):
        """
        Reverse the key schedule from startRound back to round 0
        """
        
        if self.m_NoRows == 1 and self.m_NoCols == 1:
            for i in range(startRound, -1, -1):
                key[0] ^= self.m_RoundConstant[i]
                key[0] = self.m_InverseSBox[key[0]]
        
        elif self.m_NoRows == 1 and self.m_NoCols == 2:
            for i in range(startRound, -1, -1):
                key[1] ^= key[0]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[1]]
        
        elif self.m_NoRows == 1 and self.m_NoCols == 4:
            for i in range(startRound, -1, -1):
                key[3] ^= key[2]
                key[2] ^= key[1]
                key[1] ^= key[0]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[3]]
        
        elif self.m_NoRows == 2 and self.m_NoCols == 1:
            for i in range(startRound, -1, -1):
                storedKeyPart0 = key[1]
                
                key[1] = key[0] ^ self.m_RoundConstant[i]
                key[1] = self.m_InverseSBox[key[1]]
                key[0] = self.m_InverseSBox[storedKeyPart0]
        
        elif self.m_NoRows == 2 and self.m_NoCols == 2:
            for i in range(startRound, -1, -1):
                key[3] ^= key[1]
                key[2] ^= key[0]
                key[1] ^= self.m_SBox[key[2]]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[3]]
        
        elif self.m_NoRows == 2 and self.m_NoCols == 4:
            for i in range(startRound, -1, -1):
                key[7] ^= key[5]
                key[6] ^= key[4]
                key[5] ^= key[3]
                key[4] ^= key[2]
                key[3] ^= key[1]
                key[2] ^= key[0]
                key[1] ^= self.m_SBox[key[6]]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[7]]
        
        elif self.m_NoRows == 4 and self.m_NoCols == 1:
            for i in range(startRound, -1, -1):
                storedKeyPart0 = key[3]
                storedKeyPart1 = key[2]
                storedKeyPart2 = key[1]
                
                key[3] = key[0] ^ self.m_RoundConstant[i]
                key[3] = self.m_InverseSBox[key[3]]
                key[2] = self.m_InverseSBox[storedKeyPart0]
                key[1] = self.m_InverseSBox[storedKeyPart1]
                key[0] = self.m_InverseSBox[storedKeyPart2]
        
        elif self.m_NoRows == 4 and self.m_NoCols == 2:
            for i in range(startRound, -1, -1):
                key[7] ^= key[3]
                key[6] ^= key[2]
                key[5] ^= key[1]
                key[4] ^= key[0]
                key[3] ^= self.m_SBox[key[4]]
                key[2] ^= self.m_SBox[key[5]]
                key[1] ^= self.m_SBox[key[6]]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[7]]
        
        elif self.m_NoRows == 4 and self.m_NoCols == 4:
            for i in range(startRound, -1, -1):
                key[15] ^= key[11]
                key[14] ^= key[10]
                key[13] ^= key[9]
                key[12] ^= key[8]
                key[11] ^= key[7]
                key[10] ^= key[6]
                key[9] ^= key[5]
                key[8] ^= key[4]
                key[7] ^= key[3]
                key[6] ^= key[2]
                key[5] ^= key[1]
                key[4] ^= key[0]
                key[3] ^= self.m_SBox[key[12]]
                key[2] ^= self.m_SBox[key[13]]
                key[1] ^= self.m_SBox[key[14]]
                key[0] ^= self.m_RoundConstant[i] ^ self.m_SBox[key[15]]
        
        else:
            raise ValueError("Invalid configuration for ReverseKeySchedule")
        
        return key


    def InverseSubBytes(self):
        """Inverse S-Box substitution"""
        for b in range(self.m_NoBlocks):
            self.m_Data[b] = self.m_InverseSBox[self.m_Data[b]]


    def InverseShiftRows(self):
        """Inverse Shift Rows - shift RIGHT instead of LEFT"""
        if self.m_NoRows == 1 or self.m_NoCols == 1:
            return
        
        for row in range(1, self.m_NoRows):
            # Shift right by row positions (opposite of ShiftRows)
            for shift in range(row):
                if self.m_NoCols == 2:
                    # For two columns, swap is its own inverse
                    self.SwapDataElements(row, row + self.m_NoRows)
                else:
                    # For 4 columns, shift right (reverse of left shift)
                    self.SwapDataElements(row + self.m_NoRows * 3, row + self.m_NoRows * 2)
                    self.SwapDataElements(row + self.m_NoRows * 2, row + self.m_NoRows)
                    self.SwapDataElements(row + self.m_NoRows, row)


    def InverseMixColumns(self):
        """Inverse Mix Columns operation"""
        if self.m_NoCols == 1:
            return
        
        for c in range(self.m_NoCols):
            if self.m_NoRows == 2:
                self.InverseMixColumn_2(c * self.m_NoRows, c * self.m_NoRows + 1)
            else:
                self.InverseMixColumn_4(c * self.m_NoRows, c * self.m_NoRows + 1,
                                    c * self.m_NoRows + 2, c * self.m_NoRows + 3)


    def InverseMixColumn_2(self, e1: uint8, e2: uint8):
        """
        Inverse MixColumn for 2 rows
        For the 2x2 case, the MixColumns matrix is self-inverse
        """
        self.MixColumn_2(e1, e2)

    def InverseMixColumn_4(self, e1: uint8, e2: uint8, e3: uint8, e4: uint8):
        """
        Inverse MixColumn for 4 rows
        """
        # Read the data in reverse order
        val1 = self.m_Data[e4]
        val2 = self.m_Data[e3]
        val3 = self.m_Data[e2]
        val4 = self.m_Data[e1]
        
        # Create mask based on word size
        mask = (1 << self.m_WordSize) - 1
        high_bit = 1 << (self.m_WordSize - 1)
        poly = 0x13 if self.m_WordSize == 4 else 0x1B
        
        # Compute val*2
        val1_2 = val1 << 1
        val2_2 = val2 << 1
        val3_2 = val3 << 1
        val4_2 = val4 << 1
        
        if (val1 & high_bit) != 0:
            val1_2 ^= poly
        if (val2 & high_bit) != 0:
            val2_2 ^= poly
        if (val3 & high_bit) != 0:
            val3_2 ^= poly
        if (val4 & high_bit) != 0:
            val4_2 ^= poly
        
        val1_2 &= mask
        val2_2 &= mask
        val3_2 &= mask
        val4_2 &= mask
        
        # Compute val*4
        val1_4 = val1_2 << 1
        val2_4 = val2_2 << 1
        val3_4 = val3_2 << 1
        val4_4 = val4_2 << 1
        
        if (val1_2 & high_bit) != 0:
            val1_4 ^= poly
        if (val2_2 & high_bit) != 0:
            val2_4 ^= poly
        if (val3_2 & high_bit) != 0:
            val3_4 ^= poly
        if (val4_2 & high_bit) != 0:
            val4_4 ^= poly
        
        val1_4 &= mask
        val2_4 &= mask
        val3_4 &= mask
        val4_4 &= mask
        
        # Compute val*8
        val1_8 = val1_4 << 1
        val2_8 = val2_4 << 1
        val3_8 = val3_4 << 1
        val4_8 = val4_4 << 1
        
        if (val1_4 & high_bit) != 0:
            val1_8 ^= poly
        if (val2_4 & high_bit) != 0:
            val2_8 ^= poly
        if (val3_4 & high_bit) != 0:
            val3_8 ^= poly
        if (val4_4 & high_bit) != 0:
            val4_8 ^= poly
        
        val1_8 &= mask
        val2_8 &= mask
        val3_8 &= mask
        val4_8 &= mask
        
        # Compute 9, B, D, E
        val1_9 = val1_8 ^ val1
        val1_B = val1_8 ^ val1_2 ^ val1
        val1_D = val1_8 ^ val1_4 ^ val1
        val1_E = val1_8 ^ val1_4 ^ val1_2
        
        val2_9 = val2_8 ^ val2
        val2_B = val2_8 ^ val2_2 ^ val2
        val2_D = val2_8 ^ val2_4 ^ val2
        val2_E = val2_8 ^ val2_4 ^ val2_2
        
        val3_9 = val3_8 ^ val3
        val3_B = val3_8 ^ val3_2 ^ val3
        val3_D = val3_8 ^ val3_4 ^ val3
        val3_E = val3_8 ^ val3_4 ^ val3_2
        
        val4_9 = val4_8 ^ val4
        val4_B = val4_8 ^ val4_2 ^ val4
        val4_D = val4_8 ^ val4_4 ^ val4
        val4_E = val4_8 ^ val4_4 ^ val4_2
        
        self.m_Data[e4] = val4_B ^ val3_D ^ val2_9 ^ val1_E
        self.m_Data[e3] = val4_D ^ val3_9 ^ val2_E ^ val1_B
        self.m_Data[e2] = val4_9 ^ val3_E ^ val2_B ^ val1_D
        self.m_Data[e1] = val4_E ^ val3_B ^ val2_D ^ val1_9


    def Decrypt(self, data: List[uint8], key: List[uint8]):
        """
        Decrypt ciphertext with the given key
        """
        self.m_Data = data.copy()
        self.m_Key = key.copy()
        
        
        # Generate all round keys first
        round_keys = []
        temp_key = key.copy()
        round_keys.append(temp_key.copy())
        
        for round in range(self.m_NoRounds):
            self.m_Key = temp_key.copy()
            self.UpdateKeySchedule(round)
            temp_key = self.m_Key.copy()
            round_keys.append(temp_key.copy())
        
        # Process rounds in reverse
        for round in range(self.m_NoRounds - 1, -1, -1):
            # XOR with round_keys[round + 1]
            for b in range(self.m_NoBlocks):
                self.m_Data[b] ^= round_keys[round + 1][b]
            
            
            # Inverse Mix Columns
            if round != self.m_NoRounds - 1 or not self.m_SkipLastMc:
                self.InverseMixColumns()
            
            # Inverse Shift Rows
            self.InverseShiftRows()
            
            # Inverse SubBytes
            self.InverseSubBytes()
        
        for b in range(self.m_NoBlocks):
            self.m_Data[b] ^= round_keys[0][b]
        

if __name__ == "__main__":
    """
        Example usage of SmallScaleAES

        data: Data to be encrypted
        key: Encryption key
        cipher_text: Resulting ciphertext after encryption
    """
    aes = SmallScaleAES(rounds=10, rows=4, cols=4, wordSize=4)

    data = [0x0, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
    key = [0xF, 0xE, 0xD, 0xC,0xB,0xA,0x9,0x8,0x7,0x6,0x5,0x4,0x3,0x2,0x1,0x0]
    f_round = 8
    fault = [0xF, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
    print("Initial Data:", data)
    aes.Encrypt(data, key)
    print("Encrypted Data:", aes.m_Data)
    cipher_text = aes.m_Data.copy()
    print("Cipher Text:", cipher_text)
    aes.Decrypt(cipher_text, key)
    print("Decrypted Data:", aes.m_Data)
    print("Fault:", fault, " & Location:", f_round)
    aes.EncryptWithFault(data, key, f_round, fault)
    print("Faulty Ciphertext:", aes.m_Data)