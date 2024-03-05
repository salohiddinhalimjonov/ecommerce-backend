from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.product.models import Category
from apps.common.permissions import EditedPermissionClass
from apps.product.serializers.category import CategorySerializer, CategoryListSerializer, CategoryDetailSerializer, SubCategorySerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [EditedPermissionClass,]

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(level=1)
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        else:
            return CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get('parent')
        if isinstance(parent, Category):
            if parent.level != 1:
                return Response({'status':'Parent can not be sub category!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = Category(level=2, **serializer.validated_data)
                obj.save()
        else:
            image = serializer.validated_data.get('image')
            if not image:
                return Response({'status': 'Parent Categories must have an image!'}, status=status.HTTP_400_BAD_REQUEST)
            obj = Category(**serializer.validated_data)
            obj.save()
        serializer = CategorySerializer(obj, context={"request": self.request})

        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get('parent')
        if isinstance(parent, Category):
            if parent != 1:
                return Response({'status': 'Parent can not be sub category!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.level = 2
                instance.save()
        else:
            image = serializer.validated_data.get('image')
            if not image and not instance.image:
                return Response({'status': 'Parent Categories must have an image!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer = CategorySerializer(instance, context={"request": self.request})
        return Response({'updated_data': serializer.data}, status=status.HTTP_201_CREATED)



class SubCategoryView(ListAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(level=2)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context




