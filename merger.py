
def merge(list1,list2):
    result = []
    for element in list1 + list2:
        try:
            index = next(i for i, x in enumerate(result) if x['Name'] == element['Name'])
        except StopIteration:
            index=None


        if index is not None:
            result[index]['Shop'].append({
                "Shop_name": 'kupa',
                "Price": element["Price"],
                "Link": element["Link"]
            })
        else:
            result.append({
                "Name": element["Name"],
                "Img": element["Img"],
                "Shop": [
                    {
                        "Shop_name": "kupa",
                        "Price": element["Price"],
                        "Link": element["Link"]
                    }
                ]
            })
    return result


#if __name__ == '__main__':
    #merge(list1,list2)
    #merge_rest(result,list1,list2)
