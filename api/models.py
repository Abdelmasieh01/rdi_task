from django.db import models
from django.core.exceptions import ValidationError


class Content(models.Model):
    # This is an abstract model used only to add those fields to other models by inheritance
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    
class Image(Content):
    file = models.ImageField(verbose_name="Image Url", upload_to='images/')
    width = models.PositiveSmallIntegerField(verbose_name="Image width")
    height = models.PositiveSmallIntegerField(verbose_name="Image height")
    channels = models.PositiveBigIntegerField(verbose_name="Number of channels")


def validate_pdf_type(value):
    if value.file.file.content_type != "application/pdf":
        raise ValidationError("The file is not a pdf!")


class Pdf(Content):
    file = models.FileField(verbose_name="File Url", upload_to="PDFs/", validators=[validate_pdf_type])
    page_count = models.PositiveSmallIntegerField(verbose_name="Number of pages")
    width = models.PositiveSmallIntegerField(verbose_name="Page width")
    height = models.PositiveSmallIntegerField(verbose_name="Page height")
