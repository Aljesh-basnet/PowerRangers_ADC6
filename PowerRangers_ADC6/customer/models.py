from django.db import models

class BookRoom(models.Model):
    cname = models.CharField(max_length=20)
    roomtype =models.CharField(max_length=20)
    roomno=models.IntegerField(max_length=20)
    cemail = models.EmailField()
    ccontact = models.CharField(max_length=15)
            

    def __str__(self):
        return f"{self.cname} has booked {self.roomno}"
