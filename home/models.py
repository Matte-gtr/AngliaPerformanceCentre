from django.db import models


class Site_Page(models.Model):
    name = models.CharField(max_length=56, blank=False, null=False)
    page_link = models.CharField(max_length=254, blank=False, null=False)

    def __str__(self):
        return str(self.name)


class Advert(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to="adverts", blank=False, null=False)
    url = models.ForeignKey(Site_Page, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
