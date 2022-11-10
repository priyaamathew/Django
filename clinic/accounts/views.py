from operator import truediv
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q

# Create your views here.
def home_view(request):
    return render(request,'accounts/index.html')
# Signup views 

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'accounts/adminsignup.html',{'form':form})

def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'accounts/doctorsignup.html',context=mydict)

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'accounts/patientsignup.html',context=mydict)

def pharmacist_signup_view(request):
    userForm=forms.PharmacistUserForm()
    PharmacistForm=forms.PharmacistForm()
    mydict={'userForm':userForm,'PharmacistForm':PharmacistForm}
    if request.method=='POST':
        userForm=forms.PharmacistUserForm(request.POST)
        PharmacistForm=forms.PharmacistForm(request.POST,request.FILES)
        if userForm.is_valid() and PharmacistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            pharmacist=PharmacistForm.save(commit=False)
            pharmacist.user=user
            pharmacist=pharmacist.save()
            my_pharmacist_group = Group.objects.get_or_create(name='PHARMACIST')
            my_pharmacist_group[0].user_set.add(user)
        return HttpResponseRedirect('pharmacistlogin')
    return render(request,'accounts/pharmacistsignup.html',context=mydict)

#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_pharmacist(user):
    return user.groups.filter(name='PHARMACIST').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('accounts/admindashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('accounts/doctordashboard')
        else:
            return render(request,'accounts/doctor_wait_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('accounts/patientdashboard')
        else:
            return render(request,'accounts/patient_wait_approval.html')
    elif is_pharmacist(request.user):
        accountapproval=models.Pharmacist.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('accounts/pharmacistdashboard')
        else:
            return render(request,'accounts/pharmaist_wait_approval.html')
 

# Admin views start

def admin_dashboardview(request):
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    appointment=models.Appointment.objects.all()
    pharmacist=models.Pharmacist.objects.all().filter(status=False)
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()
    patientcount=models.Patient.objects.all().filter(status=True).count()
    doctor=models.Doctor.objects.all().filter(status=False)
    patient=models.Patient.objects.all().filter(status=False)
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()
    appointment=models.Appointment.objects.all().filter(status=False)
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    
    mydict={
    'doctors':doctors,
    'doctor':doctor,
    'patients':patients,
    'patient':patient,
    'appoinment': appointment,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pharmacist':pharmacist
   
    }
    return render(request,'accounts/admindashboard.html',context=mydict)



def admin_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'accounts/admin_doctor.html',{'doctors':doctors})

# for providing token number and approval

class DoctorUpdateView(UpdateView):
    model = models.Doctor
    fields = ['status']
    template_name = 'accounts/doctor_update.html'
    success_url = reverse_lazy('accounts:admin-dashboard')
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'accounts/admin_patient.html',{'patients':patients})

class PatientUpdateView(UpdateView):
    model = models.Patient
    fields = ['token_number','status']
    template_name = 'accounts/patient_update.html'
    success_url = reverse_lazy('accounts:admin-dashboard')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})

class BookUpdateView(UpdateView):
    model = models.Appointment
    fields = ['token_number','status']
    template_name = 'accounts/booking_update.html'
    success_url = reverse_lazy('accounts:admin-dashboard')

class PharmacistUpdateView(UpdateView):
    model = models.Pharmacist
    fields = ['status']
    template_name = 'accounts/pharmacist_update.html'
    success_url = reverse_lazy('accounts:admin-dashboard')


def doctor_dashboardview(request):
    patient=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    patientbill=models.PatientBill.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    prescription=models.Prescription.objects.all().filter(status=True,doctorId=request.user.id)
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
     'prescription':prescription,   
    'patient':patient,
    'patientbill': patientbill,
    'appointmentcount':appointmentcount,
    'patientcount':patientcount,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'accounts/doctordashboard.html',context=mydict)

   




# patient view start here
def patient_dashboardview(request):
   patient=models.Patient.objects.get(user_id=request.user.id)
   doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
   appointmentcount=models.Appointment.objects.all().filter(status=False,patientId=request.user.id).count()
   prescriptioncount=models.Prescription.objects.all().filter(status=False,patientId=request.user.id).count()
   mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'appointmentcount':appointmentcount,
    'prescriptioncount':prescriptioncount

    }
    
   return render(request,'accounts/patientdashboard.html',context=mydict)


