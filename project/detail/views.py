from django.shortcuts import render
from app.models import House, Facility


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