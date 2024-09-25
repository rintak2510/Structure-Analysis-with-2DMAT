normalization = "TOTAL"
Rfactor = 'A'
first_degree = 0.3
last_degree = 6.5
row_number = 2  #surf-bulkP.sの00スポットが何列目にあるかを記入
omega = 0.3 #ガウス関数の半値幅を記入
first_line = 5
last_line = round(4+ (last_degree-(first_degree-0.1))/0.1)

def read_file()
    file_to_read = input()
    file_reader = open(file_to_read, "r")
    f = file_reader.readlines()
    file_reader.close()
    return f

original = read_file()
compared_to = read_file()

degree = []
c_list = []
e_list = []

#両方の角度を合致させるコードを書く。今回は保証されているものとする。

for element in clines[first_line-1 : last_line]:
    element = element.replace(",", "")
    data = element.split()
    degree.append(float(data[0]))
    c_list.append(float(data[row_number-1]))

new_c_list = []
for index in range(len(c_list)):
    integral = 0.0
    for index2 in range(len(c_list)):
        integral += c_list[index2] * g(degree[index] - degree[index2]) * 0.1
    new_c_list.append(integral)
c_list = new_c_list


for volume in f:
        data =volume.split()
        e_list.append(float(data[1]))
    if normalization == "TOTAL":
        e_norm = sum(e_list)
        c_norm = sum(c_list)
    else:
        e_norm = max(e_list)
        c_norm = max(c_list)

    e_list = np.array(e_list)/e_norm
    c_list = np.array(c_list)/c_norm

    if Rfactor =='A':
        r=0
        for i in range(len(c_list)):
            r+= (np.abs(c_list[i] - e_list[i]))**2
            
        r = np.sqrt(r)

    elif Rfactor == 'B':
        y1 = 0.0
        for i in range(len(degree)):
            y1 = y1+(e_list[i]-c_list[i])**2.0
        
        y2 = 0.0
        for i in range(len(degree)):
            y2 = y2 + e_list[i]**2.0
        y3 = 0.0
        for i in range(len(e_list)):
            y3 = y3+c_list[i]**2.0
        r = y1/(y2+y3)

   # plot(r)
   # ax1.scatter(degree, e_list, marker="$o$",linewidth=0.0,color="red",label ="experiment")
   # plt.legend()
   # plt.savefig("RockingCurve.png")
   # plt.show()

