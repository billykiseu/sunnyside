# Custom Analytics app
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .utils import get_client_ip, get_client_loc
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from base.signals import user_logged_in, user_logged_out
from .signals import object_viewed_signal

User = settings.AUTH_USER_MODEL


FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE')
FORCE_USER_END_INACTIVE = getattr(settings, 'FORCE_USER_END_INACTIVE')


class ObjectViewed(models.Model):
    user = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    object_name = models.CharField(max_length=120, blank=True, null=True)
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=120, blank=True, null=True)


def __str__(self, ):
    return "%s viewed: %s" % (self.content_object, self.timestamp)


class Meta:
    ordering = ['-timestamp']
    verbose_name = 'Object Viewed'
    verbose_name_plural = 'Objects Viewed'

# Item viewed receiver


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    ip_address = get_client_ip(request)
    client_loc = get_client_loc(request)
    c_type = ContentType.objects.get_for_model(sender)
    new_view_obj = ObjectViewed.objects.create(
        user=request.user,
        object_id=instance.id,
        object_name=instance.name,
        content_type=c_type,
        ip_address=ip_address,
        location=client_loc,
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    session_key = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)
    location = models.CharField(max_length=120, blank=True, null=True)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, request, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(
            user=instance.user, ended=False, active=False).exclude(pk=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

# killinactive user sessions


def post_save_user_changed_receiver(sender, instance, created, request, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(
                user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()


if FORCE_USER_END_INACTIVE:
    post_save.connect(post_save_user_changed_receiver, sender=User)

# Login receiver


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    client_loc = get_client_loc(request)
    session_key = request.session.session_key
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key,
        location=client_loc,)


user_logged_in.connect(user_logged_in_receiver)


def user_logged_out_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ended = True


user_logged_out.connect(user_logged_out_receiver)
