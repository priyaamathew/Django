from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views
app_name ='accounts'
urlpatterns = [
   path('',views.home_view, name='home'),
   path('adminsignup/',views.admin_signup_view, name='admin_signup'), 
   path('doctorsignup',views.doctor_signup_view, name='doctor_signup'),
   path('patientsignup',views.patient_signup_view, name='patient_signup'),
   path('pharmacistsignup',views.pharmacist_signup_view, name='pharamacist_signup'),
   
   
   path('adminlogin', LoginView.as_view(template_name='accounts/adminlogin.html'),name='adminlogin'),
   path('doctorlogin', LoginView.as_view(template_name='accounts/doctorlogin.html'),name='doctorlogin'),
   path('patientlogin', LoginView.as_view(template_name='accounts/patientlogin.html'),name='patientlogin'),
   path('pharmacistlogin', LoginView.as_view(template_name='accounts/pharmacist_login.html'),name='pharmacistlogin'),
  
  
   
   
   path('admindashboard', views.admin_dashboardview, name='admin-dashboard'),
   path('admin-view-doctor', views.admin_doctor_view,name='admin-view-doctor'),
   path('approval/doctor/<int:pk>/',views.DoctorUpdateView.as_view(), name='DoctorUpdateView'),
   path('admin-view-patient', views.admin_patient_view,name='admin-view-patient'),
   path('approval/patient/<int:pk>/',views.PatientUpdateView.as_view(), name='PatientUpdateView'),
   path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
   path('approve-appointment/<int:pk>', views.BookUpdateView.as_view(),name='BookUpdateView'),
   path('approval/pharmacist/<int:pk>/',views.PharmacistUpdateView.as_view(), name='PharmacistUpdateView'),
   path('invoice-patient', views.admin_invoice_view,name='invoice-patient-view'),
   path('invoice-patient/<int:pk>', views.invoice_patient_view,name='invoice-patient'),
   
   
   path('prescription', views.doctor_prescription_view, name='doctor-prescription'),
  
   path('doctordashboard', views.doctor_dashboardview, name='doctor-dashboard'),
   #path('doctordashboard/prescription', views.PrescriptionUpdateView.as_view(), name='doctor-prescription'),
   
   path('patientdashboard', views.patient_dashboardview, name='patient-dashboard'),
   path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
   path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
   path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
   path('patient-view-prescription', views.prescription_view,name='patient-view-prescription'),
   path('patient-view-bill', views.bill_view,name='patient-view-bill'),
   
   path('pharmacistdashboard', views.pharmacist_dashboardview, name='pharmacist-dashboard'),
   path('pharmacistdashboard/add/',views.ProductCreateView.as_view(), name='Add_Product'),
   path('pharmacistdashboard/update/<int:pk>/',views.ProductUpdateView.as_view(), name='Update_Product'),
   path('pharmacistdashboard/delete/<int:pk>/',views.ProductDeleteView.as_view(), name='Delete_Product'),
]