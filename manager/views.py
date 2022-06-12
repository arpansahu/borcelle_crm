from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, RedirectView, DetailView, UpdateView, DeleteView

from account.models import Account
from manager.forms import ContactsForm, ContactsModelForm
from manager.models import Contacts


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user_phone = request.GET.get('user_phone', None)
        user_name = request.GET.get('user_name', None)
        user_gst = request.GET.get('user_gst', None)
        user_email = request.GET.get('user_email', None)
        country_code = request.GET.get('country_code', None)

        contacts = request.user.contacts_set.all()

        if user_phone:
            contacts = contacts.filter(phone=user_phone)
            context['user_phone'] = user_phone
        if user_name:
            contacts = contacts.filter(name=user_name)
            context['user_name'] = user_name
        if user_phone:
            contacts = contacts.filter(gst=user_gst)
            context['user_phone'] = user_phone
        if user_email:
            contacts = contacts.filter(email=user_email)
            context['user_email'] = user_email
        if country_code:
            contacts = contacts.filter(country_code=country_code)
            context['country_code'] = country_code

        context['contacts'] = contacts
        context['room_name'] = 'broadcast'
        return render(self.request, template_name='Home.html', context=context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ContactsView(View):
    def get(self, request, *args, **kwargs):
        return redirect('home')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ContactDetailView(DetailView):
    model = Contacts
    template_name = 'contacts/contact.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = 'broadcast'
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ContactsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ContactsForm()}
        return render(request, 'contacts/contact-create.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            country_code = form.cleaned_data['country_code']
            phone = form.cleaned_data['phone']
            gst = form.cleaned_data['gst']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            contact = Contacts(name=name, country_code=country_code, phone=phone, gst=gst, email=email, address=address,
                               owner=request.user)
            contact.save()
            return HttpResponseRedirect(reverse_lazy('contact-detailed', args=[contact.id]))
        return render(request, 'contacts/contact-create.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ContactsUpdateView(UpdateView):
    template_name = 'contacts/contact-update.html'
    model = Contacts
    form_class = ContactsModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'jobs'
        return context

    def get_success_url(self):
        return reverse('contact-detailed', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ContactsDeleteView(DeleteView):
    model = Contacts
    template_name = 'contacts/contacts_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')


@login_required()
def search_gst(request):
    gst = request.GET.get('gst')
    payload = []
    if gst:
        contacts = request.user.contacts_set.all().filter(gst__icontains=gst)
        for objs in contacts:
            payload.append(objs.gst)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})


@login_required()
def search_email(request):
    email = request.GET.get('email')
    payload = []
    if email:
        contacts = request.user.contacts_set.all().filter(email__icontains=email)
        for objs in contacts:
            payload.append(objs.email)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})


@login_required()
def search_country_code(request):
    country_code = request.GET.get('country_code')
    payload = []
    if country_code:
        contacts = request.user.contacts_set.all().filter(country_code__icontains=country_code)
        for objs in contacts:
            payload.append(objs.country_code)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})


@login_required()
def search_phone(request):
    phone = request.GET.get('phone')
    payload = []
    if phone:
        contacts = request.user.contacts_set.all().filter(phone__icontains=phone)
        for objs in contacts:
            payload.append(objs.phone)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})


@login_required()
def search_name(request):
    name = request.GET.get('name')
    payload = []
    if name:
        contacts = request.user.contacts_set.all().filter(name__icontains=name)
        for objs in contacts:
            payload.append(objs.name)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})
