from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


class UserTypeRequiredMixin(AccessMixin):
    required_user_type = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != self.required_user_type:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class ProfileExistsMixin(LoginRequiredMixin):
    profile_attr = None
    redirect_to = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            getattr(request.user, self.profile_attr)
        except ObjectDoesNotExist:
            return redirect(self.redirect_to)
        return super().dispatch(request, *args, **kwargs)


class ProfileGetObjectMixin(LoginRequiredMixin):
    profile_attr = None
    redirect_to = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.object = getattr(request.user, self.profile_attr)
        except ObjectDoesNotExist:
            return redirect(self.redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object
