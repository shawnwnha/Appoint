from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
validate_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
########################################################################################################
class UserManager(models.Manager):
	def register_validator(self, postData): 
		errors = {}
		first_name = postData['first_name']
		last_name = postData['last_name']
		email = postData['email']
		password = postData['password']
		password_c = postData['password_c'] 
		if len(first_name) < 1 or len(last_name) < 1 or len(email) < 1 or len(password) <1 or len(password_c)<1:
			errors['length'] = "All inputs must be filled."
			return errors 
		else:
			if len(first_name) < 3 or len(last_name) < 3:
				errors['name_length'] = "Name must be more than 2 characters."
			if not first_name.isalpha() or not last_name.isalpha():
				errors['name_type'] = "Name be alphabets only"
			if len(password) < 8 or len(password_c) < 8:
				errors['password_length'] = "Password be more than 8 characters."
			if password != password_c:
				errors['password_match'] = "Password confirmation failed."
			if User.objects.filter(email = email):
				errors['email'] = "Email already exists."
			if not validate_email.match(email):
				errors['email_valid'] = "Email not valid."
			return errors		

	def login_validator(self, postData):
		errors ={}
		login_id = postData['login_id']
		login_pw = postData['login_pw']
		
		if len(login_id)<1 or len(login_pw)<1:
			errors['length'] = "All inputs must be filled."
			return errors
		else:
			user = User.objects.filter(email = login_id)
			if not user:
				errors['invalid_id'] = "Email does not exist."
			else:
				user = User.objects.get(email = login_id)
				data_pw = user.password 
				if not bcrypt.checkpw(str(login_pw).encode(), data_pw.encode()):
					errors['invalid_password'] = "Invalid Password."
			return errors

class User(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.IntegerField() # default 0, ADMIN = 1
    objects = UserManager()

class Profile(models.Model):
	content = models.CharField(max_length=255)
	user = models.OneToOneField(User, related_name ="profile") # ONE TO ONE (USER & PROFILE)
	created_at = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now = True)

class Appointment(models.Model):
	subject = models.CharField(max_length=255)
	start = models.DateTimeField()
	end = models.DateTimeField()
	user = models.ForeignKey(User, related_name = "appointments") # ONE TO MANY (USER & APPOINTMENTS)
	rejected = models.IntegerField() # default by 0. REJECTED = 1
	created_at = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now = True)

class Schedule(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	user = models.ForeignKey(User, related_name = "schedules") # ONE TO MANY (USER & SCHEDULES)
	#appointment = models.OneToOneField(Appointment, related_name="schedule") # ONE TO ONE (SCHEDULE & APPOINTMENTS)
	created_at = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
	message = models.TextField(max_length= 1000)
	user = models.ForeignKey(User,related_name ="messages") #ONE TO MANY (USER & MESSAGES)
	appointment = models.ForeignKey(Appointment, related_name = "messages") # ONE TO MANY (APPOINTMENT & MESSAGES)
	created_at = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now = True)

