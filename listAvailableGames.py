import streamlit as st

@st.cache
def merge(list):
    result = []
    for element in list:
        try:
            index = next(i for i, x in enumerate(result) if x["Name"] == element[1])
        except StopIteration:
            index=None


        if index is not None:
            result[index]['Shop'].append({
                "Shop_name": element[3],
                "Price": element[5],
                "Link": element[4]
            })
        else:
            result.append({
                "Name": element[1],
                "Img": element[2],
                "Shop": [
                    {
                        "Shop_name": element[3],
                        "Price": element[5],
                        "Link": element[4]
                    }
                ]
            })
    return result

