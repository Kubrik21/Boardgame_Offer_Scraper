def merge(list1,list2):
    result = []
    for element in list1 + list2:
        try:
            index = next(i for i, x in enumerate(result) if x['Name'] == element['Name'])
        except StopIteration:
            index=None

        #getting name of store
        if "mepel.pl" in element["Link"]:
            shop="mepel.pl"
        else:
            shop="Shopgracz.pl"

        if index is not None:
            result[index]['Shop'].append({
                "Shop_name": shop,
                "Price": element["Price"],
                "Link": element["Link"]
            })
        else:
            result.append({
                "Name": element["Name"],
                "Img": element["Img"],
                "Shop": [
                    {
                        "Shop_name": shop,
                        "Price": element["Price"],
                        "Link": element["Link"]
                    }
                ]
            })
    return result

