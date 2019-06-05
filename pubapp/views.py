from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
import random

# Create your views here.
from pubapp.forms import UserForm, CharacterForm
from pubapp.models import Character, CharacterUser, StaticImage, CharacterBio
from pubapp.utils import update_or_create_user_character_relations

IMAGE_FILE_TYPES = ['png', 'jpg', 'bmp', 'jpeg']


def suggestion_list_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    page_options = {'is_error': False, 'error_message': '', 'is_success': False, 'success_message': ''}
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            if 'image' not in request.FILES:
                page_options['is_error'] = True
                page_options['error_message'] = 'Invalid Image!'
            else:
                static_image = StaticImage()
                static_image.file = request.FILES['image']
                static_image.name = static_image.file.url.split('.')[0].split('/')[-1]
                file_type = static_image.file.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    page_options['is_error'] = True
                    page_options['error_message'] = 'Invalid Image Type!'
                else:
                    static_image.save()
                    character.image = static_image
                    character.save()
                    page_options['is_success'] = True
                    page_options['success_message'] = 'The character is pending approval!'
    return render(request, 'pub_character_suggest.html', page_options)


def characters_list_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    character_filtered = []
    characters = Character.objects.filter(is_approved=True).all()
    for character in characters:
        relation = CharacterUser.objects.filter(user=request.user, character=character, drinks__gte=1).first()
        if relation is not None:
            character_filtered.append(character)

    return render(request, 'pub_characters_list.html', {'characters': character_filtered})


def character_view(request, character_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    character = Character.objects.filter(is_approved=True, id=character_id).first()

    if character is None:
        return HttpResponseNotFound()

    relation = CharacterUser.objects.filter(user=request.user, character=character).first()
    bio = None

    if relation.drinks == 1:
        bio = CharacterBio.objects.filter(character=character, bioType="T1").first()
    elif relation.drinks == 2:
        bio = CharacterBio.objects.filter(character=character, bioType="T2").first()
    elif relation.drinks >= 3:
        bio = CharacterBio.objects.filter(character=character, bioType="T3").first()

    if bio is None:
        return HttpResponseNotFound()
    return render(request, 'pub_character.html', {'character': character, 'bio': bio})


def pub_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == "POST":
        character_id = int(request.POST['pub_button'])
        if character_id is None:
            return HttpResponseNotFound()
        relation = CharacterUser.objects.filter(user=request.user, character__pk=character_id,
                                                character__is_approved=True).first()
        relation.drinks += 1
        relation.save()
        return redirect('/pub/characters/' + str(character_id))
    characters = Character.objects.filter(is_approved=True).all()
    random_characters = random.sample(list(characters), 3) if characters.count() > 0 else []
    return render(request, 'pub.html', {'random_characters': random_characters})


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    return render(request, 'index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    page_options = {'createAccount': False, 'isError': False}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        page_options['isError'] = True
        page_options['errorMessage'] = "Wrong username/password ... faggot"

    return render(request, 'accounts_handler.html', page_options)


def logout_command(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/accounts/login/')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    page_options = {'createAccount': True, 'isError': False}

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                update_or_create_user_character_relations(user)
                if user.is_active:
                    login(request, user)
                    return redirect('/')
            page_options['isError'] = True
            page_options['errorMessage'] = "Invalid username/password..."

    return render(request, 'accounts_handler.html', page_options)


def refresh_relationship_content_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.user.is_superuser:
        users = User.objects.all()
        for user in users:
            update_or_create_user_character_relations(user)

    return HttpResponse("<h1>Users Character Relations Updated</h1>")
