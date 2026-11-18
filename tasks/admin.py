from django.contrib import admin

from .models import Comment, Membership, Task, TaskList

admin.site.register(TaskList)
admin.site.register(Membership)
admin.site.register(Task)
admin.site.register(Comment)