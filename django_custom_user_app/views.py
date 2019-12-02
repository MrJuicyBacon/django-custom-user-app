import json
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import User, Session as DbSession


@csrf_exempt
@require_POST
def auth(request):
    if not ('email' in request.POST and 'password' in request.POST):
        return HttpResponse('NO FIELDS')
    user = DbSession.query(User).filter(User.email == request.POST['email']).first()
    if user is None:
        return HttpResponse('NO USER')
    if check_password(request.POST['password'], user.password) is not True:
        return HttpResponse('WRONG PASS')

    response_data = {
        'user': user.as_dict(),
        'auth_token': None,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
