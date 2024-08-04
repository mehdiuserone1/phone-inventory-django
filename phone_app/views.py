from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from .forms import CreateForm, PhoneFilterForm, UpdateForm
from .models import Phone, Brand



class PhoneList(View):
    def get(self, request):
        phone_filter_form = PhoneFilterForm(request.GET or None)
        phones = Phone.objects.all()

        if phone_filter_form.is_valid():
            brand_name = phone_filter_form.cleaned_data.get('brand_name')
            brand_nation = phone_filter_form.cleaned_data.get('brand_nation')
            model_name = phone_filter_form.cleaned_data.get('model_name')
            color = phone_filter_form.cleaned_data.get('color')
            min_price = phone_filter_form.cleaned_data.get('min_price')
            max_price = phone_filter_form.cleaned_data.get('max_price')
            min_screen_size = phone_filter_form.cleaned_data.get('min_screen_size')
            max_screen_size = phone_filter_form.cleaned_data.get('max_screen_size')
            region = phone_filter_form.cleaned_data.get('region')
            inventory_status = phone_filter_form.cleaned_data.get('inventory_status')

            if brand_name:
                phones = phones.filter(brand__brand_name__icontains=brand_name)
            if brand_nation:
                phones = phones.filter(brand__brand_nation__icontains=brand_nation)
            if model_name:
                phones = phones.filter(model_name__icontains=model_name)
            if color:
                phones = phones.filter(color__icontains=color)
            if min_price is not None:
                phones = phones.filter(price__gte=min_price)
            if max_price is not None:
                phones = phones.filter(price__lte=max_price)
            if min_screen_size is not None:
                phones = phones.filter(screen_size__gte=min_screen_size)
            if max_screen_size is not None:
                phones = phones.filter(screen_size__lte=max_screen_size)
            if region:
                phones = phones.filter(region__icontains=region)
            if inventory_status:
                if inventory_status == 'available':
                    phones = phones.filter(inventory_status=True)
                elif inventory_status == 'unavailable':
                    phones = phones.filter(inventory_status=False)

        context = {
            'phone_filter_form': phone_filter_form,
            'phones': phones
        }
        return render(request, 'phone_app/phone_list.html', context)


class PhoneDetail(View):
    def get(self, request, slug):
        phone = get_object_or_404(Phone, slug=slug)
        update_form = UpdateForm(initial={
            'brand_name': phone.brand.brand_name,
            'brand_nation': phone.brand.brand_nation,
            'model_name': phone.model_name,
            'color': phone.color,
            'price': phone.price,
            'screen_size': phone.screen_size,
            'region': phone.region,
            'inventory_status': phone.inventory_status,
        })
        return render(request, 'phone_app/detail_phone.html', {'phone': phone, 'update_form': update_form})

    def post(self, request, slug):
        phone = get_object_or_404(Phone, slug=slug)
        update_form = UpdateForm()
        if 'update' in request.POST:
            update_form = UpdateForm(request.POST)
            if update_form.is_valid():
                brand_name = update_form.cleaned_data['brand_name']
                brand_nation = update_form.cleaned_data['brand_nation']
                model_name = update_form.cleaned_data['model_name']
                color = update_form.cleaned_data['color']
                price = update_form.cleaned_data['price']
                screen_size = update_form.cleaned_data['screen_size']
                region = update_form.cleaned_data['region']
                inventory_status = update_form.cleaned_data['inventory_status']

                try:
                    brand = Brand.objects.get(brand_name=brand_name)
                    if brand.brand_nation != brand_nation:
                        update_form.add_error('brand_name', 'The brand already exists with a different nationality.')
                        return render(request, 'phone_app/detail_phone.html', {'update_form': update_form, 'phone': phone})
                except Brand.DoesNotExist:
                    brand = Brand.objects.create(brand_name=brand_name, brand_nation=brand_nation)

                phone.brand = brand
                phone.model_name = model_name
                phone.color = color
                phone.price = price
                phone.screen_size = screen_size
                phone.region = region
                phone.inventory_status = inventory_status
                new_slug = slugify(f"{brand.brand_name}-{model_name}")
                if phone.slug != new_slug:
                    phone.slug = new_slug
                phone.save()
                return redirect('phone_detail', slug=phone.slug)
            return render(request, 'phone_app/detail_phone.html', {'update_form': update_form, 'phone': phone})
        elif 'delete' in request.POST:
            phone.delete()
            return redirect('phone_list')


        return render(request, 'phone_app/detail_phone.html', {'update_form': update_form, 'phone': phone})


class CreatePhone(View):
    def get(self, request):
        create_form = CreateForm()
        context = {
            'create_form': create_form
        }
        return render(request, 'phone_app/create_phone.html', context)

    def post(self, request):
        create_form = CreateForm(request.POST)
        if create_form.is_valid():
            brand_name = create_form.cleaned_data['brand_name']
            brand_nation = create_form.cleaned_data['brand_nation']
            model_name = create_form.cleaned_data['model_name']
            color = create_form.cleaned_data['color']
            price = create_form.cleaned_data['price']
            screen_size = create_form.cleaned_data['screen_size']
            region = create_form.cleaned_data['region']
            inventory_status = create_form.cleaned_data['inventory_status']

            try:

                brand = Brand.objects.get(brand_name=brand_name)
                if brand.brand_nation != brand_nation:

                    create_form.add_error('brand_name', 'The brand already exists with a different nationality.')
                    return render(request, 'phone_app/create_phone.html', {'create_form': create_form})
            except Brand.DoesNotExist:

                brand = Brand.objects.create(brand_name=brand_name, brand_nation=brand_nation)

            Phone.objects.create(
                brand=brand,
                model_name=model_name,
                color=color,
                price=price,
                screen_size=screen_size,
                region=region,
                inventory_status=inventory_status
            )

            return redirect('phone_list')
        return render(request, 'phone_app/create_phone.html', {'create_form': create_form})
