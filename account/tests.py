import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Account

User = get_user_model()


@pytest.mark.django_db
class TestAccountModel:
    """Test suite for Account model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        assert admin_user.username == 'admin'
        assert admin_user.email == 'admin@example.com'
        assert admin_user.is_staff
        assert admin_user.is_superuser
        assert admin_user.is_active
    
    def test_user_str_representation(self, test_user):
        """Test the string representation of user"""
        assert str(test_user) == test_user.username


@pytest.mark.django_db
class TestAccountViews:
    """Test suite for Account views"""
    
    def test_registration_view_get(self, client):
        """Test registration page loads correctly"""
        response = client.get('/register/')
        assert response.status_code == 200
        assert 'account/register.html' in [t.name for t in response.templates]
    
    def test_login_view_get(self, client):
        """Test login page loads correctly"""
        response = client.get('/login/')
        assert response.status_code == 200
        assert 'registration/login.html' in [t.name for t in response.templates]
    
    def test_login_with_valid_credentials(self, client, test_user, test_password):
        """Test login with valid credentials"""
        response = client.post('/login/', {
            'username': test_user.username,
            'password': test_password
        })
        # Should redirect after successful login
        assert response.status_code in [200, 302]
    
    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/login/', {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        assert response.status_code == 200  # Stays on login page
    
    def test_logout(self, authenticated_client):
        """Test logout functionality"""
        response = authenticated_client.get('/logout/')
        assert response.status_code in [200, 302]
    
    def test_account_view_requires_login(self, client):
        """Test that account view requires authentication"""
        response = client.get('/account/')
        # Should redirect to login page
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_account_view_authenticated(self, authenticated_client):
        """Test account view for authenticated user"""
        response = authenticated_client.get('/account/')
        assert response.status_code == 200
