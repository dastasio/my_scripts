from itertools import combinations
Sums = [] * 46
print(Sums[45])
Digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for SumLength in range(2, 9):
   Combinations = combinations(Digits, SumLength)

   for Comb in Combinations:
       Sums[sum(Comb)]

for Sum in Sums:
    print('Sum {}'.format(sum(Sum[0])))
    for Combination in Sum:
        print('[', end='')
        for Digit in Combination:
            print(Digit, end='')
        print(']')
    print('')