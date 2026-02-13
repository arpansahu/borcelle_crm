import pytest
from django.test import TestCase
from manager.models import Contact


@pytest.mark.django_db
class TestContactModel:
    """Test suite for Contact model"""
    
    def test_create_contact(self, test_user):
        """Test creating a contact"""
        contact = Contact.objects.create(
            user=test_user,
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            country_code='+1'
        )
        assert contact.name == 'John Doe'
        assert contact.email == 'john@example.com'
        assert contact.phone == '1234567890'
        assert contact.user == test_user
    
    def test_contact_str_representation(self, test_user):
        """Test the string representation of contact"""
        contact = Contact.objects.create(
            user=test_user,
            name='Jane Smith',
            email='jane@example.com'
        )
        assert str(contact) == 'Jane Smith'


@pytest.mark.django_db
class TestManagerViews:
    """Test suite for Manager views"""
    
    def test_home_view_requires_login(self, client):
        """Test that home view requires authentication"""
        response = client.get('/')
        # Should redirect to login page
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_home_view_authenticated(self, authenticated_client):
        """Test home view for authenticated user"""
        response = authenticated_client.get('/')
        assert response.status_code == 200
        assert 'Home.html' in [t.name for t in response.templates]
    
    def test_contacts_view_requires_login(self, client):
        """Test that contacts view requires authentication"""
        response = client.get('/contacts/')
        assert response.status_code == 302
    
    def test_contacts_view_authenticated(self, authenticated_client):
        """Test contacts view for authenticated user"""
        response = authenticated_client.get('/contacts/')
        assert response.status_code == 200
    
    def test_contacts_create_view_authenticated(self, authenticated_client):
        """Test contact creation view"""
        response = authenticated_client.get('/contacts/add/')
        assert response.status_code == 200
    
    def test_create_contact_post(self, authenticated_client, test_user):
        """Test creating a contact via POST"""
        data = {
            'name': 'Test Contact',
            'email': 'testcontact@example.com',
            'phone': '9876543210',
            'country_code': '+91'
        }
        response = authenticated_client.post('/contacts/add/', data)
        # Should redirect after successful creation
        assert response.status_code in [200, 302]
        # Verify contact was created
        assert Contact.objects.filter(name='Test Contact').exists()
    
    def test_contact_detail_view(self, authenticated_client, test_user):
        """Test contact detail view"""
        contact = Contact.objects.create(
            user=test_user,
            name='Detail Test',
            email='detail@example.com'
        )
        response = authenticated_client.get(f'/contacts/{contact.id}/')
        assert response.status_code == 200
    
    def test_contact_update_view(self, authenticated_client, test_user):
        """Test contact update view"""
        contact = Contact.objects.create(
            user=test_user,
            name='Update Test',
            email='update@example.com'
        )
        response = authenticated_client.get(f'/contacts/update/{contact.id}/')
        assert response.status_code == 200
    
    def test_contact_delete_view(self, authenticated_client, test_user):
        """Test contact delete view"""
        contact = Contact.objects.create(
            user=test_user,
            name='Delete Test',
            email='delete@example.com'
        )
        response = authenticated_client.post(f'/contacts/delete/{contact.id}/')
        # Should redirect after deletion
        assert response.status_code in [200, 302]
        # Verify contact was deleted
        assert not Contact.objects.filter(id=contact.id).exists()


@pytest.mark.django_db
class TestSearchFunctions:
    """Test suite for search functionality"""
    
    def test_search_name(self, authenticated_client, test_user):
        """Test name search functionality"""
        Contact.objects.create(
            user=test_user,
            name='Alice Johnson',
            email='alice@example.com'
        )
        response = authenticated_client.get('/search_name/?query=Alice')
        assert response.status_code == 200
        assert 'Alice' in str(response.content)
    
    def test_search_email(self, authenticated_client, test_user):
        """Test email search functionality"""
        Contact.objects.create(
            user=test_user,
            name='Bob Smith',
            email='bob@example.com'
        )
        response = authenticated_client.get('/search_email/?query=bob@')
        assert response.status_code == 200
    
    def test_search_phone(self, authenticated_client, test_user):
        """Test phone search functionality"""
        Contact.objects.create(
            user=test_user,
            name='Carol White',
            email='carol@example.com',
            phone='5551234567'
        )
        response = authenticated_client.get('/search_phone/?query=555')
        assert response.status_code == 200
