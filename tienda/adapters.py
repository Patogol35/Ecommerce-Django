from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user

        if not user.username:
            user.username = user.email.split("@")[0]

        user.save()
        return user
