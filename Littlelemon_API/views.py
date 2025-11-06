from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, categorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.core.paginator import Paginator 
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.

@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menu_items(request):
    if request.method=='GET':
        items=MenuItem.objects.select_related('category').all()
        title=request.query_params.get('title')
        featured=request.query_params.get('featured')
        category=request.query_params.get('category')
        if title:
            items=items.filter(title__icontains=title)
        if featured:
            items=items.filter(featured=featured)
        if category:
            try:
                category_obj=Category.objects.get(title=category)
            except:
                return Response({"errror":"cette category est inexistante"}, status=status.HTTP_404_NOT_FOUND)
            items=items.filter(category_id=category_obj.id)
        perpage=request.query_params.get('perpage', default=2)
        page=request.query_params.get('page', default=1)
        ordering=request.query_params.get('ordering')
        if ordering:
            ordering_fields=ordering.split(',')
            items=items.objects.order_by(*ordering_fields)
        paginator=Paginator(items, per_page=perpage)
        try:
            items=paginator.page(number=page)
        except:
            items=[]
        serialized_items=MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    elif request.method=='POST':
        if request.user.groups.filter(name='Gestionnaire').exists():
            serialized_items=MenuItemSerializer(data=request.data)
            if serialized_items.is_valid():
                serialized_items.save()
                return Response(serialized_items.data, status=status.HTTP_201_CREATED)
            return Response(serialized_items.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'vous etes pas autorise a effectuer cette action'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','PUT','DELETE','PATCH'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def item_detail(request, pk):
    try:
        item=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {'error': 'Menu item not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method=='GET':
        item_serialized=MenuItemSerializer(item)
        return Response(item_serialized.data, status=status.HTTP_200_OK)
    
    if request.user.groups.filter(name='Gestionnaire').exists():
        if request.method=='PUT':
            serialized_item=MenuItemSerializer(item, data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status=status.HTTP_200_OK)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method=='PATCH':
            serialized_item=MenuItemSerializer(item, data=request.data, partial=True)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data, status=status.HTTP_200_OK)
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method=='DELETE':
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {'error': 'Vous n\'êtes pas autorisé à effectuer cette action'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    

@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def managers(request):
    if request.user.groups.filter(name='Gestionnaire').exists():
        try: 
            groupe_manager=Group.objects.get(name='Gestionnaire')
        except Group.DoesNotExist:
            return Response({'error':'Le groupe Gestionnaire nexiste pas.'}, status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            user=User.objects.filter(groups=groupe_manager)
            userSerialized=UserSerializer(user, many=True)
            return Response(userSerialized.data, status=status.HTTP_200_OK)
        elif request.method=='POST':
            userSerialized=UserSerializer(data=request.data)
            if userSerialized.is_valid():
                user=userSerialized.save()
                user.groups.add(groupe_manager)
            return Response(userSerialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {'error': 'Vous n\'êtes pas autorisé à effectuer cette action'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def deliverys(request):
    if request.user.groups.filter(name='Gestionnaire').exists():
        try: 
            groupe_delivery=Group.objects.get(name='Livreur')
        except Group.DoesNotExist:
            return Response({'error':'Le groupe livreur nexiste pas.'}, status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            user=User.objects.filter(groups=groupe_delivery)
            userSerialized=UserSerializer(user, many=True)
            return Response(userSerialized.data, status=status.HTTP_200_OK)
        elif request.method=='POST':
            userSerialized=UserSerializer(data=request.data)
            if userSerialized.is_valid():
                user=userSerialized.save()
                user.groups.add(groupe_delivery)
            return Response(userSerialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {'error': 'Vous n\'êtes pas autorisé à effectuer cette action'}, 
            status=status.HTTP_403_FORBIDDEN
        )

@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def manager(request, pk):
    try:
        groupe_manager=Group.objects.get(name='Gestionnaire')
        user=User.objects.get(pk=pk, groups=groupe_manager)
    except:
        return Response({'error': "utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)
    user.delete()  
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def delivery(request, pk):
    try:
        groupe_delivery=Group.objects.get(name='Livreur')
        user=User.objects.get(pk=pk, groups=groupe_delivery)
    except:
        return Response({'error': "utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)
    user.delete()  
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE','POST','GET'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def cart(request):
    if request.method=='POST':
        users=request.user
        menu_items_id=request.data.get('menuitem')
        quantity=request.data.get('quantity')
        quantity=int(quantity)
        if not menu_items_id or not quantity:
            return Response({'error': 'les champs menuitem et quantity sont obligatoires.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            menu_item=MenuItem.objects.get(pk=menu_items_id)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)
        cart, created=Cart.objects.get_or_create(
            user=users,
            menuitem=menu_item,
            defaults={
                'quantity': quantity,
                'unit_price': menu_item.price,
            }
        )
        cartSerialized=CartSerializer(cart)
        return Response(cartSerialized.data, status=status.HTTP_201_CREATED)
    if request.method=='GET':
        user=request.user
        cartitems=Cart.objects.filter(user=user)
        cartSerialized=CartSerializer(cartitems, many=True)
        return Response(cartSerialized.data, status=status.HTTP_200_OK)
    if request.method=='DELETE':
        user=request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def orders(request):
    if request.method=='GET':
        if request.user.groups.filter(name='Gestionnaire').exists():
            order=Order.objects.all()
            orderSerialized=OrderSerializer(order, many=True)
            return Response(orderSerialized.data, status=status.HTTP_200_OK)
        else:
            users=request.user
            order=Order.objects.filter(user=users)
            orderSerialized=OrderSerializer(order, many=True)
            return Response(orderSerialized.data, status=status.HTTP_200_OK)
    if request.method=='POST':

        user = request.user
        items = Cart.objects.filter(user=user)

        if not items.exists():
            return Response({'error': 'Le panier est vide.'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.unit_price * item.quantity for item in items)

        delivery_crew = None
        delivery_id = request.data.get('delivery_crew')
        if delivery_id:
            try:
                delivery_user = User.objects.get(pk=delivery_id, groups__name='Livreur')
                delivery_crew = delivery_user
            except User.DoesNotExist:
                return Response({'error': 'Livreur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            user=user,
            delivery_crew=delivery_crew,
            status=False,
            total=total,
            date=date.today()
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
        items.delete()

    
        order_serialized = OrderSerializer(order)
        return Response(order_serialized.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','PATCH','DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_detail(request, pk):
    if request.method=='GET':
        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error':'cette commande est inexistante.'}, status=status.HTTP_404_NOT_FOUND)
        order_item=OrderItem.objects.filter(order=order)
        order_item_serialized=OrderItemSerializer(order_item, many=True)
        return Response(order_item_serialized.data, status=status.HTTP_200_OK)
    if request.method=='PUT':
        order=Order.objects.get(pk=pk)
        order_serialized=OrderSerializer(order, data=request.data)
        if order_serialized.is_valid():
            order_serialized.save()
            return Response(order_serialized.data, status=status.HTTP_200_OK)
        return Response(order_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method=='PATCH':
        if request.user.groups.filter(name='Livreur').exists():
            try:
                order=Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                return Response({'error':'cette commande est inexistante.'}, status=status.HTTP_404_NOT_FOUND)
            status_value=request.data.get('status')
            if status_value is None:
                return Response({'error':'le champ status est obligatoire.'}, status=status.HTTP_400_BAD_REQUEST)
            order.status=status_value
            order.save()
            order_serialized=OrderSerializer(order)
            return Response(order_serialized.data, status=status.HTTP_200_OK)
        else:
            order=Order.objects.get(pk=pk)
            # correction: partial (typo corrected)
            order_serialized=OrderSerializer(order, data=request.data, partial=True)
            if order_serialized.is_valid():
                order_serialized.save()
                return Response(order_serialized.data, status=status.HTTP_200_OK)
            return Response(order_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method=='DELETE':
        order=Order.objects.get(pk=pk)
        order_items=OrderItem.objects.filter(order=order)
        order_items.delete()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    