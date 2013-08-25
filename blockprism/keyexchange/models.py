from django.db import models
from django.contrib import admin

class PublicKey(models.Model):
    public_key = models.TextField(db_index=True, unique=True)


class Facebook(models.Model):
    facebook_id = models.CharField(max_length=32, unique=True)
    public_key = models.ForeignKey(PublicKey)

    def __unicode__(self):
        return self.facebook_id


class GMail(models.Model):
    gmail_id = models.CharField(max_length=32, unique=True)
    public_key = models.ForeignKey(PublicKey)
    
    def __unicode__(self):
        return self.gmail_id

admin.site.register(PublicKey)
admin.site.register(Facebook)
admin.site.register(GMail)