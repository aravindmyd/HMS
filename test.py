# data=((1, '987654321', 'Naveen', '28', '', 'General ward', 'Thiruvalluvar Nagar', 'Chennai', 'TamilNadu', 'active'), (553, '123456789', 'AV', '20', '2020-05-27', 'General ward', 'Ambattur', 'Chennai', 'TamilNadu', 'active'))
# for i in data:
#     count = 1
#     print("<tr>")
#     print(f"<th scope'row'>{count}</th>")
#     for j in i:
#         print(f"<td>{j}</td>")
#     print("</tr>")
#     count+=1
##SSNID	PATIENT NAME	AGE	DATE OF JOINING	TYPE OF ROOM	ADDRESS
data =((1, '987654321', 'Naveen', '28', '', 'General ward', 'Thiruvalluvar Nagar', 'Chennai', 'TamilNadu', 'active'), (553, '123456789', 'AV', '20', '2020-05-27', 'General ward', 'Ambattur', 'Chennai', 'TamilNadu', 'active'))
modified_ls = []
no_need=[0,7,8,9]
for i in data:
    ls = []
    for j in range(len(i)):
        if j not in no_need:
            ls.append(i[j])
    modified_ls.append(ls)
print(modified_ls)