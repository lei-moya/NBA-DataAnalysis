import json
from uploadFile.models import NBA
from django.http import HttpResponse


# Create your views here.
def table_check(request):
    if request.method == 'POST':
        columns = json.loads(request.body.decode('utf-8'))
        if not columns:
            data = list(NBA.objects.values())
        else:
            data = list(NBA.objects.values(*columns))
        return HttpResponse(json.dumps(data), content_type='application/json')


def table_update(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))[0]
        if data['id']:
            NBA.objects.filter(id=data['id']).update(**data)
        else:
            newRow = NBA(**data)
            newRow.save()
    return HttpResponse(json.dumps({"result": "success"}), content_type='application/json')


def table_del(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        NBA.objects.filter(id=data).delete()
    return HttpResponse(json.dumps({"result": "success"}), content_type='application/json')
