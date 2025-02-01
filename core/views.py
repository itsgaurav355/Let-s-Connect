from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse
from .models import Profile ,Post,LikePost,Followers,Review, Message
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.db.models import Q

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    user_following_list =[]
    feed = []

    user_following = Followers.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
       
    feed_list = list(chain(*feed))
    
    #Suggestion list for a user
    all_users = User.objects.all() # lenscart dmart subways ... 
    user_following_all = []
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    curr_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(curr_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)
    
    suggestion_profile_list = list(chain(*username_profile_list))
    return render(request,'index.html',{'user_object':user_object,'user_profile':user_profile,'posts':feed_list,'suggestion_profile_list':suggestion_profile_list[:4]})

def home(request):
    return render(request,'main.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')
    

def signin(request):
    if request.method == "POST":
        username =request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages = 'Credentials are Invalid '
            return render(request,'signin.html',{'messages':messages})
    else:
        pass
    return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        
        if request.FILES.get('image')== None:
            image =user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            # year = request.POST['year']


            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            # user_profile.year = year 

            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            # year = request.POST['year']


            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            # user_profile.year = year 
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method ==  "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()

        return redirect('/home')
    
    else:
        return redirect('/home')

def review(request):
    if request.method ==  "POST":
        user = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']

        new_rev = Review.objects.create(name=user,email=email,desc=description)
        new_rev.save()

        return redirect('/')
    
    else:
        return redirect('/') 

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id = post_id)
    like_filter = LikePost.objects.filter(post_id = post_id,username = username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.noOfLikes=post.noOfLikes+1
        post.save()
        return redirect('/home')
    else:
        like_filter.delete()
        post.noOfLikes=post.noOfLikes-1
        post.save()
        return redirect('/home')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk
    
    if Followers.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(Followers.objects.filter(user=pk))
    user_following = len(Followers.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/home')

@login_required(login_url='signin')
def messages_page(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    # Get all followers and following users
    followers = Followers.objects.filter(Q(follower=request.user.username) | Q(user=request.user.username))
    chat_partners = User.objects.filter(
        Q(username__in=[f.user for f in followers]) |
        Q(username__in=[f.follower for f in followers])
    ).exclude(username=request.user.username).distinct()

    return render(request, 'messages.html', {
        'user_profile': user_profile,
        'chat_partners': chat_partners
    })

@login_required(login_url='signin')
def get_messages(request, chat_partner_id):
    chat_partner = User.objects.get(id=chat_partner_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=chat_partner) |
        Q(sender=chat_partner, receiver=request.user)
    ).order_by('timestamp')
    
    # Mark messages as read
    unread_messages = messages.filter(is_read=False, receiver=request.user)
    unread_messages.update(is_read=True)
    
    return JsonResponse([{
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages], safe=False)

@login_required(login_url='signin')
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id
        })
    return JsonResponse({'status': 'error'})

@login_required
def send_typing(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        is_typing = request.POST.get('is_typing')
        # Implement your typing indicator logic here
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def check_typing(request, chat_partner_id):
    # Implement your typing status check here
    return JsonResponse({'is_typing': False, 'username': ''})
    