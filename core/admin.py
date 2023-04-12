from django.contrib import admin
from .models import Profile,Post,LikePost,Followers,Thread,ChatMessage,Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Followers)
admin.site.register(ChatMessage)
admin.site.register(Review)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)