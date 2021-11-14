def getDrivingLicenseResponse(esData):
    response = {
        "data": {
            "requestType": "licenseNumber",
            "numberofRecordsFound": 0,
            "drivingLicenseRecord": []
        },
        "error": None,
        "type": "DRIVINGLICENSE"
    }

    for data in esData:
        drivinglicenseData = data['_source']
        drivingLicenseRecord = {
            "applyDate": drivinglicenseData['apply_date']if 'apply_date' in drivinglicenseData else '',
            "bloodGroup": drivinglicenseData['blood_group']if 'blood_group' in drivinglicenseData else '',
            "dateOfBirth": drivinglicenseData['date_of_birth']if 'date_of_birth' in drivinglicenseData else '',
            "expiryDate": drivinglicenseData['expiry_date']if 'expiry_date' in drivinglicenseData else '',
            "fatherName": drivinglicenseData['father_name']if 'father_name' in drivinglicenseData else '',
            "gender": drivinglicenseData['gender']if 'gender' in drivinglicenseData else '',
            "issueDate": drivinglicenseData['issue_date']if 'issue_date' in drivinglicenseData else '',
            "issuingAuthority": drivinglicenseData['issuing_authority']if 'issuing_authority' in drivinglicenseData else '',
            "licenseNumber": drivinglicenseData['license_number']if 'license_number' in drivinglicenseData else '',
            "licenseType": drivinglicenseData['license_type']if 'license_type' in drivinglicenseData else '',
            "mobileNo": drivinglicenseData['mobile_no']if 'mobile_no' in drivinglicenseData else '',
            "name": drivinglicenseData['name']if 'name' in drivinglicenseData else '',
            "permanentAddress": drivinglicenseData['permanent_address']if 'permanent_address' in drivinglicenseData else '',
            "photo": drivinglicenseData['photo']if 'photo' in drivinglicenseData else '',
            "presentAddress": drivinglicenseData['present_address']if 'present_address' in drivinglicenseData else '',
            "renewalDate": drivinglicenseData['renewal_date']if 'renewal_date' in drivinglicenseData else '',
            "signature": drivinglicenseData['signature']if 'signature' in drivinglicenseData else '',
            "vehicleClasses": drivinglicenseData['vehicle_classes']if 'vehicle_classes' in drivinglicenseData else '',
            "nid": drivinglicenseData['nid'] if 'nid' in drivinglicenseData else '',
            "spouseName": drivinglicenseData['spouseName'] if 'spouseName' in drivinglicenseData else ''
        }
        response['data']['drivingLicenseRecord'].append(drivingLicenseRecord)
    response['data']['numberofRecordsFound'] = len(esData)
    return response
