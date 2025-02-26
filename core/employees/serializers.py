from django.contrib.auth.models import User
from employees.models import Employee, EmployeeJob, EmployeeJobLevel, EmployeeJobSpecialty, EmployeeStatus
from employees.utils import generate_username
from rest_framework import serializers


class EmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeStatus
        fields = '__all__'


class EmployeeJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeJob
        fields = '__all__'


class EmployeeJobLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeJobLevel
        fields = '__all__'


class EmployeeJobSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeJobSpecialty
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    # Write-only fields for user creation
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    # Foreign keys using IDs for writing
    status = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), allow_null=True, write_only=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeJob.objects.all(), allow_null=True, write_only=True)
    position_level = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeJobLevel.objects.all(), allow_null=True, write_only=True)
    position_specialties = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeJobSpecialty.objects.all(), many=True, allow_null=True, write_only=True)

    class Meta:
        model = Employee
        fields = ('company_id', 'gender', 'status', 'position',
                  'position_level', 'position_specialties', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        # Extract user-related fields
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')

        # Extract ManyToMany field separately
        position_specialties_data = validated_data.pop(
            'position_specialties', [])

        # Generate a username (you can use a custom function if needed)
        username = generate_username(first_name)

        # Ensure unique username
        counter = 1
        base_username = username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password("welcome01")  # Default password
        user.save()

        # Create the employee and attach the user
        employee = Employee.objects.create(user=user, **validated_data)

        # Assign ManyToMany field using .set()
        employee.position_specialties.set(position_specialties_data)

        return employee

    # added def update so first_name, last_name, and email at user can also be updated
    def update(self, instance, validated_data):
        # Extract user-related fields
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)

        # Extract ManyToMany field separately
        position_specialties_data = validated_data.pop(
            'position_specialties', None)

        # Update User model fields if provided
        user = instance.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        # Update Employee model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany field
        if position_specialties_data is not None:
            instance.position_specialties.set(position_specialties_data)

        return instance

    def to_representation(self, instance):
        """Customize GET response to return nested objects instead of IDs."""
        data = super().to_representation(instance)

        # Include user details
        data['user'] = {
            "id": instance.user.id,
            "username": instance.user.username,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "email": instance.user.email
        }

        # Include nested objects for foreign keys
        data['status'] = EmployeeStatusSerializer(
            instance.status).data if instance.status else None
        data['position'] = EmployeeJobSerializer(
            instance.position).data if instance.position else None
        data['position_level'] = EmployeeJobLevelSerializer(
            instance.position_level).data if instance.position_level else None
        data['position_specialties'] = EmployeeJobSpecialtySerializer(
            instance.position_specialties.all(), many=True).data

        return data
