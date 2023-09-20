from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection

import domitory_api.models
from .models import user, Dormitory


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        userObj = user.objects.all().filter(username=username).first()
        print(userObj)
        if userObj:
            request.session["username"] = username
            print(username + "登录成功")
            return HttpResponse("登录成功")

    elif request.method == "GET":
        return render(request, "login.html")


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        repass = request.POST.get("repass")
        if password == repass:
            if not user.objects.filter(username=username):
                user.objects.create(username=username, password=password, userType=0)
                return HttpResponse("注册成功")
            else:
                return HttpResponse("用户名重复")
        else:
            return HttpResponse("输入有误")
    else:
        return render(request, "register.html")


def dash(request):
    username = request.session.get("username")
    return render(request, "dash.html", {"username": username})


def search(request):
    username = request.session.get("username")
    if request.method == "POST":
        try:
            stuName = request.POST.get("stuName")
        except:
            return HttpResponse("error")
        if stuName:
            print(stuName)
            with connection.cursor() as cursor:
                cursor.execute('''
                           SELECT d.id, d.building, d.room, d.score, b.bedNumber, b.bedUsername, b.bedUserTel, b.bedUserNo
                           FROM domitory_api_dormitory d
                           LEFT JOIN domitory_api_bedinfo b ON d.id = b.dormitory_id
                           WHERE b.bedUsername LIKE %s
                       ''', ["%" + stuName + "%"]),
                results = cursor.fetchall()
                return render(request, "search.html", {"results": results, "username": username, "keyword": stuName})
        try:
            tar_building = request.POST.get("building")
            tar_room = request.POST.get("room")
        except:
            return HttpResponse("error")
        print(tar_building + tar_room)
        with connection.cursor() as cursor:
            cursor.execute('''
                       SELECT d.id, d.building, d.room, d.score, b.bedNumber, b.bedUsername, b.bedUserTel, b.bedUserNo
                       FROM domitory_api_dormitory d
                       LEFT JOIN domitory_api_bedinfo b ON d.id = b.dormitory_id
                       WHERE d.building = %s AND d.room=%s
                   ''', [tar_building, tar_room]),
            results = cursor.fetchall()
        if results:
            return render(request, "search.html", {"results": results, "keyword": tar_building + "-" + tar_room})
        else:
            return HttpResponse("查询失败")
    elif request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT d.id, d.building, d.room, d.score, b.bedNumber, b.bedUsername, b.bedUserTel, b.bedUserNo
                FROM domitory_api_dormitory d
                LEFT JOIN domitory_api_bedinfo b ON d.id = b.dormitory_id
            ''')
            results = cursor.fetchall()
        return render(request, 'search.html', {'results': results})


def suguan(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")
    if request.method == "GET":
        rooms = Dormitory.objects.all()
        return render(request, "suguan.html", {"rooms": rooms, "username": username})
    elif request.method == "POST":
        try:
            score = request.POST.get("score")
            roomId = request.POST.get("roomId")
        except:
            return HttpResponse("输入有误")
        roomTitle = Dormitory.objects.filter(id=roomId)
        print(username + "将" + roomTitle + "修改为：" + score + "分")
        Dormitory.objects.filter(id=roomId).update(score=score)
        content = {
            "success": True,
        }
        return JsonResponse(content)
