from django.conf.urls import url
from . import views 

urlpatterns =[
	url(r'^$', views.index), # login page
    url(r'^login/0$', views.login), # POST _ Login
    url(r'^register$', views.registerpage),
	url(r'^register/0$', views.register),
    url(r'^homepage$', views.homepage),
    url(r'^homepage/addshedule$', views.addschedule),
    url(r'^homepage/addshedules$', views.addschedules),
    url(r'^homepage/accept/(\d+)$', views.accept),
    url(r'^homepage/reject/(\d+)$', views.reject),
    url(r'^homepage/addreject/(\d+)$', views.addreject),
    url(r'^userpage$', views.userpage),
    url(r'^appoint/(?P<id>\d+)$',views.appointmentpage),
    url(r'^appoint/confirm/(?P<id>\d+)$',views.appoint),
    url(r'^cancel/(?P<id>\d+)$',views.cancel),
    url(r'^logout$',views.logout),
]
	
    
    
	

