# app/api/forms.py
from fastapi import Form


class OAuth2EmailRequestForm:
    """
    Переопределяем стандартную форму OAuth2, чтобы использовать email вместо username.
    """

    def __init__(
            self,
            email: str = Form(...),  # Меняем username на email
            password: str = Form(...),
            scope: str = Form(""),
            client_id: str = Form(None),
            client_secret: str = Form(None),
    ):
        self.email = email
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
