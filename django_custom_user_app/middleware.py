from .models import User, Token, Session as DbSession


class AuthMiddleware:
    """
    Middleware for extracting auth token from the request
    and assigning user object to the "custom_user" parameter of the request
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get "auth_token" either from POST or GET request
        if request.method == 'POST':
            auth_token = request.POST.get('auth_token')
        else:
            auth_token = request.GET.get('auth_token')

        # Assign user if exists
        user = None
        if auth_token is not None:
            token_object = DbSession.query(Token).join(User).filter(Token.token == auth_token).first()
            try:
                user = token_object.user
            except AttributeError:
                pass
        request.custom_user = user

        response = self.get_response(request)
        return response
