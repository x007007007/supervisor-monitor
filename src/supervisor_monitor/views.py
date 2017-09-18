from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Supervisor
from .models import SupervisorService
from django.views.decorators.csrf import csrf_exempt
from .monitor import Monitor
# Create your views here.


def index(request):
    return render(request, "supervisor_monitor/index.html")


@csrf_exempt
def supervisor_view(request):
    if request.method == "POST":
        urls = request.POST.getlist("url", [])
        usernames = request.POST.getlist("username", [])
        passwords = request.POST.getlist("password", [])
        res = []
        for url, username, password in zip(urls, usernames, passwords):
            username = username or None
            password = password or None
            try:
                monitor = Monitor(url, username, password)
                identification = monitor.getIdentification()
                rc = Supervisor(url=url, identification=identification, password=password, username=username)
                rc.save()
                res.append({"url": url, "identification": identification})
            except:
                res.append({"status": "error"})

        return JsonResponse({
            "count": len(res),
            "data": res
        })
    if request.method == "GET":
        res = []
        for supervisor in Supervisor.objects.all():  # type: Supervisor
            sd = {
                "identification": supervisor.identification,
                "pid": -1,
                "url": supervisor.url
            }
            try:
                sd['pid'] = supervisor.monitor().getPid()
                sd['state'] = supervisor.monitor().getStatus()
            except:
                import traceback
                traceback.print_exc()
                sd['state'] = -2
            res.append(sd)
        return JsonResponse({
            "data": res
        })

@csrf_exempt
def supervisor_reload_view(request, supervisor_id):
    if request.method == "POST":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        return JsonResponse({
            "result": supervisor.reload()
        })

@csrf_exempt
def supervisor_restart_view(request, supervisor_id):
    if request.method == "POST":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        return JsonResponse({
            "result": supervisor.restart()
        })

@csrf_exempt
def supervisor_service_view(request, supervisor_id):
    if request.method == "GET":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        services = supervisor.getServiceList()
        return JsonResponse({
            'count': len(services),
            'data': services
        })
    elif request.method == "POST":
        print(request.POST)


@csrf_exempt
def supervisor_service_console_view(request, supervisor_id, service_name):
    if request.method == "GET":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        offset = request.GET.get('offset')
        length = request.GET.get('length', "1024")
        try:
            offset = int(offset)
        except:
            offset = None
        try:
            length = int(length)
        except:
            length = 1024
        if offset is None:
            logstr, offset, overflow = supervisor.monitor().getRpcServer().supervisor.tailProcessStdoutLog(service_name, 0, length)
        else:
            logstr = supervisor.monitor().getRpcServer().supervisor.readProcessStdoutLog(service_name, offset, length)
        print(logstr)
        return JsonResponse({
            "offset": offset,
            "length": len(logstr),
            "log": logstr
        })


@csrf_exempt
def supervisor_service_stderr_view(request, supervisor_id, service_name):
    if request.method == "GET":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        offset = request.GET.get('offset')
        length = request.GET.get('length', "1024")
        try:
            offset = int(offset)
        except:
            offset = None
        try:
            length = int(length)
        except:
            length = 1024
        if offset is None:
            logstr, offset, overflow = supervisor.monitor().getRpcServer().supervisor.tailProcessStderrLog(service_name, 0, length)
        else:
            logstr = supervisor.monitor().getRpcServer().supervisor.readProcessStderrLog(service_name, offset, length)
        print(logstr)
        return JsonResponse({
            "offset": offset,
            "length": len(logstr),
            "log": logstr
        })


@csrf_exempt
def supervisor_service_stop_view(request, supervisor_id, service_name):
    if request.method == "POST":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        supervisor.monitor().stop(service_name)
    return JsonResponse({
        "msg": "not allow",
    }, status=405)

@csrf_exempt
def supervisor_service_start_view(request, supervisor_id, service_name):
    if request.method == "POST":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        supervisor.monitor().start(service_name)
        return JsonResponse({
            "status": 1
        })
    return JsonResponse({
        "msg": "not allow",
    }, status=405)

@csrf_exempt
def supervisor_service_restart_view(request, supervisor_id, service_name):
    if request.method == "POST":
        supervisor = Supervisor.objects.get(identification=supervisor_id)
        supervisor.monitor().restart(service_name)
        return JsonResponse({
            "status": 1
        })
    return JsonResponse({
        "msg": "not allow",
    }, status=405)