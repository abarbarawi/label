from django.shortcuts import render
from django.contrib.auth.models import auth
from django.http import HttpResponse, HttpResponseRedirect ,JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import reters,clips,data_sets,evaluations
from data_process.split import generate_csv,split_files
from django.db.models import Q
from django.contrib.auth import logout
from django.db import connection



def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('app:home'))
        else:
            print("They used username: {} and password: {}".format(username, password))
            messages.info(request, 'invalid credentials ')
            return HttpResponseRedirect(reverse('app:login'))
    else:
        return render(request, 'Login.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('app:login'))
#this function used to retrive data in the home page
def home(request):
    data_set=data_sets.objects.all()
    user = reters.objects.get(user=request.user)
    eval = evaluations.objects.filter(rater=user)
    audios=clips.objects.all()
    all_clips=len(audios)
    evaluated_clips = len(eval)
    context={
        'data_sets':data_set,
        'evaluated_clips':evaluated_clips,
        'all_clips':all_clips,
    }

    return render(request,'home.html',context)
#this function used to split data to clips it takes dataset and number of seconds
def split_data(request):
   data_set=data_sets.objects.all()

   context={
       'data_set':data_set,
   }
   if request.method=='POST':
       data_set_id=request.POST['data_set']
       sec=request.POST['duration']
       data=data_sets.objects.get(id=data_set_id)
       path=data.path
       name=data.name
       generate_csv(name,path)

       split_files(name=name,duration=sec)
       return render(request,'split_data.html',{'msg':'successful'})
   return render(request,'split_data.html',context)
#this function to get the data according to the dataset
def get_audio_clips(request):
    data_set=data_sets.objects.all()

    if request.method == 'GET':
        type = request.GET['type']
        if type == 'dataset':
            id = request.GET['id']
            dataset = data_sets.objects.get(id=id)
            audios = clips.objects.filter(data_set=dataset)
            user = reters.objects.get(user=request.user)
            evaluation = evaluations.objects.filter(rater=user)

            cursor = connection.cursor()
            cursor.execute('''select * from app_clips where id NOT in (select clip_id from app_evaluations where rater_id ='''+str (user.id)+''' )''')
            not_eval_audios = cursor.row = cursor.fetchall()
            print(not_eval_audios)
            datajs = list(not_eval_audios)
            alldata=datajs
            datajs = datajs[:1]




            return JsonResponse({'datajs':datajs,'alldata':alldata }, safe=False)

    else:
        context={
            'data_sets': data_set,
        }
        return render(request, 'home.html', context)

#this function used to label the clips
def evaluate(request):

    if request.method=='GET':
        audio_id=request.GET['audio_id']
        label=request.GET['label']
        ll=''
        if label=='block':
            ll=6
        elif label=='wordrepetition':
            ll = 2
        elif label=='partwordrepetition':
            ll = 7
        elif label=='phraserepetition':
            ll = 3
        elif label=='prolongation':
            ll = 5
        elif label=='soundrepetition':
            ll = 1
        elif label=='interjection':
            ll = 4
        elif label=='clearvoice':
            ll = 0
        print('label' , ll )
        user=reters.objects.get(user=request.user)
        clip=clips.objects.get(id=audio_id)
        evaluation=evaluations(clip=clip,label=ll,rater=user)
        evaluation.save()

        eval = evaluations.objects.filter(rater=user)
        evaluated_clips = len(eval)
        return JsonResponse({'success':1,'evaluated_clips':evaluated_clips},status=200)

#this function used to get the next audio clip
def next(request):
    data_set=data_sets.objects.all()
    if request.method == 'GET':
        type = request.GET['type']
        if type == 'next':
            id = request.GET['id']
            dataset = data_sets.objects.get(id=id)
            audios = clips.objects.filter(data_set=dataset)
            user = reters.objects.get(user=request.user)
            evaluation = evaluations.objects.filter(rater=user)

            cursor = connection.cursor()
            cursor.execute(
                '''select * from app_clips where id NOT in (select clip_id from app_evaluations where rater_id =''' + str(
                    user.id) + ''' )''')
            not_eval_audios = cursor.row = cursor.fetchall()
            print(not_eval_audios)
            datajs = list(not_eval_audios)
            alldata = datajs
            datajs = datajs[:1]

            return JsonResponse({'datajs': datajs, 'alldata': alldata}, safe=False)

    else:
        context={
            'data_sets': data_set,
        }
        return render(request, 'home.html', context)
