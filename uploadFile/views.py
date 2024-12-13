# Create your views here.
import json
from django.http import HttpResponse
import pandas as pd
from uploadFile.models import NBA


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_content = pd.read_csv(file)
        NaN = 0
        Nan_data = []
        Nan_key = []
        Nan_data_str = '['
        for row in file_content.iterrows():
            if row[1].isnull().sum() == 0:
                player = NBA(full_name=row[1]['full_name'], rating=row[1]['rating'], jersey=row[1]['jersey'],
                             team=row[1]['team'],
                             position=row[1]['position'], b_day=row[1]['b_day'], height=row[1]['height'],
                             weight=row[1]['weight'], salary=row[1]['salary'], country=row[1]['country'],
                             draft_year=row[1]['draft_year'], draft_round=row[1]['draft_round'],
                             draft_peak=row[1]['draft_peak'], college=row[1]['college'], version=row[1]['version'])
                player.save()
            else:
                Nan_data.append(row[1].to_json())
                NaN += 1
                key = row[1][row[1].isnull()].index.tolist()[0]
                if key not in Nan_key:
                    Nan_key.append(key)
        rows = file_content.shape[0]
        Nan_data = ','.join(Nan_data)
        Nan_data_str += Nan_data
        Nan_data_str += ']'
        data = {
            'data': json.loads(Nan_data_str),
            'rows': rows - NaN,
            'Nan': Nan_key
        }
        return HttpResponse(json.dumps(data), content_type='application/json')


def upload_message(request):
    if request.method == 'POST':
        row = json.loads(request.body.decode('utf-8'))
        if pd.DataFrame([row]).isnull().all().sum() == 0:
            player = NBA(full_name=row['full_name'], rating=row['rating'], jersey=row['jersey'], team=row['team'],
                         position=row['position'], b_day=row['b_day'], height=row['height'],
                         weight=row['weight'], salary=row['salary'], country=row['country'],
                         draft_year=row['draft_year'], draft_round=row['draft_round'],
                         draft_peak=row['draft_peak'], college=row['college'], version=row['version'])
            player.save()
            return HttpResponse(json.dumps({'result': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': 'false'}), content_type='application/json')

def upload_messages(request):
    if request.method == 'POST':
        rows = json.loads(request.body.decode('utf-8'))
        for row in rows:
            if pd.DataFrame([row]).isnull().all().sum() == 0:
                player = NBA(full_name=row['full_name'], rating=row['rating'], jersey=row['jersey'], team=row['team'],
                             position=row['position'], b_day=row['b_day'], height=row['height'],
                             weight=row['weight'], salary=row['salary'], country=row['country'],
                             draft_year=row['draft_year'], draft_round=row['draft_round'],
                             draft_peak=row['draft_peak'], college=row['college'], version=row['version'])
                player.save()
                rows = [r for r in rows if r != row]
        return HttpResponse(json.dumps(rows), content_type='application/json')