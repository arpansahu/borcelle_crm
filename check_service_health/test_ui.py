# check_service_health/test_ui.py
"""
UI tests for Borcelle CRM using Playwright
Tests run against a Django server that should be already running
"""

import pytest
from playwright.sync_api import Page, expect
import time
import os


# Configuration
BASE_URL = os.getenv("TEST_SERVER_URL", "http://127.0.0.1:8000")  # Django test server
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_USERNAME = "testuser"
TEST_USER_PASSWORD = "TestPass123!"


@pytest.fixture(scope="module")
def browser_context_args(browser_context_args):
    """Configure browser context for all tests"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


class TestPublicPages:
    """Test public pages that don't require authentication"""
    
    def test_homepage_redirects_to_login(self, page: Page):
        """Test that the homepage redirects to login when not authenticated"""
        page.goto(BASE_URL)
        # Should redirect to login page
        page.wait_for_url(f"{BASE_URL}/login/*", timeout=10000)
        expect(page).to_have_title("Sign IN")
        
    def test_login_page_loads(self, page: Page):
        """Test that the login page loads and has correct elements"""
        page.goto(f"{BASE_URL}/login/")
        expect(page).to_have_title("Sign IN")
        
        # Check for login form elements
        expect(page.locator('input[name="username"]')).to_be_visible()
        expect(page.locator('input[name="password"]')).to_be_visible()
        expect(page.locator('button[type="submit"]')).to_be_visible()
    
    def test_register_page_loads(self, page: Page):
        """Test that the registration page loads"""
        page.goto(f"{BASE_URL}/register/")
        expect(page).to_have_title("Sign UP")
        
        # Check for registration form (uses password1 and password2 from UserCreationForm)
        expect(page.locator('input[name="email"]')).to_be_visible()
        expect(page.locator('input[name="username"]')).to_be_visible()
        expect(page.locator('input[name="password1"]')).to_be_visible()


class TestAuthentication:
    """Test authentication flows"""
    
    def test_login_with_valid_credentials(self, page: Page):
        """Test logging in with valid credentials"""
        page.goto(f"{BASE_URL}/login/")
        
        # Form field is 'username' but expects email value
        page.fill('input[name="username"]', TEST_USER_EMAIL)
        page.fill('input[name="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        
        # Wait for redirect and check if logged in
        page.wait_for_url(f"{BASE_URL}/", timeout=10000)
        
    def test_login_with_invalid_credentials(self, page: Page):
        """Test logging in with invalid credentials"""
        page.goto(f"{BASE_URL}/login/")
        
        page.fill('input[name="username"]', "wronguser")
        page.fill('input[name="password"]', "wrongpassword")
        page.click('button[type="submit"]')
        
        # Should show error message
        time.sleep(1)
        assert "login" in page.url.lower()


class TestAuthenticatedPages:
    """Test pages that require authentication"""
    
    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Login before each test in this class"""
        page.goto(f"{BASE_URL}/login/")
        # Form field is 'username' but expects email value
        page.fill('input[name="username"]', TEST_USER_EMAIL)
        page.fill('input[name="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_url(f"{BASE_URL}/", timeout=10000)
    
    def test_dashboard_loads(self, page: Page):
        """Test that dashboard loads after login"""
        page.goto(f"{BASE_URL}/")
        # Check for dashboard elements
        assert "Borcelle CRM" in page.title()
    
    def test_contacts_page_loads(self, page: Page):
        """Test contacts page redirects to home (ContactsView redirects)"""
        page.goto(f"{BASE_URL}/contact/")
        # ContactsView redirects to home
        page.wait_for_url(f"{BASE_URL}/", timeout=10000)
        expect(page).to_have_url(f"{BASE_URL}/")
    
    def test_add_contact_page_loads(self, page: Page):
        """Test add contact page loads"""
        page.goto(f"{BASE_URL}/contact/add/")
        
        # Check for form fields
        expect(page.locator('input[name="name"]')).to_be_visible()
        expect(page.locator('input[name="email"]')).to_be_visible()
    
    def test_account_page_loads(self, page: Page):
        """Test account page loads"""
        page.goto(f"{BASE_URL}/account/")
        expect(page).to_have_url(f"{BASE_URL}/account/")
    
    def test_logout(self, page: Page):
        """Test logout functionality"""
        page.goto(f"{BASE_URL}/logout/")
        time.sleep(1)
        
        # Should redirect to login page
        page.goto(f"{BASE_URL}/")
        page.wait_for_url(f"{BASE_URL}/login/*", timeout=10000)


class TestResponsiveness:
    """Test responsive design"""
    
    def test_mobile_viewport(self, page: Page):
        """Test site on mobile viewport"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{BASE_URL}/login/")
        
        # Check if page renders correctly
        expect(page.locator('input[name="username"]')).to_be_visible()
    
    def test_tablet_viewport(self, page: Page):
        """Test site on tablet viewport"""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(f"{BASE_URL}/login/")
        
        # Check if page renders correctly
        expect(page.locator('input[name="username"]')).to_be_visible()
