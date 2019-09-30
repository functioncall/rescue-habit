from django.contrib.auth.models import User
from blog.models import Post


class Survey:
    def __init__(self, user_id=None, user_fb_id=None):
        self.user_fb_id = user_fb_id
        self.user_id = user_id
        self.state_store = {}

    def get_instance(self):
        pass

    def set_instance(self):
        pass

    def create_survey(self, user_id):
        pass

    def send_survey(self):
        """
        Call data function for survey intent
        :return:
        """
        pass


class Scheduler:
    def __init__(self):
        self.users = self._get_users()

    @staticmethod
    def _get_users():
        return User.objects.all().distinct()

    def send_survey_to_all_users(self):
        for user in self.users:
            survey_object = Survey(user.id)
            survey_object.send_survey()

    def send_report_to_all_users(self):
        pass

    def send_weekly_report(self, user_id):
        pass

    def send_monthly_report(self, user_id):
        pass
