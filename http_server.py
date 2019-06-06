import socket
import sys
import traceback
import os


def response_ok(body=b"Default response (no body provided)", mimetype=b"text/plain"):
    print('[server] inside response_ok()') # DKA
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body,
    ])


def response_method_not_allowed():
    print('[server] inside response_method_not_allowed()') # DKA
    """Returns a 405 Method Not Allowed response"""

    return b"\r\n".join([
        b"HTTP/1.1 405 NOT ALLOWED",
        b"Content-Type: text/plain",
        b"",
        b"Not Allowed!",
    ])


def response_not_found():
    print('[server] inside response_not_found()') # DKA
    """Returns a 404 Not Found response"""

    return b"\r\n".join([
        b"HTTP/1.1 404 NOT FOUND",
        b"Content-Type: text/plain",
        b"",
        b"Not Found!",
    ])


def parse_request(request):
    print('[server] inside parse_request()') # DKA
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    method, path, version = request.split("\r\n")[0].split(" ")
    
    if method != "GET":
        raise NotImplementedError

    return path


def response_path(path):
    print('[server] inside response_path() path: {}'.format(path)) # DKA
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.

    with open(path, 'rb') as f:  # DKA etc...
        print('[server] inside response_path() open path: {}'.format(path)) # DKA
        content = f.read()
#        mime_type = b"not implemented" DKA

    return content


def server(log_buffer=sys.stderr):
    print('[server] inside server()') # DKA
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break
		

                print("Request received:\n{}\n\n".format(request))

                try:
                    path = parse_request(request)
                    print('[server] this path: "{}"'.format(path)) # DKA
                    local_path = os.path.join('webroot', *path.split('/'))
                    print('[server] local_path: "{}"'.format(local_path)) # DKA
                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path.

                    # TODO; If parse_request raised a NotImplementedError, then let
                    # response be a method_not_allowed response. If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    # use the content and mimetype from response_path to build a 
                    # response_ok.

                    response = response_ok(
#                        body='b"' + path + '"', DKA
#                        body=b"/sample.txt", # DKA
                        body = response_path(local_path)
#                        mimetype = b"text/plain" DKA
                    )
                except NotImplementedError:
                    response = response_method_not_allowed()

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    print('[server] inside __main__') # DKA
    server()
    sys.exit(0)
