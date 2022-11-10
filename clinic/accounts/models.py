from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='images',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)
    
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='image',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    token_number=models.PositiveIntegerField(default=0)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
    

class Pharmacist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='images',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True) 
    status=models.BooleanField(default=False)
    
    def  __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    token_number=models.PositiveIntegerField(default=0)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.patientName+" ("+self.doctorName+")"
    

class Medicine(models.Model):
    def __str__(self):
        return self.item_name
    item_name = models.CharField(max_length=100)
    itemprice_per_strip = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=200)
    quantity_in_strip = models.PositiveIntegerField(null=True)
    manufractureDate=models.DateField()
    expirayDate =models.DateField()

class Prescription(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    address = models.CharField(max_length=40)
    doctorName=models.CharField(max_length=40,null=True)
    medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    def  __str__(self):
        return self.patientName+" ("+self.doctorName+")"

class PatientBill(models.Model):
    Date=models.DateField(auto_now=True)
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    def  __str__(self):
        return self.patientName
