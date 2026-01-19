from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Q

from .models import LostItem
from .forms import LostItemForm, RegisterForm
from .utils import distance_km
from .models import ChatRoom, ChatMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatRoom, ChatMessage, Notification


# ================= HOME PAGE =================
def home(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    lost_items = LostItem.objects.all().order_by("-lost_date")

    # 🔍 SEARCH FILTER (title + location)
    if query:
        lost_items = lost_items.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )

    # 🏷 STATUS FILTER
    if status == "lost":
        lost_items = lost_items.filter(found=False)
    elif status == "found":
        lost_items = lost_items.filter(found=True)

    # 📍 LOCATION FILTER (5 km radius)
    if lat and lng:
        lat = float(lat)
        lng = float(lng)
        nearby_items = []

        for item in lost_items:
            if item.latitude and item.longitude:
                dist = distance_km(lat, lng, item.latitude, item.longitude)
                if dist <= 5:
                    item.distance = round(dist, 2)
                    nearby_items.append(item)

        lost_items = nearby_items

    return render(request, "findme/home.html", {
        "lost_items": lost_items,
        "query": query,
        "status": status,
    })


# ================= POST LOST ITEM =================
@login_required
def post_item(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect("home")
    else:
        form = LostItemForm()

    return render(request, "findme/add_item.html", {"form": form})


# ================= REGISTER =================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "findme/register.html", {"form": form})


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("home")
# ================= CHAT FUNCTIONALITY =================
# Chat room initiation view
@login_required
def start_chat(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)

    if request.user == item.owner:
        return redirect('home')

    room, created = ChatRoom.objects.get_or_create(
        item=item,
        user1=item.owner,
        user2=request.user
    )
    return redirect('chat_room', room_id=room.id)
# Chat room view
@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.user not in [room.user1, room.user2]:
        return redirect("home")

    Notification.objects.filter(
        receiver=request.user,
        link=f"/chat/{room_id}/",
        is_read=False
    ).update(is_read=True)

    messages = ChatMessage.objects.filter(
        room=room
    ).order_by("created_at")

    if request.method == "POST":
        msg = request.POST.get("message")

        if msg:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=msg
            )

        return redirect("chat_room", room_id=room.id)

    # ⚠️ THIS MUST BE OUTSIDE ALL IF BLOCKS
    return render(request, "chat/chat_room.html", {
        "room": room,
        "messages": messages,
    })


# Show notifications to owner
@login_required
def notifications(request):
    notes = Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).order_by('-created_at')

    return render(request, "findme/notifications.html", {
        "notifications": notes
    })