from wsgiref.simple_server import make_server

# APPLICATIONS 
def hello_world(environment, start_response):
    status = '200 - OK'
    hearders = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, hearders)
    print("Requested /hello")
    return [b'Hello, World!']

def bye_world(environment, start_response):
    status = '200 - OK'
    hearders = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, hearders)
    print("Requested /bye")
    return [b'Goodbye, World!']

# MIDDLEWARES
def reverser(handler):
    def inner(environment, start_response):
        response = handler(environment, start_response)
        new_response = [x[::-1] for x in response]
        return new_response
    return inner

# ROUTE CONTROLLER
def route_controller(environment, start_response):
    status = '200 - OK'
    hearders = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, hearders)

    if environment['PATH_INFO'] == '/hello':
        return [b'Hello, World!']
    
    elif environment['PATH_INFO'] == '/bye':
        return [b'Goodbye, World!']

    elif environment['PATH_INFO'] == '/':
        return [b"This is the first page."]

    else:
        start_response('404 - Not Found', hearders)
        return [b"Not Found."]

if __name__ == '__main__':
    server = make_server('', 8000, route_controller)
    print("Serving on port 8000...")
    server.serve_forever()

