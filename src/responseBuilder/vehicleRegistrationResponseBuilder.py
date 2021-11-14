def getVehicleRegistrationResponse(esData):

    
    response = {
        "data": {},
        "error": None,
        "type": "VEHICLEREGISTRATION"
    }
    if len(esData)  == 0 :
        return response
    data = esData[0]['_source']
    response['data'] = {
            "registrationNumber": data['registration_number'],
            "vehicleNumber": data['vehicle_number'],
            "vehicleRegistrationNumber": data['vehicle_registration_number'],
            "ownerName": data['owner_name'],
            "ownerAddress": data['owner_address'],
            "registrationDate": data['registration_date'],
            "registrationOfficeName": data['registration_office_name'],
            "routePermitNumber": data['route_permit_number'],
            "routePermitIssueDate": data['route_permit_issue_date'],
            "routePermitExpDate": data['route_permit_exp_date'],
            "taxTokenIssueDate": data['tax_token_issue_date'],
            "taxTokenExpDate": data['tax_token_exp_date'],
            "fitnessIssueDate": data['fitness_issue_date'],
            "fitnessExpDate": data['fitness_exp_date'],
            "vehicleColour": data['vehicle_colour'],
            "nidNumber": data['nid_number'] if 'nid_number' in data else '',
            "mobileNumber": data['mobile_number'],
            "vehicleSeries": data['vehicle_series']
        }
    return response
