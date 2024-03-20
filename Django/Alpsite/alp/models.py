from django.db import models

class Picture(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images',null=True)
    is_gallery_picture = models.BooleanField(default=False, verbose_name="Bild für Gallery")

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural  =  "Bilder"

class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    video = models.FileField(upload_to='videos',null=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural  =  "Videos"

class InformationDetail(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    images = models.ManyToManyField(Picture, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    secure = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural  =  "Informationen"
    
class Contact(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length = 254)
    gives_permission = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural  =  "Kontakte"



