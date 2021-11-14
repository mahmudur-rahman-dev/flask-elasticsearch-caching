def getMobileNoWithDoubleEightAsPrefix(msisdn):
    if not msisdn.startswith('88'):
        if msisdn.startswith('0'):
            return '88'+msisdn
        return '880'+msisdn
    return msisdn
