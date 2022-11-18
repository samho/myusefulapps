from django.shortcuts import render
from utils import dbmanager
from django.core.paginator import Paginator
from myusefulapps.settings import DEFAULT_PAGE_SIZE
from commontype.form import CommonTypeForm
# Create your views here.


def listall(request, page_id):
    if not request.user.is_authenticated:
        return render(request, 'users/sign-in.html')
    logon_user = request.session['logon_user']
    all_type_list = dbmanager.get_all_commontype_queryset()
    page_type_list = Paginator(list(all_type_list), DEFAULT_PAGE_SIZE)
    cur_type_page = page_type_list.page(page_id)
    return render(request, "commontype/list_commontype.html", {"logon_user": logon_user, "type_page": cur_type_page})


def commontype_add(request):
    if not request.user.is_authenticated:
        return render(request, 'users/sign-in.html')
    logon_user = request.session['logon_user']

    if request.method == "GET":
        type_form = CommonTypeForm()
        return render(request, "commontype/add_commontype.html", {"logon_user": logon_user, "type_form": type_form})
