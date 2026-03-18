# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Project, Review

# def saveVoteTotal_Ratio(sender, instance, *args, **kwargs):
#     project = instance.project

#     project.getVoteCount()

# post_save.connect(saveVoteTotal_Ratio, sender=Review)