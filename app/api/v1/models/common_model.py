
class CommonModels(object):
    """ 
    This class contains methods that are common to all other
    models
    """

    def makeresp(self, payload, status_code):
        """ Returns user details if found and message if not """

        if isinstance(payload, str):
            return {
                "status": status_code,
                "error": payload
            }
        if not isinstance(payload, list):
            return {
                "status": status_code,
                "data": [payload]
            }

        return {
            "status": status_code,
            "data": payload
        }
