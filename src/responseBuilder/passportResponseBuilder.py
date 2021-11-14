def getPassportResponse(esData):
    response = {
        "data": {
            "numberofRecordsFound": 0,
            "passportRecords": []
        },
        "error": None,
        "type": "PASSPORT"
    }
    response['data']['numberofRecordsFound'] = len(esData)
    if len(esData) == 0 :
        return response

    for data in esData:
        data = data['_source']
        passportRecord = {
            "bangladeshAddress": data['bangladesh_address'] if 'bangladesh_address' in data else '',
            "birthId": data['birth_id'] if 'birth_id' in data else '',
            "creationTimeStamp": data['creation_time_stamp'] if 'operator' in data else '',
            "dob": data['dob'] if 'dob' in data else '',
            "emergencyAddress": data['emergency_address'] if 'operator' in data else '',
            "facialImage": data['facial_image'] if 'facial_image' in data else '',
            "fatherName": data['father_name'] if 'father_name' in data else '',
            "finger2Image": data['finger2_image'] if 'finger2_image' in data else '',
            "finger3Image": data['finger3_image'] if 'finger3_image' in data else '',
            "finger4Image": data['finger4_image'] if 'finger4_image' in data else '',
            "fingerlImage": data['fingerlimage'] if 'fingerlimage' in data else '',
            "firstName": data['first_name'] if 'first_name' in data else '',
            "fullName": data['full_name'] if 'full_name' in data else '',
            "gender": data['gender'] if 'gender' in data else '',
            "height": data['height'] if 'height' in data else '',
            "lastName": data['last_name'] if 'last_name' in data else '',
            "maritalStatus": data['marital_status'] if 'marital_status' in data else '',
            "mobileNumber": data['mobile_number'] if 'mobile_number' in data else '',
            "modificationTimeStamp": data['modification_time_stamp'] if 'modification_time_stamp' in data else '',
            "motherName": data['mother_name'] if 'mother_name' in data else '',
            "nationalID": data['national_id'] if 'national_id' in data else '',
            "nationality": data['nationality'] if 'nationality' in data else '',
            "pob": data['pob'] if 'pob' in data else '',
            "passportNumber": data['passport_number'] if 'passport_number' in data else '',
            "passportStatus": data['passport_status'] if 'passport_status' in data else '',
            "passportType": data['passport_type'] if 'passport_type' in data else '',
            "permAddress": data['perm_address'] if 'perm_address' in data else '',
            "presentAddress": data['present_address'] if 'present_address' in data else '',
            "previousPassportNumber": data['previous_passport_number'] if 'previous_passport_number' in data else '',
            "profession": data['profession'] if 'profession' in data else '',
            "religion": data['religion'] if 'religion' in data else '',
            "revoked": data['revoked'] if 'revoked' in data else '',
            "revokedDate": data['revoked_date'] if 'revoked_date' in data else '',
            "signature": data['signature'] if 'signature' in data else '',
            "spouseName": data['spouse_name'] if 'spouse_name' in data else '',
            "typeCitizen": data['type_citizen'] if 'type_citizen' in data else '',
            "doExpiry": data['do_expiry'] if 'do_expiry' in data else '',
            "doIssue": data['do_issue'] if 'do_issue' in data else ''
        }
        response['data']['passportRecords'].append(passportRecord)
    
    return response
