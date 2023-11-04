from django.shortcuts import render,redirect
from django.urls import reverse
import mysql.connector
import os
from django.conf import settings
from .models import Details
from .models import Image
from .models import members
from .models import profile
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib 
from datetime import datetime
from django.contrib import messages 
import random
# Create your views here.
from django.http import HttpRequest,HttpResponse

def index(request):
    error_message = ""
    # return HttpResponse('<h1>welcome to my world</h1>')
    # return render(request,'index.html')
    if(request.method=="POST"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        uname=request.POST['username']
        email=request.POST['email']
        pwd=request.POST['password']
        mobile=request.POST['mobno']
        mycursor = conn.cursor()
        mycursor.execute("insert into register(uname,email,pwd,mobile) values('"+uname+"','"+email+"','"+pwd+"','"+mobile+"')")
        conn.commit()
    
        return render(request,'index.html',{"error_message": error_message})
    else:
        return render(request,'index.html',{"error_message": error_message})

def userprofile(request):
    if(request.method=="POST"):
      
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        name=request.POST['name']
        surname=request.POST['surname']
        flatno=request.POST['flatno']
        nofmem=request.POST['nofmem']
        vehno=request.POST['vehno']
        prno=request.POST['prno']
        state=request.POST['state']
        area=request.POST['area']
        edu=request.POST['edu']
        proff=request.POST['proff']
        country=request.POST['country']
        rel=request.POST['religion']
        mycursor = conn.cursor()
        mycursor.execute("insert into userdetails(userid,name,surname,flatno,nofmem,vehno,prno,state,area,edu,proff,country,rel) values('"+str(request.session['id'])+"','"+name+"','"+surname+"','"+flatno+"','"+nofmem+"','"+vehno+"','"+prno+"','"+state+"','"+area+"','"+edu+"','"+proff+"','"+country+"','"+rel+"')")
        # mycursor.execute("select * from userdetails where name='"+name+"',surname='"+surname+"',nofmem='"+nofmem+"',veh='"+vehno+"',prno='"+prno+"',state='"+state+"',area='"+area+"',edu='"+edu+"',proff='"+proff+"',country='"+country+"',religion='"+rel+"'")
        conn.commit()
      
        return redirect('welcome')
    else:
        return render(request,'userprofile.html')
    

def editprofile(request):
    if(request.method=='POST'):
        print('in post')
        name=request.POST['name']
        surname=request.POST['surname']
        flatno=request.POST['flatno']
        nofmem=request.POST['nofmem']
        vehno=request.POST['vehno']
        prno=request.POST['prno']
        state=request.POST['state']
        email=''
        if('email' in request.session and request.session['email']!=None):
            email=request.session['email']

            conn = mysql.connector.connect(

                host="localhost",
                user="root",
                password="",
                database="project"
        
            )
            mycursor=conn.cursor()
            mycursor.execute(
                    "UPDATE userdetails u "
                    "INNER JOIN register r ON u.userid = r.userid "
                    "SET u.name = '"+name+"', u.surname = '"+surname+"', u.flatno = '"+flatno+"', u.nofmem = '"+nofmem+"', u.vehno = '"+vehno+"', u.prno = '"+prno+"', u.state = '"+state+"' "
                    "WHERE r.email = '"+str(request.session['email'])+"'"
                )
            conn.commit()
            result=mycursor.fetchone()
            print(result)
            return redirect('welcome')
    else:
         email=''
         if('email' in request.session and request.session['email']!=None):
             email=request.session['email']
             conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="project"
             )
         mycursor=conn.cursor()
         
         mycursor.execute("select name,surname,flatno,nofmem,vehno,prno,state from userdetails u INNER JOIN register r ON u.userid=r.userid where r.email='"+email+"'")
         result=mycursor.fetchone()
         p=profile()
         p.name=result[0]
         p.surname=result[1]
         p.flatno=result[2]
         p.nofmem=result[3]
         p.vehno=result[4]
         p.prno=result[5]
         p.state=result[6]
         return render(request,'editprofile.html',{'profile':p})
    

