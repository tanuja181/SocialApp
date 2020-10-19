from django.shortcuts import render
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post
from accounts.models import CustomUser,ConnectionReuest,Connections
import datetime

def home(request):
    queryset = Post.objects.all()

    context = {

        "post_list": queryset
    }
    return render(request, "index.html", context)





@login_required
def add_post(request):
    posted = False
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            my_post = post_form.save(commit=False)
            my_post.author = request.user
            my_post.published_date = timezone.now()
            if 'post_image' in request.FILES:
                print('found post image')
                my_post.post_image = request.FILES['post_image']
            my_post.save()
            posted = True
        else:
            print(post_form.errors)
    else:
        post_form = PostForm()
    return render(request,'index.html',
                          {'post_form':post_form, 'posted':posted})


@login_required
def search_users(request):
	query = request.GET.get('q')
	object_list = CustomUser.objects.filter(username__icontains=query).filter(email__icontains=query).filter(phone__icontains=query)
	context ={
		'users': object_list
	}


	return render(request, "features/search_users.html", context)


@login_required
def user_profile_view(request, slug):
	p = Connections.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = ConnectionReuest.objects.filter(from_user=p.user)
	rec_friend_requests = ConnectionReuest.objects.filter(to_user=p.user)
	user_posts = Post.objects.filter(user_name=u)

	connections = p.connections.all()

	# is this in user our connection
	button_status = 'none'
	if p not in request.user.connections.connections.all():
		button_status = 'not_connected'

		# if we have sent him a connection request
		if len(ConnectionReuest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'connection_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'total_connections': connections,

		'sent_connections_requests': sent_friend_requests,
		'recieve_connection_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "features/user-profile.html", context)

# @login_required
# def connection_profile_view(request,slug):
#     p = Connections.objects.filter(slug=slug).first()
#     connections = p.connections.all()
#



