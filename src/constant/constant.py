from src.constant import timePeriods

INDEX = {
    1: 'cdr', 2: 'esaf', 3: 'sms', 4: 'lrl', 5: 'nid', 6: 'passport', 7: 'driving-license', 8: 'vehicle'
}


def getEsSearchColumn(nid):
    return "nid_"+str(len(nid))+"_digit"


def getIndexColumns(data):
    return {
        'cdr': {1: 'party_a', 2: 'imei_number', 3: 'imsi'},
        'esaf': {1: 'phone', 4: 'nid'},
        'nid': {4: getEsSearchColumn(data['searchValue'])},
        'passport': {4: 'national_id', 5: 'passport_number'},
        'driving-license': {1: 'mobile_no', 4: 'nid', 6: 'license_number'}
    }


def getSearchCriteriaDict():
    return {1: "MSISDN", 2: "IMEI",
            3: "IMSI", 4: "NID", 10: "MSISDN"}

UnifiedViewerGroups = [
    {'key':'brnNumber','value': 'BRN Number'},
    {'key':'dob','value': 'Date of Birth'},
    {'key':'drivingLicenseNumber','value': 'Driving License Number'},
    {'key':'fatherName','value': 'Father Name'},
    {'key':'gender','value': 'Gender'},
    {'key':'mobileNumber','value': 'Mobile Number'},
    {'key':'motherName','value': 'Mother'},
    {'key':'name','value': 'Name'},
    {'key':'nid10Digit','value': 'NID 10 Digit'},
    {'key':'nid13Digit','value': 'NID 13 Digit'},
    {'key':'nid17Digit','value': 'NID 17 Digit'},
    {'key':'occupation','value': 'Occupation'},
    {'key':'passportNumber','value': 'Passport Number'},
    {'key':'permanentAddress','value': 'Permanent Address'},
    {'key':'perviousPassportNumber','value': 'Pervious Passport Number'},
    {'key':'photo','value': 'Photo'},
    {'key':'presentAddress','value': 'Present Address'},
    {'key':'spouseName','value': 'Spouse Name'}
]

UnifiedViewerMapper = {
    'cdr':  {
        'id':'',
        'name': 'name_en',
        'photo': '',
        'mobileNumber': 'imsi',
        'nid10Digit': '',
        'nid13Digit': '',
        'nid17Digit': '',
        'dob': '',
        'brnNumber': '',
        'drivingLicenseNumber': '',
        'passportNumber': '',
        'perviousPassportNumber': '',
        'presentAddress': '',
        'permanentAddress': '',
        'occupation': '',
        'gender': '',
        'spouseName': '',
        'fatherName': '',
        'motherName': '',
        },
    'esaf':  {
        'id':'phone',
        'name': 'name',
        'photo': '',
        'mobileNumber': 'phone',
        'nid10Digit': 'nid',
        'nid13Digit': 'nid',
        'nid17Digit': 'nid',
        'dob': 'birth_date',
        'brnNumber': '',
        'drivingLicenseNumber': '',
        'passportNumber': '',
        'perviousPassportNumber': '',
        'presentAddress': '',
        'permanentAddress': '',
        'occupation': '',
        'gender': '',
        'spouseName': '',
        'fatherName': '',
        'motherName': '',
        },
    'nid':  {
        'id':'nid_17_digit',
        'name': 'name_en',
        'photo': 'photo',
        'mobileNumber': '',
        'nid10Digit': 'nid_10_digit',
        'nid13Digit': 'nid_13_digit',
        'nid17Digit': 'nid_17_digit',
        'dob': 'date_of_birth',
        'brnNumber': '',
        'drivingLicenseNumber': '',
        'passportNumber': '',
        'perviousPassportNumber': '',
        'presentAddress': 'present_address',
        'permanentAddress': 'permanent_address',
        'occupation': 'occupation',
        'gender': 'gender',
        'spouseName': 'spouse',
        'fatherName': 'father',
        'motherName': 'mother',
        },
    'passport': {
        'id':'passport_number',
        'name': 'full_name',
        'photo': 'facial_image',
        'mobileNumber': 'mobile_number',
        'nid10Digit': 'national_id',
        'nid13Digit':  'national_id',
        'nid17Digit':  'national_id',
        'dob': 'dob',
        'brnNumber': '',
        'drivingLicenseNumber': '',
        'passportNumber': 'passport_number',
        
        'perviousPassportNumber': 'previous_passport_number',
        'presentAddress': 'present_address',
        'permanentAddress': 'perm_address',
        'occupation': 'profession',
        'gender': 'gender',
        'spouseName': 'spouse_name',
        'fatherName': 'father_name',
        'motherName': 'mother_name',
        },
    'driving-license':  {
         'id':'license_number',
        'name': 'name',
        'photo': 'photo',
        'mobileNumber': 'mobile_no',
        'nid10Digit': 'nid',
        'nid13Digit': 'nid',
        'nid17Digit': 'nid',
        'dob': 'date_of_birth',
        'brnNumber': '',
        'drivingLicenseNumber': 'license_number',
        'passportNumber': '',
        'perviousPassportNumber': '',
        'presentAddress': 'present_address',
        'permanentAddress': 'permanent_address',
        'occupation': '',
        'gender': 'gender',
        'spouseName': 'spouse_name',
        'fatherName': '',
        'motherName': '',
        },
    'vehicle':  {
         'id':'vehicle_registration_number',
        'name': 'owner_name',
        'photo': '',
        'mobileNumber': 'imsi',
        'nid10Digit': 'nationality',
        'nid13Digit': 'nationality',
        'nid17Digit': 'nationality',
        'dob': 'date_of_birth',
        'brnNumber': '',
        'drivingLicenseNumber': '',
        'passportNumber': '',
        'perviousPassportNumber': '',
        'presentAddress': 'owner_address',
        'permanentAddress': '',
        'occupation': '',
        'gender': '',
        'spouseName': '',
        'fatherName': '',
        'motherName': '',
        },
    }