def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'accounts/patient_appointment.html',{'patient':patient})



def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patientdashboard')
    return render(request,'accounts/patient_book_appointment.html',context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id,status=True)
    return render(request,'accounts/patient_view_appointment.html',{'appointments':appointments,'patient':patient})

def doctor_prescription_view(request):
    PrescriptionForm=forms.PrescriptionForm()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'PrescriptionForm': PrescriptionForm,'doctor':doctor,'message':message}
    if request.method=='POST':
        PrescriptionForm=forms.PrescriptionForm(request.POST)
        if PrescriptionForm.is_valid():
            print(request.POST.get('patientId'))
            desc=request.POST.get('description')

            patient=models.Patient.objects.get(user_id=request.POST.get('patientId'))
            
            prescription=PrescriptionForm.save(commit=False)
            prescription.patientId=request.POST.get('patientId')
            prescription.doctorId=request.user.id #----user can choose any patient but only their info will be stored
            prescription.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
           # prescription.address=models.Patient.objects.get(id=request.POST.get('patientId')).address
            prescription.doctorName=request.user.first_name+request.user.last_name #----user can choose any patient but only their info will be stored
            prescription.status=True
            prescription.save()
        return HttpResponseRedirect('doctordashboard')
    return render(request,'accounts/prescription.html',context=mydict)






class PrescriptionUpdateView(CreateView):
    model = models.Prescription
    fields =['doctorName','patientName','address','description','medicine','status']
    template_name = 'accounts/doctor_prescription.html'
    success_url = reverse_lazy('accounts:doctor-dashboard')

def prescription_view(request):
    pres=models.Prescription.objects.all().filter(status=True,patientId=request.user.id)
    context= {
           'prescription':pres
    }
    #return HttpResponseRedirect('patientdashboard')
    return render(request, 'accounts/view_prescription.html',context)
def bill_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    billDetails=models.PatientBill.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if billDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':billDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        
        
        'medicineCost':billDetails[0].medicineCost,
       
        'doctorFee':billDetails[0].doctorFee,
        
        'total':billDetails[0].total,
        }
        print(patientDict)
    
    return render(request, 'accounts/patient_billview.html', patientDict)

def pharmacist_dashboardview(request):
    prod = models.Medicine.objects.all()
    context = { 

        'prod': prod
    }
    return render(request, 'accounts/pharmacistdashboard.html',context)

# medicine inventory
class ProductCreateView(CreateView):
    model = models.Medicine
    fields = ['item_name','itemprice_per_strip','description','quantity_in_strip','manufractureDate', 'expirayDate']
    template_name = 'accounts/add_medicine.html'
    success_url = reverse_lazy('accounts:pharmacist-dashboard')

class ProductUpdateView(UpdateView):
    model = models.Medicine
    fields = ['item_name','itemprice_per_strip','description','quantity_in_strip','manufractureDate','expirayDate']
    template_name = 'accounts/update_medicine.html'
    success_url = reverse_lazy('accounts:pharmacist-dashboard')

class ProductDeleteView(DeleteView):
    model = models.Medicine
    fields = ['item_name','itemprice_per_strip','description','quantity_in_strip','manufractureDate','expirayDate']
    template_name = 'accounts/delete_medicine.html'
    success_url = reverse_lazy('accounts:pharmacist-dashboard')






def admin_invoice_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'accounts/admin_invoice.html',{'patients':patients})


def invoice_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    #appointment=models.Appointment.objects.get(id=pk)
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
  

    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
           
            'total':(int(request.POST['doctorFee'])+int(request.POST['medicineCost']))
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientBill()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
      
       
        pDD.medicineCost=int(request.POST['medicineCost'])
       
        pDD.doctorFee=int(request.POST['doctorFee'])
       
        pDD.total=(int(request.POST['doctorFee'])+int(request.POST['medicineCost']))
        pDD.save()
        return render(request,'accounts/patient_final_bill.html',context=patientDict)
    return render(request,'accounts/patient_generate_bill.html',context=patientDict)
