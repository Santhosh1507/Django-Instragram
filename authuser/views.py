from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import  Followers, LikePost, Post, Profile, Comment, Notification
from django.db.models import Q



def signup(request):
 try:
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        if my_user is not None:
            login(request,my_user)
            return redirect('/')
        return redirect('/loginn')
    
        
 except:
        invalid="User already exists"
        return render(request, 'signup.html',{'invalid':invalid})
  
    
 return render(request, 'signup.html')
        
     
def loginn(request): 
  if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
    
        invalid="Invalid Credentials"
        return render(request, 'loginn.html',{'invalid':invalid})
               
  return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')



@login_required(login_url='/loginn')
def home(request):
    # Fetch all posts, ordered by creation date
    posts = Post.objects.all().order_by('-created_at')

    # Get a list of users that the current user is following
    following_users = Followers.objects.filter(follower=request.user).values_list('user', flat=True)

    # Get the comments for the posts, and select the user and post to avoid additional queries
    comment_posts = Comment.objects.filter(post__in=posts).select_related('user', 'post', 'profile')

    # Get the profiles for the users who commented on these posts (avoiding multiple queries)
    comment_profiles = {comment.user.id: comment.profile.profileimg for comment in comment_posts}
    
    # Get the posts where the user or their following users are the authors or the users who commented
    post = Post.objects.filter(
        Q(user=request.user) |
        Q(user__in=following_users) |
        Q(user__in=[comment.user.id for comment in comment_posts])
    ).select_related('user').prefetch_related(
        'comments__user',
    ).order_by('-created_at')
    print(post)
    # Suggested users to follow (excluding the current user and the ones already followed)
    suggested_users = User.objects.exclude(id__in=following_users).exclude(id=request.user.id)
    suggested_profiles = Profile.objects.filter(user__in=suggested_users)
    
    # for suggest in suggested_users:
    #     user_object = User.objects.get(username=suggest)
    #     print(user_object)
        
    # suggest_user = {suggest.username: suggest.username for suggest in suggested_users}

    # print(suggest_user)
   
    # Get the current user's profile
    profile = Profile.objects.get(user=request.user)
    # user_object = User.objects.get(username=id_user)
    
    # print(user_object)
    # follower = request.user
    # print(f'follower: {follower}')
    # user = user_object
    # print(f'user: {user}')
    
    # follow_unfollow = 'Unfollow'
    
    # if Followers.objects.filter(follower=follower, user=user).exists():
    #     follow_unfollow = 'Unfollow'
    # else:
    #     follow_unfollow = 'Follow'
    
    user_likes = LikePost.objects.filter(username=request.user, post_id__in=post, liked=True).values_list('post_id', flat=True)
    like_status = list(user_likes)
    
    
    # user_likes = {post.id: LikePost.objects.filter(post_id=post.id, username=request.user).exists() for post in posts}
    # print(user_likes)
    
    context = {
        'post': post,
        'profile': profile,
        'suggested_users': suggested_users,
        'suggested_profiles': suggested_profiles,
        'comment_profiles': comment_profiles,
        'user_likes': user_likes,
        'like_status': like_status, # Pass the profiles of users who commented
    }

    return render(request, 'main.html', context)


@login_required(login_url='/loginn')
def upload(request):
    if request.method == 'POST':
        user = request.user  # Assign the entire User instance, not just the username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        # Create and save the new post
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        user = request.user  # This is the actual User object
        post = get_object_or_404(Post, id=id)

        # Corrected filter logic using ForeignKey relationships
        like_filter = LikePost.objects.filter(post_id=post, username=user).first()

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=post, username=user, liked=True)
            post.no_of_likes = post.no_of_likes + 1
            if user != post.user:
                sender_profile = Profile.objects.get(user=user)
                Notification.objects.create(
                    receiver=post.user,  # Use receiver instead of user
                    sender=user,
                    notification_type='like',
                    post=post, 
                    sender_profile_image=sender_profile.profileimg.url,
                )
            
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()
        # Redirect to the post detail page after updating the like status
        # return redirect(f'/{post.id}#likes')
        # Redirect back to the post's detail page
        return redirect('/') 
    
