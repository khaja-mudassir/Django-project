from django.db import models

# Create your models here.
class Details:
    name:str
    flatno:str
    vehno:str    
    prno:str
    nofmem:str

class Image:
    imgid:int
    imgname:str

class members:
    name:str
    email:str
    flatno:str
    mobile:str
    nofmem:str

class profile:
    name:str
    surname:str
    flatno:str
    nofmem:str
    vehno:str
    prno:str
    state:str
