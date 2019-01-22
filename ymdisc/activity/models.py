from django.db import models
from django.conf import settings


class Activity(models.Model):
    index = models.SmallIntegerField(unique=True)
    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=512, blank=True)
    publish_date = models.DateField(null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['index']
        verbose_name_plural = 'activities'


class Section(models.Model):
    index = models.SmallIntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='')
    instructions = models.CharField(max_length=512)
    link_name = models.CharField(max_length=50, blank=True)
    link = models.URLField(default="", blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.activity.title + " Section " + str(self.index)

    def save(self, *args, **kwargs):    # set the default value of visible to true for the first section
        if self.index == 1:
            self.visible = True
        super(Section, self).save(*args, **kwargs)

    class Meta:
        ordering = ['index']
        unique_together = ('activity', 'index')


class Item(models.Model):
    index = models.SmallIntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.section) + " Item " + str(self.index)

    def get_comments(self):
        return self.comment_set.all()

    class Meta:
        ordering = ['index']
        unique_together = ('section', 'index')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comment by " + self.user.first_name + " on " + str(self.item)

    class Meta:
        ordering = ['comment_date_time']


class ImageQuote(models.Model):
    title = models.CharField(max_length=50)
    image_filename = models.CharField(max_length=50)

    def __str__(self):
        return self.title