@login_required(login_url='/loginn')
def explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context={
        'post':post,
        'profile':profile
        
    }
    return render(request, 'explore.html',context)
    
@login_required(login_url='/loginn')
def profile(request,id_user):
    user_object = User.objects.get(username=id_user)
    
    profile = Profile.objects.get(user=request.user)
    
    user_profile = Profile.objects.get(user=user_object)
    
    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')

    user_post_length = user_posts.count() 

    
    follower = request.user
    user = user_object
    follow_unfollow = 'Unfollow'
    
    if Followers.objects.filter(follower=follower, user=user).exists():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'
   
    
    # Count followers and following
    user_followers = Followers.objects.filter(user=user).count()
    user_following = Followers.objects.filter(follower=user).count()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow': follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
             image = user_profile.profileimg
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            if request.FILES.get('image') != None:
             image = request.FILES.get('image')
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            

            return redirect(f'/profile/{id_user}')
        else:
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)

@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/'+ request.user.username)


@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)
    profile = Profile.objects.get(user=request.user)
    context = {
        'query': query,
        'users': users,
        'posts': posts,
        'profile':profile
    }
    return render(request, 'search_user.html', context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)



def follow(request):
    if request.method == 'POST':
        follower = request.user  # Automatically use the logged-in user as the follower
        user = User.objects.get(username=request.POST['user'])  # Get the user to be followed
        print(user)
        print(follower)
        sender_profile = Profile.objects.get(user=follower)

        if Followers.objects.filter(follower=follower, user=user).exists():
            # Unfollow logic: delete the existing follower relationship
            Followers.objects.filter(follower=follower, user=user).delete()
            return redirect(f'/profile/{user.username}')
        else:
            # Follow logic: create a new follower relationship
            Followers.objects.create(follower=follower, user=user)
            Notification.objects.create(receiver=user, sender=follower, notification_type='follow', sender_profile_image=sender_profile.profileimg.url)
            return redirect(f'/profile/{user.username}')
    else:
        return redirect('/')
    
    
    
def comment_post(request, post_id):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, id=post_id)  # Fetch the post or 404 if not found
        profile = Profile.objects.get(user=user)  # Use capital 'P' for Profile

        comment_text = request.POST.get('comment_text')  # Use the correct key 'comment_text'
        if comment_text:
            Comment.objects.create(user=user, post=post, profile=profile, comment_text=comment_text)
            if user != post.user:
                sender_profile = Profile.objects.get(user=user)
                Notification.objects.create(
                    receiver=post.user,  # Use `receiver` instead of `user`
                    sender=user,
                    notification_type='comment',
                    post=post,
                    comment_text=comment_text,
                    sender_profile_image=sender_profile.profileimg.url
                )
        return redirect('/')  # Redirect back to the home page after posting
    else:
        return redirect('/')
    
    
    
def follower(request):
    if request.method == 'POST':
        follower = request.user  # Automatically use the logged-in user as the follower
        user = User.objects.get(username=request.POST['user'])  # Get the user to be followed
        print(user)
        print(follower)
        sender_profile = Profile.objects.get(user=follower)

        if Followers.objects.filter(follower=follower, user=user).exists():
            # Unfollow logic: delete the existing follower relationship
            Followers.objects.filter(follower=follower, user=user).delete()
            return redirect('/')
        else:
            # Follow logic: create a new follower relationship
            Followers.objects.create(follower=follower, user=user)
            Notification.objects.create(receiver=user, sender=follower, notification_type='follow', sender_profile_image=sender_profile.profileimg.url)
            return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/loginn')
def notifications(request):
    profile = Profile.objects.get(user=request.user)
    
    # Use `receiver` instead of `user` to filter notifications
    notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')

    print(notifications)
    
    
    # Mark notifications as read
    notifications.update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'profile': profile
    })


@login_required(login_url='/loginn')
def check_notifications(request):
    """API to check if there are unread notifications (for the red dot and sound)"""
    unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })
