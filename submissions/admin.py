from django.contrib import admin

from .models import (
    Area, Submission, SubmissionStatus, Supervisor, Supplier, FaultSource, Classification,
    Originator, MachineType, IssueDetails, NotificationRecipient
)

admin.site.register(Area)
admin.site.register(Supervisor)
admin.site.register(Supplier)
admin.site.register(FaultSource)
admin.site.register(Classification)
admin.site.register(Originator)
admin.site.register(MachineType)
admin.site.register(IssueDetails)
admin.site.register(NotificationRecipient)
admin.site.register(SubmissionStatus)
admin.site.register(Submission)