def login(request):
    error_message = ""
    if(request.method=="POST"):
        email=request.POST['email']
        pwd=request.POST['password']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = conn.cursor()
        mycursor.execute("select pwd from register where email='"+email+"' ")
        result=mycursor.fetchone()

        if(result!=None):
            db_pwd=result[0]
            if(pwd==db_pwd):
                mycursor.execute("select * from register where email='"+email+"' and pwd='"+pwd+"'")
                result=mycursor.fetchone()
                if(result!=None):
                    request.session['email']=email
                    request.session['id'] = result[0]
                    mycursor.execute("select * from userdetails where userid='"+str(request.session['id'])+"'")
                    result=mycursor.fetchone()
                    if(result!=None):
                        return redirect('welcome')
                    else:
                        return redirect('userprofile')
                else:
                    error_message = "*Invalid credentials"
            else:
                error_message = "*Incorrect password or email"
                return render(request, "index.html",{"error_message": error_message})
        else:
            error_message = "*User not found"
            return render(request, "index.html",{"error_message": error_message})

        # Close the database connection
        conn.close()
    else:
        return render(request,"index.html")

    
def welcome(request):
    email=''
    if('email' in request.session and request.session['email']!=None):
        email=request.session['email']
        print("you are :",request.session.get('email'))
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = conn.cursor()
        mycursor.execute("SELECT name,flatno,vehno,prno,nofmem FROM `userdetails` u inner join register r ON u.userid=r.userid where r.email='"+email+"'")
        result=mycursor.fetchone()
        if(result!=None):
            d=Details()
            d.name=result[0]
            d.flatno=result[1]
            d.vehno=result[2]
            d.prno=result[3]
            d.nofmem=result[4]
            return render(request,'welcome.html',{'user':d})
    else:
        return redirect('index')
    

def adminlogin(request):
    error_message = ""
    if(request.method=="POST"):
        adm=request.POST['adminname']
        admcode=request.POST['admincode']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = conn.cursor()
        mycursor.execute("select * from admin where adm='"+adm+"' and admcode='"+admcode+"'")
        result=mycursor.fetchone()
        if(result!=None):
                return render(request,"admindashboard.html")
        else:
                error_message = "*Incorrect username or password"
                return render(request, "adminlogin.html", {"error_message": error_message})
    
    else:
        return render(request,'adminlogin.html')



    

def admindashboard(request):
    return render(request,'admindashboard.html')


def management(request):
        
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor = conn.cursor()
    mycursor.execute("SELECT u.userid,name,flatno,email,mobile,nofmem from userdetails u INNER JOIN register r on u.userid=r.userid")
    result = mycursor.fetchall()
    print(result)
    if result:
        # Pass the result data to the template
        return render(request, 'management.html', {'management_data': result})
    else:
        return render(request, 'management.html', {'error_message': 'No Records found'})



