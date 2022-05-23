from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User

from cjapp.settings import logger_factory

file_name = "logfile2.log"
logs = logger_factory()
logger = logs.create(file_name,logging.DEBUG)
from restapi.models import Category, Groups, UserExpense, Expenses


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        logger.info("an user is created")
        return user

    class Meta(object):
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CategorySerializer(ModelSerializer):
    class Meta(object):
        model = Category
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    members = UserSerializer(many=True, required=False)

    class Meta(object):
        model = Groups
        fields = '__all__'


class UserExpenseSerializer(ModelSerializer):
    class Meta(object):
        model = UserExpense
        fields = ['user', 'amount_owed', 'amount_lent']


class ExpensesSerializer(ModelSerializer):
    users = UserExpenseSerializer(many=True, required=True)

    def create(self, validated_data):
        expense_users = validated_data.pop('users')
        expense = Expenses.objects.create(**validated_data)
        logger.info("an expense is created by user :" +str(validated_data.user))
        for eu in expense_users:
            UserExpense.objects.create(expense=expense, **eu)
        return expense

    def update(self, instance, validated_data):
        user_expenses = validated_data.pop('users')
        instance.description = validated_data['description']
        instance.category = validated_data['category']
        instance.group = validated_data.get('group', None)
        instance.total_amount = validated_data['total_amount']


        if user_expenses:
            instance.users.all().delete()
            UserExpense.objects.bulk_create(
                [
                    user_expense(expense=instance, **user_expense)
                    for user_expense in user_expenses
                ],
            )
        
        instance.save()
        logger.info("expense is updated successfully")

        

        return instance

    def validate(self, attrs):
        # user = self.context['request'].user
        user_ids = [user['user'].id for user in attrs['users']]
        if len(set(user_ids)) != len(user_ids):
            logger.error("Single user appears multiple times")
            raise ValidationError('Single user appears multiple times')

        return attrs

    class Meta(object):
        model = Expenses
        fields = '__all__'
