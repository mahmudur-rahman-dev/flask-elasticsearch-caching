def generate(index, value):
    column_name = ""
    
    if index == "esaf":
        column_name = "phone"
    elif index == "passport":
        column_name = "passport_number"
    elif index == "driving-license":
        column_name = "license_number"
    elif index == "birth_registration":
        column_name = "birth_reg_no"
    elif index == "nid10Digit":
        column_name = "nid_10_digit"
    elif index == "nid13Digit":
        column_name = "nid_13_digit"
    elif index == "nid17Digit":
        column_name = "nid_17_digit"

    query_body = {"query":{"bool":{"must":[{"match":{column_name : value}}],"must_not":[],"should":[]}}}
    return query_body
