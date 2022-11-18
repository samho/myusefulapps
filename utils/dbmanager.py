from django.forms.models import model_to_dict
# from users.models import User
from django.contrib.auth.models import User
from commontype.models import CommonType


# Methods for User model

def get_all_users_queryset():
    ''' return all users queryset '''
    return User.objects.all()


def get_user_by_id(id):
    ''' return User object '''
    return User.objects.get(pk=id)


def get_user_by_name(username):
    ''' return User object '''
    return User.objects.filter(username=username)


def create_user(user):
    ''' create new user, return True/False '''
    try:
        user.save()
    except Exception as e:
        return False
    return True


def update_user(user):
    ''' update user, return True/False '''
    u = get_user_by_id(user.id)
    if u is None:
        return False
    else:
        try:
            user.save()
        except Exception as e:
            return False
        return True


def delete_user(user):
    ''' delete user, return True/False '''
    u = get_user_by_id(user.id)
    if u is None:
        return False
    try:
        user.delete()
    except Exception as e:
        return False
    return True


def delete_user_by_id(id):
    ''' delete user, return True/False '''
    u = get_user_by_id(id)
    if u is None:
        return False
    try:
        u.delete()
    except Exception as e:
        return False
    return True


# Methods for Commontype model


def get_all_commontype_queryset():
    ''' return all commontype queryset '''
    return CommonType.objects.all()
