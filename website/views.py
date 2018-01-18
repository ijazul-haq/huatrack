from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ArtworkForm, ProfileForm, ArtworkTransferForm
from .models import UserProfile, Artwork, User
import time
import datetime
# import hashlib
import bigchaindb_driver
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json
from time import sleep
from django.http import JsonResponse
from bigchaindb_driver.exceptions import NotFoundError


def index(request):
    data = {'artworks': ''}
    return render(request, 'website/index.html', data)


def gallery(request):
    data = {'artworks': 'artworks'}
    return render(request, 'website/gallery.html', data)


@login_required
def profile(request):
    user = request.user
    data = {
        'user': user,
    }
    return render(request, 'user/profile.html', data)


@login_required
def collection(request):
    public_key = request.user.userprofile.public_key
    collection = Artwork.objects.filter(artist=public_key)

    data = {
        'collection': collection,
    }
    return render(request, 'user/collection.html', data)


@login_required
def artwork_detail(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    data = {
        'artwork': artwork,
    }
    return render(request, 'user/artwork_detail.html', data)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('../collection')
            else:
                return HttpResponse('account is not active')
        else:
            return render(request, 'user/login.html', {'form_errors': 'User not exist'})
    else:
        return render(request, 'user/login.html')


@login_required
def log_out(request):
    logout(request)
    return redirect('../website/user_login')


def user_reg(request):
    user_form = UserForm
    profile_form = ProfileForm

    data = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        data['user_form'] = user_form
        data['profile_form'] = profile_form

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            keys = generate_keypair()
            profile.public_key = keys.public_key
            profile.private_key = keys.private_key
            profile.save()

            return redirect('../user_login')
        else:
            data['form_errors'] = 'Invalid Form'
            return render(request, 'user/register.html', data)
    else:
        return render(request, 'user/register.html', data)


@login_required()
def artwork_reg(request):
    form = ArtworkForm

    data = {
        'form': form,
    }

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        data['form'] = form

        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.timestamp = datetime.datetime.now()
            artwork.artist = request.user.userprofile.public_key
            artwork.status = 'pending'
            artwork.save()
            return redirect('../collection')
        else:
            print(form.errors)
            data['form_errors'] = 'Invalid Form'
            return render(request, 'user/artwork_form.html', data)
    else:
        return render(request, 'user/artwork_form.html', data)


@login_required()
def asset_create(request, artwork_id):
    tokens = {'app_id': '186018c8', 'app_key': 'd317b3d1bb45c984d817c498770c47c0'}
    bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)

    data = {
        'status': False
    }
    user_public_key = request.user.userprofile.public_key
    user_private_key = request.user.userprofile.private_key

    artwork = Artwork.objects.filter(id=artwork_id)
    for art in artwork:
        art_title = art.title
        art_created = art.created
        art_hash = art.hash
        art_path = art.path.url

    art = {
        'data': {
            'art': {
                'title': art_title,
                'created': art_created,
                'timestamp': time.time(),
                'hash': art_hash,
                'path': art_path,
            },
        },
    }
    metadata = {'Developer': 'Engr. Ijazul Haq'}
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user_public_key,
        asset=art,
        metadata=metadata,
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=user_private_key,
    )
    
    bdb.transactions.send(fulfilled_creation_tx)

    txid = fulfilled_creation_tx['id']

    trials = 0

    while trials < 100:
        try:
            if bdb.transactions.status(txid).get('status') == 'valid':
                break
        except bigchaindb_driver.exceptions.NotFoundError:
            trials += 1
    tx_status = bdb.transactions.status(txid)

    if tx_status == 'valid':
        artwork.status = 'registered'
        artwork.save()
        data['status'] = 'valid'
    else:
        data['status'] = 'invalid'

    return JsonResponse(data)


@login_required()
def asset_transfer(request, artwork_id):
    data = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        txid = request.POST.get('txid')
        new_owner = User.objects.filter(email=email)
        if new_owner.count() == 1:
            for n in new_owner:
                new_owner_public_key = n.userprofile.public_key
                old_owner_private_key = request.user.userprofile.private_key
                old_owner_public_key = request.user.userprofile.public_key

                if new_owner_public_key == request.user.userprofile.public_key:
                    data['errors'] = 'You cannot transfer to yourself'
                    return render(request, 'user/collection.html', data)
                else:
                    tokens = {'app_id': '186018c8', 'app_key': 'd317b3d1bb45c984d817c498770c47c0'}
                    bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
                    asset = bdb.transactions.retrieve(txid)
                    print(old_owner_public_key)
                    print('\n')
                    print(asset['inputs'][0]['owners_before'][0])
                    if asset:
                        if old_owner_public_key != asset['inputs'][0]['owners_before'][0]:
                            data['errors'] = 'Sorry! this Artwork is not yours'
                        else:
                            transfer_asset = {
                                'id': asset['id']
                            }
                            output_index = 0
                            output = asset['outputs'][output_index]

                            transfer_input = {
                                'fulfillment':
                                    output['condition']['details'],
                                'fulfills': {
                                    'output_index': output_index,
                                    'transaction_id': asset['id'],
                                    },
                                'owners_before': output['public_keys'],
                            }
                            prepared_transfer_tx = bdb.transactions.prepare(
                                operation='TRANSFER',
                                asset=transfer_asset,
                                inputs=transfer_input,
                                recipients=new_owner_public_key,
                            )
                            fulfilled_transfer_tx = bdb.transactions.fulfill(
                                prepared_transfer_tx,
                                private_keys=old_owner_private_key,
                            )
                            sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)
                            new_owner_public_key = sent_transfer_tx['outputs'][0]['public_keys'][0]
                            data['new_owner']=new_owner_public_key
                            return JsonResponse(data)
                    else:
                        data['errors'] = 'Asset not found on Blockchain'
        else:
            data['errors'] = 'Recipient not found'
    else:
        data['errors'] = 'Request time out, try again'
    return render(request, 'user/collection.html', data)


@login_required()
def asset_get(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    status = False
    tokens = {'app_id': '186018c8', 'app_key': 'd317b3d1bb45c984d817c498770c47c0'}
    bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)

    if artwork.txid:
        status = bdb.transactions.status(artwork.txid)

    data = {
        'status': status,
    }
    return JsonResponse(data)
