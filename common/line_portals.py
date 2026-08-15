"""Reusable list + add-only portal views (no edit/delete in app)."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse


def make_portal_list_view(*, queryset_fn, headers, row_builder, title, add_url_name, base_template):
    @login_required(login_url="login_user")
    def view(request):
        qs = queryset_fn()[:500]
        rows = [row_builder(o) for o in qs]
        ctx = {
            "base_template": base_template,
            "title": title,
            "headers": headers,
            "rows": rows,
            "add_url_name": add_url_name,
        }
        return render(request, "line_portal/list.html", ctx)

    return view


def make_portal_add_view(*, Form, redirect_url_name, base_template, title):
    @login_required(login_url="login_user")
    def view(request):
        if request.method == "POST":
            form = Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Saved.")
                return redirect(redirect_url_name)
        else:
            form = Form()
        ctx = {
            "base_template": base_template,
            "title": title,
            "form": form,
            "cancel_url_name": redirect_url_name,
        }
        return render(request, "line_portal/form.html", ctx)

    return view
