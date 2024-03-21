from django.db import models
import requests
# Create your models here.
class Location(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            api_key = 'p7f8uSHnqiztfA1tGPXsHvxu865ktBvj'
            url = f'https://api.tomtom.com/search/2/geocode/{self.address}.json?limit=1&key={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    self.latitude = data['results'][0]['position']['lat']
                    self.longitude = data['results'][0]['position']['lon']
                    #print(self.latitude, self.longitude)
        super().save(*args, **kwargs)