from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, ProductImage, AttributeBase, Attribute, \
    ProductAttribute
from . forms import ProductForm

import json


def cars(request):
    """ a view for the cars for sale page """
    template = 'shop/cars.html'
    context = {
        'title': 'cars for sale',
        'section': 'shop',
    }
    return render(request, template, context)


def parts(request):
    """ a view for the parts for sale page """
    products = Product.objects.filter(publish=True)
    template = 'shop/parts.html'
    context = {
        'title': 'parts for sale',
        'section': 'shop',
        'products': products,
    }
    return render(request, template, context)


def product_detail(request, product_id):
    """ a view for the product detail page """
    product = get_object_or_404(Product, pk=product_id)
    attribs = ProductAttribute.objects.filter(product=product)
    bases = []
    for attr in attribs:
        if attr.attr.base.label not in bases:
            bases.append(attr.attr.base.label)
    template = "shop/product_detail.html"
    context = {
        'title': 'product detail',
        'section': 'shop',
        'product': product,
        'bases': bases,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ a view to add a product to the shop """
    if request.user.is_staff:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            attributes = json.loads(request.POST.get('attributes'))
            files = request.FILES.getlist('image')

            if form.is_valid():
                new_product = form.save()

                for file in files:
                    img = ProductImage(image=file)
                    img.save()
                    new_product.images.add(img)

                new_product.save()

                if attributes != []:

                    for attr in attributes:
                        value = get_object_or_404(Attribute, pk=attr[0])
                        new_attr = ProductAttribute(product=new_product,
                                                    attr=value,
                                                    additional_cost=attr[1])
                        new_attr.save()

                messages.success(request, 'Your product has been added \
                    (Not Public)')
                return redirect(reverse('parts'))  # change to "PUBLISH ITEM?"
        form = ProductForm()
        attr_base = AttributeBase.objects.all()
        attrs = Attribute.objects.all()
        template = "shop/add_product.html"
        context = {
            'title': 'add product',
            'section': 'shop',
            'form': form,
            'attr_base': attr_base,
            'attrs': attrs,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required \
            permissions to complete this action")
        return redirect(reverse('parts'))


@login_required
def delete_product(request, product_id):
    """ a view to delete a product from the shop """
    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id)
        images = product.images.all()
        for image in images:
            try:
                image.delete()
            except Exception as err:
                messages.error(request, f"Error deleting image: {err}")
        try:
            product.delete()
        except Exception as err:
            messages.error(request, f"Error deleting product: {err}")
        return redirect(reverse('parts'))  # change at a later date depending on where delete button is.
    else:
        messages.warning(request, "You don't have the required \
            permissions to complete this action")
        return redirect(reverse('parts'))


@login_required
def edit_product(request, product_id):
    """ a view to edit a product """
    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=product)
            files = request.FILES.getlist('image')
            if form.is_valid():
                updated_product = form.save(commit=False)
                updated_product.publish = False
                delete_attrs = request.POST.get('attrs-delete')
                delete_list = []
                new_attrs = request.POST.get('attributes')
                new_list = []
                imgs_delete = request.POST.get('images-delete')
                img_del_list = []
                if delete_attrs:
                    delete_list = delete_attrs.split(",")
                if new_attrs:
                    new_list = new_attrs.split(",")
                if imgs_delete:
                    img_del_list = imgs_delete.split(",")
                if delete_list:
                    for attr_id in delete_list:
                        attr_item = get_object_or_404(ProductAttribute,
                                                      pk=attr_id)
                        try:
                            attr_item.delete()
                        except Exception as err:
                            messages.error(request, f"error deleting \
                                           attribute: {err}")
                if new_list:
                    for attr_w_cost in new_list:
                        attr_id = attr_w_cost.split(":")[0]
                        attr_cost = attr_w_cost.split(":")[1]
                        attr_base = get_object_or_404(Attribute,
                                                      pk=attr_id)
                        new_attribute = ProductAttribute(
                            product=product,
                            attr=attr_base,
                            additional_cost=attr_cost)
                        new_attribute.save()
                if files:
                    for file in files:
                        new_file = ProductImage(image=file)
                        new_file.save()
                        product.images.add(new_file)
                if img_del_list:
                    for img_id in img_del_list:
                        image = get_object_or_404(ProductImage, pk=img_id)
                        try:
                            image.delete()
                        except Exception as err:
                            messages.error(request, f"error deleting \
                                           image: {err}")
                updated_product.save()
                messages.success(request, "Product successfully updated")
                return redirect(reverse('parts'))   # change to "PUBLISH ITEM?"
            else:
                messages.error(request, "Form Error: Please check your \
                               form and re-submit")
                return redirect(reverse('edit_product',
                                        args={"product_id": product_id}))
        else:
            form = ProductForm(instance=product)
            product_attrs = []
            for entry in product.attributes.all():
                product_attrs.append(entry.attr.value)
            attr_base = AttributeBase.objects.all()
            attrs = Attribute.objects.all()
            template = "shop/edit_product.html"
            context = {
                'title': 'edit product',
                'section': 'shop',
                'form': form,
                'product': product,
                'attr_base': attr_base,
                'attrs': attrs,
                'product_attrs': product_attrs,
            }
            return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required \
                         permissions to complete this action")
        return redirect(reverse('parts'))
