from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from app.models import House, Facility, Collect, User
from django.core import exceptions


# Create your views here.

def detail(request, house_id):
    if request.method == 'GET':
        data = {}
        house = House.objects.filter(house_id=house_id)
        if house[0]:
            data['house'] = house[0]
            data['user'] = house[0].user
            data['house_type'] = house[0].type
            data['house_area'] = house[0].area
            data['house_detail'] = house[0].housedetail_set.first()
            data['house_img'] = house[0].houseimg_set.all()
            temp = [fac.facility_name for fac in house[0].facility_set.all()]
            data['fac'] = [(fac, bool(fac.facility_name in temp)) for fac in Facility.objects.all()]

        return render(request, 'detail.html', {'data': data})


def collect(request):
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        user_account = request.session.get('account')
        method = request.POST.get('method')
        house = House.objects.filter(house_id=house_id).first()
        if method == '1':
            if user_account:
                user = User.objects.filter(account=user_account).first()
                if Collect.objects.filter(user=user, house=house).exists():
                    return JsonResponse({'code': 1})
                else:
                    return JsonResponse({'code': 0})
            else:
                return JsonResponse({'code': 0})
        elif method == '2':
            if user_account:
                user = User.objects.filter(account=user_account).first()
                if Collect.objects.filter(user=user, house=house).exists():
                    return JsonResponse({'code': 0})
                else:
                    try:
                        Collect.objects.create(user=user, house=house)
                        return JsonResponse({'code': 1})
                    except exceptions:
                        return JsonResponse({'code':0})
            else:
                return JsonResponse({'code':5})
        elif method == '3':
            if user_account:
                user = User.objects.filter(account=user_account).first()
                if Collect.objects.filter(user=user, house=house).exists():
                    try:
                        Collect.objects.filter(user=user, house=house).delete()
                        return JsonResponse({'code': 1})
                    except exceptions:
                        return JsonResponse({'code': 0})
                else:
                    return JsonResponse({'code': 0})
            else:
                return JsonResponse({'code':5})