def getBirthRegResponse(esData):
    response = {
        "data": {
            "numberOfRecords": 0,
            "responseRecords": []
        },
        "error": None,
        "type": "BIRTHREGISTRATION"
    }
    response['data']['numberOfRecords'] = len(esData)
    for data in esData:
        birthRegData = data['_source']
        response['data']['responseRecords'] = {
            "birthRegNo": birthRegData['birth_reg_no'] if 'birth_reg_no' in birthRegData else '',
            "personNameBN": birthRegData['person_name_bn'] if 'person_name_bn' in birthRegData else '',
            "personNameEN":  birthRegData['person_name_en'] if 'person_name_en' in birthRegData else '',
            "personSex":  birthRegData['person_sex'] if 'person_sex' in birthRegData else '',
            "personBirthDate":  birthRegData['person_birth_date'] if 'person_birth_date' in birthRegData else '',
            "personRegDate":  birthRegData['person_reg_date'] if 'person_reg_date' in birthRegData else '',
            "personBirthPlaceBN":  birthRegData['person_birth_place_bn'] if 'person_birth_place_bn' in birthRegData else '',
            "personBirthPlaceEN":  birthRegData['person_birth_place_en'] if 'person_birth_place_en' in birthRegData else '',
            "motherNameBN":  birthRegData['mother_name_bn'] if 'mother_name_bn' in birthRegData else '',
            "motherNameEN":  birthRegData['mother_name_en'] if 'mother_name_en' in birthRegData else '',
            "motherNatBN":  birthRegData['mother_nat_bn'] if 'mother_nat_bn' in birthRegData else '',
            "motherNatEN":  birthRegData['mother_nat_en'] if 'mother_nat_en' in birthRegData else '',
            "fatherNameBN":  birthRegData['father_name_bn'] if 'father_name_bn' in birthRegData else '',
            "fatherNameEN":  birthRegData['father_name_en'] if 'father_name_en' in birthRegData else '',
            "fatherNatBN":  birthRegData['father_nat_bn'] if 'father_nat_bn' in birthRegData else '',
            "fatherNatEN":  birthRegData['father_nat_en'] if 'father_nat_en' in birthRegData else '',
            "regOffice":  birthRegData['reg_office'] if 'reg_office' in birthRegData else ''
        }
    
    return response
