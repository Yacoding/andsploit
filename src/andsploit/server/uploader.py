#coding=utf-8
from base64 import b64encode
from socket import socket
import ssl

from andsploit.server.receivers.http import HTTPRequest, HTTPResponse
from andsploit.ssl.provider import Provider

def delete(arguments, resource):
    sock = get_socket(arguments)
    
    request = HTTPRequest(verb="DELETE", resource=resource)
    
    request.writeTo(sock)
    response = HTTPResponse.readFrom(sock)
    
    return response.code == 200

def get_socket(arguments):
    sock = socket()
    
    if arguments.ssl:
        provider = Provider()
        
        sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs=provider.ca_certificate_path())

    sock.settimeout(5.0)
    if hasattr(arguments, 'push_server') and arguments.push_server != None:
        sock.connect(arguments.push_server)
    else:
        sock.connect(arguments.server)
    
    return sock
    
def upload(arguments, resource, data, magic=None, mimetype=None, headers=None):
    sock = get_socket(arguments)
    
    request = HTTPRequest(verb="POST", resource=resource, headers=headers, body=data)
    if arguments.credentials != None:
        request.headers["Authorization"] = "Basic %s" % b64encode(":".join(arguments.credentials))
    request.headers["Content-Length"] = len(data)
    if mimetype != None:
        request.headers["Content-Type"] = mimetype
    if magic != None:
        request.headers["X-andsploit-Magic"] = magic
        
    request.writeTo(sock)
    response = HTTPResponse.readFrom(sock)

    return response.status == 201
#201(已创建)请求成功并且服务器创建了新的资源。