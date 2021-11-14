def getAgencyId(agencyId):
    if agencyId:
        agencyId = agencyId.strip('/').split('/')[0]
    return agencyId
