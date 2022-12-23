result=[]
def merge(list1,list2):
    x=list1[1]
    y=list2[1]

    for element in list1:
        if element["Name"] in list2["Name"]:
            result.append({
                "Name": element["Name"],
                "Img": element["Img"],
                "Shop": [
                    {
                        "Shop_name": x,
                        "Price": element["Price"],
                        "Link": element["Link"]
                    },
                    {
                        "Shop_name": y,
                        "Price": list2[element["Name"]]["Price"],
                        "Link": list2[element["Name"]]["Link"]
                    }
                ]
            })




def merge_rest(result,list1,list2):

    for elem in list1,list2:
        if "mepel" in elem["Link"]:
            shop="mepel.pl"
        else:
            shop="ShopGracz"

        if elem not in result:
            result.append({
                "Name": elem["Name"],
                "Img": elem["Img"],
                "Shop": [
                    {
                        "Shop_name": shop,
                        "Price": elem["Price"],
                        "Link": elem["Link"]
                    }
                ]
            })
def merge_all(list1,list2):
    res=merge(list1,list2)
    merge_rest(res, list1, list2)

    return result

#if __name__ == '__main__':
    #merge(list1,list2)
    #merge_rest(result,list1,list2)
