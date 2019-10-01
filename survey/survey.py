import json
import operator
import os

from blog.models import Post, SurveyHistory


class Survey:
    def __init__(self, user_id=None, user_fb_id=None):
        """

        :param user_id: passed from internal else derived from user_fb_id
        :param user_fb_id:
        """
        self.user_id = "1" if user_fb_id == "2140353912711652" else user_id
        self.user_fb_id = user_fb_id
        self.posts = Post.objects.filter(author__id=self.user_id)
        self.survey_json_path = '/Users/shekhar/Documents/workspace/django-blog/django_project/survey/survey_state.json'
        self.survey_state = self._get_survey_state()

    def _get_survey_state(self):
        if os.path.exists(self.survey_json_path):
            with open(self.survey_json_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def is_active(self):
        if os.path.exists(self.survey_json_path):
            with open(self.survey_json_path, 'r') as f:
                if f.read() != "{}":
                    return True
                else:
                    return False
        else:
            return False

    def create_survey(self):
        for post in self.posts:
            if self.survey_state != {} and self.user_id in self.survey_state.keys():
                self.survey_state[self.user_id][post.id] = 0
            else:
                self.survey_state[self.user_id] = {post.id: 0}

        with open(self.survey_json_path, 'w') as f:
            json.dump(self.survey_state, f)

    def get_current_instance(self):
        """
        Call data function for survey intent
        :return:
        """
        # send the current survey question
        try:
            posts = self.survey_state.get(self.user_id)
            for post_id, is_marked in sorted(posts.items(), key=operator.itemgetter(1)):
                print("post: ", post_id, is_marked)
                first_result = Post.objects.filter(id=post_id).first()
                print("first_result: ",first_result)
                if first_result is not None:
                    return {
                        "post_id": post_id,
                        "post": first_result.title
                    }
                else:
                    return None
        except KeyError:
            return None

    def store_survey_response(self, post_id, post_response):
        post = Post.objects.filter(id=post_id).first()
        sh = SurveyHistory.objects.create(post=post, record=post_response)
        sh.save()
        del self.survey_state[self.user_id][post_id]
        print("survey_state: ", self.survey_state)
        with open(self.survey_json_path, 'w') as f:
            json.dump(self.survey_state, f)

    def clear_survey_state(self):
        if os.path.exists(self.survey_json_path):
            os.remove(self.survey_json_path)
            self.survey_state = {}
        else:
            print("Path does not exists")
