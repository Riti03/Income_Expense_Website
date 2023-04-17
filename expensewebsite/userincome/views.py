from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator 
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django_zoom_meetings import ZoomMeetings
from datetime import datetime
# from .userpreferences.models import UserPreference
# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user).order_by('id')
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income, 
        'page_obj': page_obj,
        # 'currency': currency
    }
    return render(request, 'income/index.html',context)


@login_required(login_url='/authentication/login') 
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source,description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income')





@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)

        # income.owner = request.user
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated successfully')

        return redirect('income')


@login_required
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record removed')
    return redirect('income')   



#blog part starts here

@login_required
def blog_page(request):
    allBlogs = blog.objects.all().order_by('-publishedat')
    return render(request, 'income/blog.html',{'allBlogs':allBlogs})

@login_required
def consulting_page(request):
    all_cons=Consulting.objects.all()
    booked = Booking.objects.filter(client=request.user).values('consulting')
    bl=list(booked)
    bliids=[ele['consulting'] for ele in bl]
    bookdet=[]
    for i in bliids:
        bookdet.append(Consulting.objects.get(id=i))
    free_cons_li=[]
    paid_cons_li=[]
    for fr in all_cons:
        if not fr.id in bliids:
            if fr.price.lower()=='free':
                free_cons_li.append(Consulting.objects.get(id=fr.id))
            else:
                paid_cons_li.append(Consulting.objects.get(id=fr.id))
    context={
        'free_cons':free_cons_li,
        'paid_cons':paid_cons_li,
        'bookdet':bookdet,
    }
    return render(request,'income/consilting.html',context)

@csrf_exempt
@login_required
def booking_page(request):
    if request.method == 'POST':
        dataidnum = request.POST.get('dataidnum')
        consiltingid = Consulting.objects.get(id=dataidnum) 
        datapricenum = request.POST.get('dataprice')
        orderid= request.POST.get('orderid')
        owner=request.user
        # dataprice = request.POST.get('dataprice')
        # dataprice = int(dataprice)
        # print(dataprice)
        # if dataprice == 0:
        # Consulting.objects.filter(id=dataidnum).update(booked=True)
        # return render(request,'income/consilting.html')
        Booking.objects.create(client=owner,consulting=consiltingid,fee=datapricenum,razor_pay_order_id=orderid)
        return redirect('consulting_page')



@login_required
def checkout(request,id):
    get_details = Consulting.objects.filter(id=id)
    get_pr = Consulting.objects.filter(id=id).values('price')

    priceamo = int(list(get_pr)[0]['price'])
    
    client = razorpay.Client(auth = (settings.KEY , settings.SECRET))
    payment = client.order.create({'amount': priceamo * 100,'currency':'INR','payment_capture': 1})
    print("******")
    print(payment)
    print("*******")
    pay_id = payment['id']
    # Consulting.objects.filter(id=id).update(razor_pay_order_id=pay_id)

    context = {
        'checkout_payment':get_details,
        'payment':payment,
    }
    return render(request,'income/checkoutpage.html',context)




#meeting list


def meetinglist(request):
    if request.user.is_superuser:
        all_meetings = Consulting.objects.all()
        context={
            'allmettings':all_meetings,
        }
        return render(request,'income/meetinglist.html',context)
    


zoom_api_key = settings.ZOOM_API_KEY
zoom_api_secret = settings.ZOOM_API_SECRET
zoom_email = settings.ZOOM_EMAIL_ID

def createmeetingin(request):
    if request.method == 'POST':
        idmet = request.POST['id']
        topic = request.POST['topic']
        scheduledtime = request.POST['scheduledtime']
        duration = request.POST['duration']
        password = request.POST['password']

        scheduledtime = scheduledtime+":00Z"
        # print(scheduledtime)
        # 2021-05-10T12:10:10Z
        scheduledtime=datetime.strptime(scheduledtime, '%Y-%m-%dT%H:%M:%SZ')
    

        my_zoom = ZoomMeetings(zoom_api_key,zoom_api_secret,zoom_email)

        create_meeting = my_zoom.CreateMeeting(scheduledtime,topic,duration,password)

        
        print(create_meeting['id'],create_meeting['start_url'],create_meeting['join_url'])
        # print(create_meeting)

        Consulting.objects.filter(id=idmet).update(scheduledat=scheduledtime,meduration=duration,zoomlink=create_meeting['join_url'],meetingid=create_meeting['id'])

        return redirect('meetinglist')
    

def cancelmeetingin(request):
    if request.method == 'POST':
        iddel = request.POST['id']
        meetid = Consulting.objects.filter(id=iddel).values('meetingid')
        str_meeting_id=str(list(meetid)[0]['meetingid'])
        # print(str_meeting_id)

        my_zoom = ZoomMeetings(zoom_api_key,zoom_api_secret,zoom_email)

        delete_meeting = my_zoom.DeletMeeting(str_meeting_id)

        Consulting.objects.filter(id=iddel).delete()

        print(delete_meeting)

        return redirect('meetinglist')
    
def meetingdetails(request):    
    if request.method == 'GET':
        dataid = request.GET['dataidnum']
        meetingid = str(list(Consulting.objects.filter(id=dataid).values('meetingid'))[0]['meetingid'])
        # print(meetingid)
        my_zoom = ZoomMeetings(zoom_api_key,zoom_api_secret,zoom_email)
        get_meeting = my_zoom.GetMeeting(meetingid)
        # print(get_meeting)
        topic = get_meeting['topic']
        createdat = get_meeting['created_at']
        scheduledat = get_meeting['start_time']
        duration = get_meeting['duration']
        status = get_meeting['status']
        startlink = get_meeting['start_url']
        joinlink = get_meeting['join_url']
        password = get_meeting['password']

        data = {
            'meetingid': meetingid,
            'topic': topic,
            'createdat': createdat,
            'scheduledat': scheduledat,
            'duration': duration,
            'status': status,
            'startlink': startlink,
            'joinlink': joinlink,
            'password': password,

        }
        return JsonResponse(data)
        


    





