import numpy as np
from ham_w import ham_w

# CPA Parameters
nibbleStart = 0
nibbleEnd = 16
keyCandidateStart = 0
keyCandidateStop = 15
solvedKey = np.zeros((1,nibbleEnd))

# SBox
SBOX=[6,11,5,4,2,14,7,10,9,13,15,12,3,1,0,8]
SBOX = np.array(SBOX)
plaintexts = np.load(plaintexts_path_npy, mmap_mode="c")

for nibble in range(nibbleStart, nibbleEnd):

    bestCorr = -inf
    bestKey  = 0

    for i in range(keyCandidateStart, keyCandidateStop+1):

        # Step 1: Hypothesis
        h_i = np.zeros((1,n))
        for k in range(n):   # traces
            h_i[k] = ham_w(x_i[k])

        # Step 2: Correlation for each sample point j
        for j in range(p):
            # initialize sums
            sum_h      = 0
            sum_d      = 0
            sum_h2     = 0
            sum_d2     = 0
            sum_hd     = 0
            # loop over traces
            for k in range(n):
                d_jk = trace[k][j]     # data point j of trace k

                sum_h  += h_i[k]
                sum_d  += d_jk
                sum_h2 += h_i[k] * h_i[k]
                sum_d2 += d_jk * d_jk
                sum_hd += h_i[k] * d_jk

            # compute correlation using the formula
            numerator   = n * sum_hd - (sum_h * sum_d)
            denominator = sqrt( (n*sum_h2 - sum_h^2) * (n*sum_d2 - sum_d^2) )

            rho[i][j] = numerator / denominator
            if rho > bestCorr:
                bestCorr = rho
                bestKey  = keyGuess

    solvedKey[nibble] = bestKey