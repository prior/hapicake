from utils.exception import WrappedError

class Error(WrappedError):
    def __init__(self, info=None, err=None):
        super(Error, self).__init__(info, err)
    
class RequestError(Error):
    def __init__(self, request, info=None, err=None):
        super(RequestError, self).__init__(info, err)
        self.request = request

    def __str__(self):
        return "%s\n%s" % (super(RequestError, self).__str__(), self.request.url)

class TimeoutError(RequestError): 
    def __str__(self):
        return "Exceeded %ss timeout! %s" % (self.request.timeout or '?', super(TimeoutError, self).__str__())

class ResponseError(RequestError):
    def __init__(self, response, info=None, err=None):
        super(ResponseError, self).__init__(response.request, info, err)
        self.response = response

    def __str__(self):
        return "%s %s" % (super(ResponseError, self).__str__(), str(self.response.status_code))

class ParseError(ResponseError):
    def __init__(self, response, info=None, err=None):
        super(ParseError, self).__init__(response, info, err)

    def __str__(self):
        return "%s\n%s" % (super(ParseError, self).__str__(), self.response.content)


