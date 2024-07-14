from django.core.mail import BadHeaderError, send_mail
from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK):
        response_data = {"message": message}
        response_data["status_code"] = status_code
        response_data["success"] = True
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status_code)

    @staticmethod
    def error(message, data=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {"message": message}
        response_data["data"] = {}
        response_data["success"] = False
        response_data["status_code"] = status_code
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status_code)


def send_email(subject, message, to_email, from_email="hiankitkr@gmail.com"):
    subject = subject
    message = message
    from_email = from_email
    if subject and message and to_email:
        try:
            send_mail(subject, message, from_email, to_email)
            return True
        except BadHeaderError:
            return False
        except Exception as e:
            print(f"failed to send email to {to_email} /n Error: {str(e)}")
            return False
    else:
        return False
