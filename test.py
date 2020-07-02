data = ((2, '123456789', 'Lupin', '10', '60'), (3, '123456789', 'Tonic', '10', '1220'), (2, '123456789', 'Lupin', '10', '60'))
#medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
no_need = [0,1]
medicine_data =[]
for record in data:
    ls = []
    for item in range(len(record)):
        if item not in no_need:
            if item ==4:
                ls.append(f"RS.{int(record[4]) / int(record[3])}")
            ls.append(record[item])
    medicine_data.append(ls)
print(medicine_data)



