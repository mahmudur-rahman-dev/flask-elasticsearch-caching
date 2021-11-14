def getNidResponse(esData):
    response = {
        "data": {},
        "error": None,
        "type": "NID"
    }
    responseData ={}
    if len(esData)>0:
        nid = esData[0]['_source']
        responseData = {
            "requestId": nid["request_id"] if 'request_id' in nid else '',
            "name": nid["name"] if 'name' in nid else '',
            "nameEn": nid["name_en"] if 'name_en' in nid else '',
            "gender": nid["gender"] if 'gender' in nid else '',
            "bloodGroup": nid["blood_group"] if 'blood_group' in nid else '',
            "dateOfBirth": nid["date_of_birth"] if 'date_of_birth' in nid else '',
            "father": nid["father"] if 'father' in nid else '',
            "mother": nid["mother"] if 'mother' in nid else '',
            "spouse": nid["spouse"] if 'spouse' in nid else '',
            "nid10Digit": nid["nid_10_digit"] if 'nid_10_digit' in nid else '',
            "occupation": nid["occupation"] if 'occupation' in nid else '',
            "permanentAddress": {
                "division": nid["permanent_address"]["division"] if ('permanent_address' in nid) and ('division' in nid["permanent_address"]) else '',
                "district": nid["permanent_address"]["district"] if ('permanent_address' in nid) and ('district' in nid["permanent_address"]) else '',
                "rmo": nid["permanent_address"]["rmo"] if ('permanent_address' in nid) and ('rmo' in nid["permanent_address"]) else '',
                "upozila": nid["permanent_address"]["upozila"] if ('permanent_address' in nid) and ('upozila' in nid["permanent_address"]) else '',
                "postOffice": nid["permanent_address"]["post_office"] if ('permanent_address' in nid) and ('post_office' in nid["permanent_address"]) else '',
                "postalCode": nid["permanent_address"]["postal_code"] if ('permanent_address' in nid) and ('postal_code' in nid["permanent_address"]) else '',
                "wardForUnionPorishod": nid["permanent_address"]["ward_for_union_porishod"] if ('permanent_address' in nid) and ('ward_for_union_porishod' in nid["permanent_address"]) else '',
                "additionalMouzaOrMoholla": nid["permanent_address"]["additional_mouza_or_moholla"] if ('permanent_address' in nid) and ('additional_mouza_or_moholla' in nid["permanent_address"]) else '',
                "additionalVillageOrRoad": nid["permanent_address"]["additional_village_or_road"] if ('permanent_address' in nid) and ('additional_village_or_road' in nid["permanent_address"]) else '',
                "homeOrHoldingNo": nid["permanent_address"]["home_or_holding_no"] if ('permanent_address' in nid) and ('home_or_holding_no' in nid["permanent_address"]) else '',
                "region": nid["permanent_address"]["region"] if ('permanent_address' in nid) and ('region' in nid["permanent_address"]) else '',

                "mouzaOrMoholla": nid["permanent_address"]["mouza_or_moholla"] if ('permanent_address' in nid) and ('mouza_or_moholla' in nid["permanent_address"]) else '',
                "unionOrWard": nid["permanent_address"]["union_or_ward"] if ('permanent_address' in nid) and ('union_or_ward' in nid["permanent_address"]) else '',
                "rmoCode": nid["permanent_address"]["rmo_code"]  if ('permanent_address' in nid) and ('rmo_code' in nid["permanent_address"]) else ''
            },
            "photo": nid["photo"]  if 'photo' in nid else '',
            "presentAddress": {
                "division": nid["present_address"]["division"] if ('present_address' in nid) and ('division' in nid["present_address"]) else '',
                "district": nid["present_address"]["district"] if ('present_address' in nid) and ('district' in nid["present_address"]) else '',
                "rmo": nid["present_address"]["rmo"] if ('present_address' in nid) and ('rmo' in nid["present_address"]) else '',
                "upozila": nid["present_address"]["upozila"] if ('present_address' in nid) and ('upozila' in nid["present_address"]) else '',
                "postOffice": nid["present_address"]["post_office"] if ('present_address' in nid) and ('post_office' in nid["present_address"]) else '',
                "postalCode": nid["present_address"]["postal_code"] if ('present_address' in nid) and ('postal_code' in nid["present_address"]) else '',
                "wardForUnionPorishod": nid["present_address"]["ward_for_union_porishod"] if ('present_address' in nid) and ('ward_for_union_porishod' in nid["present_address"]) else '',
                "additionalMouzaOrMoholla": nid["present_address"]["additional_mouza_or_moholla"] if ('present_address' in nid) and ('additional_mouza_or_moholla' in nid["present_address"]) else '',
                "additionalVillageOrRoad": nid["present_address"]["additional_village_or_road"] if ('present_address' in nid) and ('additional_village_or_road' in nid["present_address"]) else '',
                "homeOrHoldingNo": nid["present_address"]["home_or_holding_no"] if ('present_address' in nid) and ('home_or_holding_no' in nid["present_address"]) else '',
                "region": nid["present_address"]["region"] if ('present_address' in nid) and ('region' in nid["present_address"]) else '',
                "mouzaOrMoholla": nid["present_address"]["mouza_or_moholla"] if ('present_address' in nid) and ('mouza_or_moholla' in nid["present_address"]) else '',
                "unionOrWard": nid["present_address"]["union_or_ward"] if ('present_address' in nid) and ('union_or_ward' in nid["present_address"]) else '',
                "rmoCode": nid["present_address"]["rmo_code"]  if ('present_address' in nid) and ('rmo_code' in nid["present_address"]) else ''
            },
            "nid17Digit": nid["nid_17_digit"]  if 'nid_17_digit' in nid else '',
            "nid13Digit": nid["nid_13_digit"]  if 'nid_13_digit' in nid else '',
            "homeOrHoldingNo":nid["home_or_holding_no"]  if 'home_or_holding_no' in nid else '',
            "region": nid["region"]  if 'region' in nid else '',
            "mouzaOrMoholla": nid["mouza_or_moholla"]  if 'mouza_or_moholla' in nid else ''
        }
    response["data"]=responseData
    return response