requestTypeId = {
    'CDR': 1,
    'ESAF': 2,
    'SMS': 3,
    'LRL': 4,
    'NID': 5,
    'PASSPORT': 6,
    'DRIVING_LICENSE': 7,
    'DRIVINGLICENSE': 7,
    'VEHICLE_REGISTRATION': 8,
    'BIRTH_REGISTRATION': 9,
    'VEHICLEREGISTRATION': 8,
    'BIRTHREGISTRATION': 9
}

SelectionCriterias = {
    'MSISDN': 1,
    'IMEI': 2,
    'IMSI': 3,
    'NID': 4,
    'PASSPORT': 5,
    'DRIVING_LICENSE': 6,
    'VEHICLE_REGISTRATION': 7,
    'BIRTH_REGISTRATION': 8,
    'mobileNumber': 1,
    'licenseNumber': 6,
    'nidNumber': 4,
    'NationalID': 4,
    'PassportNo': 5

}


def getDrivingLicenseSearchCriteria():
    return{
        "licenseNumber": "license_number",
        "mobileNumber": "mobile_no",
        "nidNumber": "nid"
    }


def getPassportSearchCriteria():
    return {
        "NationalID": 'national_id',
        "PassportNo": 'passport_number'
    }


def getCommonResponseBody():
    return {
        "data": {},
        "error": None,
        "type": "NID"
    }


def getSearchedWith(body,type):
    if type in ["CDR","ESAF","SMS","UNIFIED_VIEW"]:
        return body['searchValue']
    elif type in ["PASSPORT","DRIVINGLICENSE"]:
        return body['parameterValue']
    elif type == "BIRTHREGISTRATION":
        return body['birthRegNo']
    elif type == "VEHICLEREGISTRATION":
        return f"{body['zone']}-{body['series']}-{body['vehicleNumber']}"
    elif type == "NID":
        return body['nidNumber']

esCDRSearchCriteriaDict = {"MSISDN": "party_a",
                           "IMEI": "imei_number",
                           "IMSI": "imsi"}
cdrEsSourceColumn = {
    'MSISDN' : '_source.party_a',
    'IMEI' : '_source.imei_number'
}


timePeriods = {
    1: timePeriods.TimePeriods.LATE_NIGHT.name,
    2: timePeriods.TimePeriods.EARLY_MORNING.name,
    3: timePeriods.TimePeriods.MORNING.name,
    4: timePeriods.TimePeriods.NOON.name,
    5: timePeriods.TimePeriods.EVENING.name,
    6: timePeriods.TimePeriods.NIGHT.name
}

timePeriodsIncc = {
    'LATE_NIGHT' : 'lateNight',
    'EARLY_MORNING' : 'earlyMorning',
    'MORNING' : 'morning',
    'NOON' : 'noon',
    'EVENING' : 'evening',
    'NIGHT' : 'night'
}



TaskTypes = ['CDR', 'SMS', 'ESAF', 'NID', 'LRL', 'PASSPORT', 'BIRTHREGISTRATION', 'VEHICLEREGISTRATION', 'DRIVINGLICENSE']


searchCriteriaByID = {
    "1" : 'MSISDN',
    "2" : 'IMEI',
    "3" : 'IMSI',
    "4" : 'NID No',
    "5" : 'PASSPORT',
    "6" : 'DRIVING LICENSE',
    "7" : 'VEHICLE REGISTRATION No',
    "8" : 'BIRTH REGISTRATION No'
}
    

ColumnNameforSearchedValue = {
    'CDR' : ['msisdn'],
    'ESAF' : ['msisdn'],
    'SMS' : ['msisdn'],
    'LRL' : ['msisdn'],
    'NID' : ['nidNumber'],
    'PASSPORT' : ['parameterValue'],
    'DRIVINGLICENSE' : ['searchedWith'],
    'VEHICLEREGISTRATION' : ['zone', 'series', 'vehicleNumber' ],
    'BIRTHREGISTRATION' : ['birthRegNo']
}

