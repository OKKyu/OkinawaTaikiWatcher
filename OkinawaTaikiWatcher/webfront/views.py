from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.db import transaction
from .models import Criterias, Settings, Kyokus

# Create your views here.


def login_app(request):
    '''
      responsing login page.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect("topview")

    return render(request, "login.html")


def authentication(request):
    '''
      authenticating process.
    '''
    context = {}

    user = authenticate(username=request.POST['login_id'], password=request.POST['login_pw'])

    if user is not None:
        login(request, user)

        # Redirect to topview
        return HttpResponseRedirect("topview")
    else:
        temp = loader.get_template('common_message.html')
        msg = {}
        msg.setdefault('subject', 'ログインに失敗しました。')
        msg.setdefault('message1', '入力内容が正しいかもう一度確かめてログインし直して下さい。')
        msg.setdefault('message2', '※リンクを押すとトップ画面に戻ります')
        context['msg'] = msg

        return HttpResponseForbidden(temp.render(context, request))


@login_required(login_url='login', redirect_field_name='')
def topview(request):
    template = loader.get_template("topview.html")
    context = {}

    # set run_flg to context.
    run_flg = Settings.objects.all().first().boot_switch
    context.setdefault("run_flg", run_flg)

    # set criterias to context.
    criterias = {}
    for criteria in Criterias.objects.all():
        criterias.setdefault(criteria.substitute, criteria.criteria)
    context.setdefault("criterias", criterias)

    # set kyokus to context.
    kyokus = {}
    for kyoku in Kyokus.objects.all():
        kyokus.setdefault(kyoku.name, kyoku.alert_flg)
    context.setdefault("kyokus", kyokus)

    return HttpResponse(template.render(context, request))


@login_required(login_url='login', redirect_field_name='')
@permission_required('webfront.change_criterias')
@permission_required('webfront.change_kyokus')
@permission_required('webfront.change_settings')
def update_infos(request):
    try:
        with transaction.atomic():
            # Settings
            settings = Settings.objects.all().first()
            settings.boot_switch = request.POST.get("toggle_running", False)
            settings.save()

            # criterias
            for name in request.POST.keys():
                # exclude other inputs.
                if "toggle" in name or ("alterval_" not in name and "kyoku_alert_" not in name):
                    continue

                # validate.
                print(name)
                val = request.POST.get(name)
                if val is None or len(val) <= 0 or (val is str):
                    continue

                # alter value and save.
                if "alterval_" in name:
                    criteria = Criterias.objects.get(substitute=name.split("_")[1])
                    criteria.criteria = val
                    criteria.save()

                if "kyoku_alert_" in name:
                    print(val)
                    kyoku = Kyokus.objects.get(name=name.split("_")[2])
                    kyoku.alert_flg = val
                    kyoku.save()

            return HttpResponseRedirect("topview")
    except Exception as ex:
        print(ex)
        temp = loader.get_template('common_message.html')
        context = {}
        msg = {}
        msg.setdefault('subject', 'エラー発生')
        msg.setdefault('message1', '入力内容が正しいかもう一度確かめてログインし直して下さい。')
        msg.setdefault('message2', '※リンクを押すとトップ画面に戻ります')
        context['msg'] = msg

        return HttpResponse(temp.render(context, request))


def logout_app(request):
    logout(request)

    return render(request, "login.html")


def _topview_mock():
    '''
      Test data for topview.
    '''
    context = {
        "run_flg": True,
        "criterias": {
            "CO2": 0.01,
            "SOX": 0.02,
            "PM2.5": 4
        }
    }
    return context