def addnotice(request):
    if(request.method=="POST"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        name=request.POST['nname']
        type=request.POST['ntype']
        don=request.POST['ndate']
        message=request.POST['nmsg']
        mycursor = conn.cursor()
        mycursor.execute("insert into addnotice(name,type,don,message) values('"+name+"','"+type+"','"+don+"','"+message+"')")
        conn.commit()
    return render(request,'addnotice.html')
    


def viewcomplaints(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor = conn.cursor()
    mycursor.execute("SELECT * from complaints")
    result = mycursor.fetchall()
    print(result)
    if result:
        # Pass the result data to the template
        return render(request, 'viewcomplaints.html', {'complaints_data': result})
    else:
        return render(request, 'viewcomplaints.html', {'error_message': 'No Records found'})

    # return render(request,'viewcomplaints.html')


def viewpayment(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor = conn.cursor()
    mycursor.execute("SELECT * from payment")
    result = mycursor.fetchall()
    print(result)
    if result:

        return render(request,'viewpayment.html',{'payment_data': result})
    else:
        return render(request,'viewpayment.html',{'error_message': 'No Records found'})


def photo(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['my_image']
        saved_file_path = handle_uploaded_file(uploaded_file)
        print("saved"+saved_file_path)
        s=saved_file_path.split("\\")
        print(s[1])
        conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="project"
            )
        # s=saved_file_path.split("\\")
        mycursor=conn.cursor()
        mycursor.execute("insert into photo(imgname) values('"+s[1]+"')")
        conn.commit()
        return render(request,'photo.html',{'status':'stored successfully',  'uploaded_file_url': saved_file_path})
    else:
        return render(request,'photo.html')
    # return render(request,'photo.html')

def photogallery(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor=conn.cursor()
    mycursor.execute("select * from photo")
    result=mycursor.fetchall()
    print(result)
    if result:
        return render(request,'photogallery.html',{'images_data':result,"IMAGEURL":settings.MEDIA_URL})
    else:
        return render(request,'photogallery.html',{'error_message':'No records found'})

def userphotogallery(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor=conn.cursor()
    mycursor.execute("select * from photo")
    result=mycursor.fetchall()
    print(result)
    if result:
        return render(request,'userphotogallery.html',{'images_data':result,"IMAGEURL":settings.MEDIA_URL})
    else:
        return render(request,'userphotogallery.html',{'error_message':'No records found'})

    



def noticeboard(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    mycursor = conn.cursor()
    mycursor.execute("SELECT * from addnotice")
    result = mycursor.fetchall()
    print(result)
    if result:
        # Pass the result data to the template
        return render(request, 'noticeboard.html', {'notice_data': result})
    else:
        return render(request, 'noticeboard.html', {'error_message': 'No Records found'})





    return render(request,'noticeboard.html')

def complaint(request):
    if(request.method=="POST"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        title=request.POST['ctitle']
        flatno=request.POST['cflat']
        message=request.POST['cmsg']
        mycursor = conn.cursor()
        mycursor.execute("insert into complaints(title,flatno,message) values('"+title+"','"+flatno+"','"+message+"')")
        conn.commit()

    return render(request,'complaint.html',{"status": "Submitted successfully"})



def payment(request):
    if(request.method=="POST"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        name=request.POST['ptitle']
        flatno=request.POST['pflat']
        amount=request.POST['pamount']
        if 'paymentStatus' in request.POST:
            pstatus=request.POST['paymentStatus']
        else:
            pstatus = "Unpaid"
        mycursor = conn.cursor()
        mycursor.execute("insert into payment(name,flatno,amount,pstatus) values('"+name+"','"+flatno+"','"+amount+"','"+pstatus+"')")
        conn.commit()

    return render(request,'payment.html')

def userphoto(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['my_image']
        saved_file_path = handle_uploaded_file(uploaded_file)
        print("saved"+saved_file_path)
        s=saved_file_path.split("\\")
        print(s[1])
        conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="project"
            )
        # s=saved_file_path.split("\\")
        mycursor=conn.cursor()
        mycursor.execute("insert into photo(imgname) values('"+s[1]+"')")
        conn.commit()
        return render(request,'userphoto.html',{'status':'stored successfully',  'uploaded_file_url': saved_file_path})
        
    else:
        return render(request,'userphoto.html')






    # return render(request,'userphoto.html')

def Addmember(request):  
    if(request.method=="POST"):
        print('in post')
        name=request.POST['username']
        email=request.POST['email']
        flatno=request.POST['flatno']
        mobile=request.POST['mobno']
        nofmem=request.POST['nofmem']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",    
            password="",
            database="project"        
            )
        mycursor = conn.cursor()
        mycursor.execute ( "INSERT INTO register ( email, mobile) VALUES ( '"+email+"', '"+mobile+"')")
        mycursor.execute("INSERT INTO userdetails ( name, flatno, nofmem) VALUES ('"+name+"', '"+flatno+"', '"+nofmem+"')") 

        # mycursor.execute(insert_register_query, (email, mobile))
        # mycursor.execute(insert_userdata_query, (name,flatno, nofmem))
        conn.commit()
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = conn.cursor()
        mycursor.execute("SELECT u.userid,name,flatno,email,mobile,nofmem from userdetails u INNER JOIN register r on u.userid=r.userid")
        result = mycursor.fetchall()
        print(result)
        if result:
            # Pass the result data to the template
            return render(request, 'management.html', {'management_data': result})
        else:
            return render(request, 'management.html', {'error_message': 'No Records found'})
    
    else:
        return render(request,'Addmember.html')

def Updatemember(request,id):
    if(request.method=='POST'):
        print('in post')
        name=request.POST['username']
        email=request.POST['email']
        flatno=request.POST['flatno']
        mobile=request.POST['mobno']
        nofmem=request.POST['nofmem']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor=conn.cursor()
        mycursor.execute("update register set email='"+email+"', mobile='"+mobile+"' where userid="+str(id))
        mycursor.execute("update userdetails set name='"+name+"', flatno='"+flatno+"',nofmem='"+nofmem+"' where userid="+str(id))
        conn.commit()
        result=mycursor.fetchone()
        print(result)
        return redirect('management')
    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor=conn.cursor()
        mycursor.execute("SELECT name, email, flatno, mobile, nofmem FROM register INNER JOIN userdetails ON register.userid = userdetails.userid WHERE register.userid ="+str(id))
        result=mycursor.fetchone()
        m=members()
        m.name=result[0]
        m.email=result[1]
        m.flatno=result[2]
        m.mobile=result[3]
        m.nofmem=result[4]
        return render(request,'Updatemember.html',{'members':m})


def Deletemember(request,id):
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    name = request.POST.get('name')
    flatno = request.POST.get('flatno')
    nofmem = request.POST.get('nofmem') 
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    print("id:",str(id))
    mycursor = conn.cursor()
    # delete_register_query = "DELETE FROM register WHERE userid = %d"
    # delete_userdata_query = "DELETE FROM userdetails WHERE userid = %d"
    mycursor.execute("DELETE FROM register WHERE userid = "+str(id))
    mycursor.execute("DELETE FROM userdetails WHERE userid = "+str(id))
    conn.commit()
    return redirect('management')





def handle_uploaded_file(uploaded_file):
    # Define the directory where you want to save the uploaded files
    upload_dir = 'media'
    
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Generate a unique file name (you can modify this as needed)
    file_name = os.path.join(upload_dir, uploaded_file.name)
    
    # Open the destination file and save the uploaded file data into it
    with open(file_name, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_name


def loadimages(request):
    conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="project"
            )
    mycursor=conn.cursor()
    mycursor.execute("select * from photo")
    result=mycursor.fetchall()
    images=[]
    if(result!=None):
        for x in result:
            s=Image()
            s.imgid=x[0]
            s.imgname=x[1]
            images.append(s)
    return render(request,'loadimages.html',{"images":images,"MEDIA_URL":settings.MEDIA_URL})

def forgotpassword(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = conn.cursor()
        # retrieve post details
        email = request.POST['email']
        mycursor.execute(
            "SELECT pwd FROM register WHERE email='" + email + "'")
        result = mycursor.fetchone()
        pwd = str(result)
        if result is not None:
            # SMTP server configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'k.mudassiruddin786@gmail.com'
            # For App Password, enable 2-step verification, then create an app password
            smtp_password = 'yudh xffz qiwz hoxy'
            # Email content
            subject = 'Password recovery'
            body = 'This is a Password recovery email sent from Community maintainance. ' \
                   'Your password as per registration is: ' + pwd[2:len(pwd) - 3]
            sender_email = 'k.mudassiruddin786@gmail.com'
            receiver_email = email
            # Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            message = "Password sent to the given email ID"
            return render(request, 'index.html', {'alert_message': message})
        else:
            message = "Please enter the correct email ID"
            return render(request, 'forgotpassword.html', {'alert_message': message})
    else:
        return render(request, 'forgotpassword.html')
    


def logout(request):
    try:
        if(request.session['email']!=None):
            del request.session["email"]
    except KeyError:
        pass
    return redirect('index')

    
# def welcome(request):
#     if('email' not in request.session):
#         return redirect('index')
#     return render(request,"welcome.html")


    

# def login(request):
#     error_message = None
#     if(request.method=="POST"):
#         email=request.POST['email']
#         pwd=request.POST['password']
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="project"
#         )
#         mycursor = conn.cursor()
#         mycursor.execute("select * from register where email='"+email+"' and pwd='"+pwd+"'")
#         result=mycursor.fetchone()
#         if(result!=None):
#             request.session['email']=email
#             request.session['id'] = result[0]
#             mycursor.execute("select * from userdetails where userid='"+str(request.session['id'])+"'")
#             result=mycursor.fetchone()
#             if(result!=None):
#                 return redirect("welcome")
#             else:
#                 return redirect("userprofile")
#         else:
#             return render(request,"index.html")
#     else:
#         return render(request,'index.html')


# def adminlogin(request):
#     if(request.method=="POST"):
#         adm=request.POST['adminname']
#         admcode=request.POST['admincode']
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="project"
#         )
#         mycursor = conn.cursor()
#         mycursor.execute("select * from admin where adm='"+adm+"' and admcode='"+admcode+"'")
#         result=mycursor.fetchone()
#         if(result!=None):
#             return render(request,"admindashboard.html")
#         else:
#             return render(request,"adminlogin.html")
#     else:
#         return render(request,'adminlogin.html')

                        



