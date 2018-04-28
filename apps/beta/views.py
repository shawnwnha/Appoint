from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import User, Profile, Appointment, Schedule, Message
#####################################################################################################
def index(request):
	return render(request, 'beta/loginpage.html')

def registerpage(request):
	return render(request, 'beta/registerpage.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, message in errors.iteritems():
            messages.error(request, message, tag)
        return redirect('/register')
    else:
        user= User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
            admin = 0
        )
        request.session['id']=user.id
        request.session['firstname']=user.first_name
        return redirect("/userpage")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, message in errors.iteritems():
            messages.error(request, message, tag)
        return redirect('/')
    else:
        this_user = User.objects.get(email = request.POST['login_id'])
        # Save session ID on successful login, so that we can retrieve when needed # -shawn
        if this_user.admin == 0:
            request.session['id']=this_user.id
            request.session['first_name']=this_user.first_name
            return redirect('/userpage')  
        else:
            request.session['id']=this_user.id
            request.session['first_name']=this_user.first_name
            return redirect('/homepage')

def homepage(request):
    schedules=Schedule.objects.all()
    confirmedappos=Appointment.objects.filter(rejected=2).order_by('-start')
    unconfirmedappos=Appointment.objects.filter(rejected=0).order_by('-start')
    print confirmedappos
    context={
        'schedules':schedules,
        'confirmedappos':confirmedappos,
        'unconfirmedappos':unconfirmedappos,
    }
    return render(request,"beta/homepage.html",context)

def userpage(request):
    schedules = Schedule.objects.all().order_by('start')
    user = User.objects.get(id = request.session['id'])
    appointments = Appointment.objects.filter(user_id = user.id).order_by('start')
    count = appointments.count()
    doctor = User.objects.filter(admin = 1).first()
    context = {
        'user': user,
        'schedules': schedules,
        'appointments': appointments,
        'count': count,
        'doctor': doctor 
    }
    return render(request,"beta/userpage.html", context)


def accept(request,passid):
    currentappo=Appointment.objects.get(id=passid)
    currentappo.rejected=2
    currentappo.save()
    return redirect("/homepage")

def reject(request,passid):
    return render(request,"beta/rejectpopup.html",{'passid':passid})
    
def addreject(request,passid):
    currentappo=Appointment.objects.get(id=passid)
    currentappo.subject=request.POST['reason']
    currentappo.rejected=1
    currentappo.save()
    return redirect("/homepage")
    

def addschedule(request):
    return render(request,'beta/addschedule.html')

def addschedules(request):
    start=request.POST['start']
    end=request.POST['end']
    if start>end:
        error="End_time is greater than start_time"
        return render(request,'beta/addschedule.html',{'error':error})
    else:
        Schedule.objects.create(start=start,end=end,user_id=request.session['id'])
        schedules=Schedule.objects.all().order_by('start')
        return redirect('/homepage',{'schedules':schedules})

def appointmentpage(request,id):
    schedule = Schedule.objects.get(id=id)
    context = {
       'schedule': schedule
    }
    return render(request,'beta/appointmentpage.html', context)

def appoint(request,id):
    schedule = Schedule.objects.get(id=id)
    user = User.objects.get(id = request.session['id'])
    subject = request.POST['subject']
    Appointment.objects.create(subject = subject, start = schedule.start, end = schedule.end, user = user, rejected = 0)
    schedule.delete()
    return redirect('/userpage')

def cancel(request,id):
    appointment = Appointment.objects.get(id=id)
    user = User.objects.get(admin = 1)
    Schedule.objects.create(start = appointment.start, end = appointment.end, user = user)
    appointment.delete()
    return redirect('/userpage')    

def logout(request):
    del request.session['id']
    return redirect("/")