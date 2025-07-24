from mail_templated import send_mail


def send_email(
    path: str, user: object, token: str, sender: str, receiver: str
):
    send_mail(path, {'user': user, 'token': token}, sender, [receiver])
