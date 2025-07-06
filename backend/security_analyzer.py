import httpx
import ssl
import certifi
from urllib.parse import urlparse
from datetime import datetime
import socket
import requests


# async def fetch_security_headers(url):
#     required_headers = [
#         'Content-Security-Policy',
#         'X-Content-Type-Options',
#         'X-Frame-Options',
#         'Strict-Transport-Security',
#         'X-XSS-Protection'
#     ]

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)

#     headers_report = {}
#     for header in required_headers:
#         value = response.headers.get(header)
#         headers_report[header] = value if value else 'Missing'

#     return headers_report

def fetch_security_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers

        secure_headers = {
            "Content-Security-Policy": headers.get("Content-Security-Policy", "Missing"),
            "X-Content-Type-Options": headers.get("X-Content-Type-Options", "Missing"),
            "X-Frame-Options": headers.get("X-Frame-Options", "Missing"),
            "Strict-Transport-Security": headers.get("Strict-Transport-Security", "Missing"),
            "X-XSS-Protection": headers.get("X-XSS-Protection", "Missing"),
        }

        https_validity = "Not Checked"
        if url.startswith("https"):
            try:
                import ssl
                import socket
                from datetime import datetime

                hostname = url.split("//")[1].split("/")[0]
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        valid_from = cert['notBefore']
                        valid_to = cert['notAfter']
                        https_validity = {
                            "valid_from": valid_from,
                            "valid_to": valid_to
                        }
            except Exception as e:
                https_validity = {"error": str(e)}

        return {
            "https_certificate_validity": https_validity,
            "secure_headers_status": secure_headers
        }

    except Exception as e:
        return {
            "error": str(e)
        }



# def check_https_certificate(url):
#     parsed_url = urlparse(url)
#     hostname = parsed_url.hostname

#     context = ssl.create_default_context(cafile=certifi.where())

#     try:
#         with context.wrap_socket(
#             ssl.SSLSocket(), server_hostname=hostname
#         ) as s:
#             s.connect((hostname, 443))
#             cert = s.getpeercert()

#             # Parse valid_from and valid_to into readable dates
#             valid_from = cert.get('notBefore')
#             valid_to = cert.get('notAfter')

#             issuer = cert.get('issuer')
#             issuer_name = ", ".join(f"{x[0]}={x[1]}" for x in issuer[0]) if issuer else "Unknown"

#             return {
#                 "issuer": issuer_name,
#                 "valid_from": valid_from,
#                 "valid_to": valid_to,
#                 "expired": is_certificate_expired(valid_to)
#             }

#     except Exception as e:
#         return {"error": str(e)}

def check_https_certificate(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": cert.get('issuer'),
                    "valid_from": cert.get('notBefore'),
                    "valid_to": cert.get('notAfter'),
                }
    except Exception as e:
        return {"error": str(e)}


def is_certificate_expired(valid_to):
    try:
        expiry_date = datetime.strptime(valid_to, "%b %d %H:%M:%S %Y %Z")
        return datetime.utcnow() > expiry_date
    except:
        return "Unknown"
