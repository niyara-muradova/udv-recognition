from datetime import datetime

data = '990801401668'
data_list = list(data)

weight = [1,2,3,4,5,6,7,8,9,10,11]
c_digit = 0

for i in range(11):

    mult = weight[i]*int(data_list[i])
    c_digit += mult

c_digit = c_digit%11



