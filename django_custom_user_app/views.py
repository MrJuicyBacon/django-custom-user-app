import json
from uuid import uuid4
from datetime import date, timedelta
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Session as DbSession


def create_response(input_object, status_code=200, content_type="application/json"):
    return HttpResponse(json.dumps(input_object), content_type=content_type, status=status_code)


@csrf_exempt
@require_POST
def auth(request):
    # Check if already have valid auth_token
    if request.custom_user is not None:
        return create_response({'error': 'You already have valid auth_token.'}, 400)
    # Check if all fields are present
    if not ('email' in request.POST and 'password' in request.POST):
        return create_response({'error': '"email" and "password" fields are required.'}, 400)

    # Get user object and check if user exists
    user = DbSession.query(User).filter(User.email == request.POST['email']).first()
    if user is None:
        return create_response({'error': 'No user found with provided email.'}, 400)

    # Check password
    if check_password(request.POST['password'], user.password) is not True:
        return create_response({'error': 'Wrong password.'}, 400)

    # All checks passed, creating token and response
    token = str(uuid4())
    expire_in_days = getattr(settings, 'AUTH_TOKEN_EXPIRE_IN_DAYS', 30)
    expire_date = date.today() + timedelta(days=expire_in_days)
    token_object = Token(token=token, user=user, expire=expire_date)
    DbSession.add(token_object)
    DbSession.commit()
    response_data = {
        'user': user.as_dict(),
        'auth_token': token,
    }

    return create_response(response_data)


@require_GET
def profile(request, user_id):
    # Get current user
    if user_id == 'me':
        if request.custom_user is None:
            return create_response({'error': 'You are not logged in or auth_token is not valid.'}, 403)
        user = request.custom_user
    # Get user by user id
    else:
        try:
            user_id = int(user_id)
        except ValueError:
            return create_response({'error': 'Unable to parse given user id.'}, 400)
        user = DbSession.query(User).get(user_id)

    if user is not None:
        return create_response({'user': user.as_dict()})
    return create_response({'error': 'Unable to find user with given user id.'}, 400)
