import google.generativeai as genai
from google.generativeai import configure
import requests
from faker import Faker
from config import Config

configure(api_key=Config.AI_API_KEY)
fake = Faker()

class Bot:
    def __init__(self, num_users=1, num_posts_per_user=1, num_comments_per_post=1, comment_type="positive"):
        self.num_users = num_users
        self.num_posts_per_user = num_posts_per_user
        self.num_comments_per_post = num_comments_per_post
        self.comment_type = comment_type

    def generate_text(self, prompt):
        my_model = genai.GenerativeModel('gemini-1.5-flash')
        response = my_model.generate_content(prompt)
        try:
            generated_text = response._result.candidates[0].content.parts[0].text
        except (AttributeError, IndexError) as e:
            raise ValueError("Unexpected response structure or no content generated") from e

        return generated_text

    def create_user(self):
        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "password"
        }
        response = requests.post(f"{Config.API_URL}/register/", json=user_data)
        response.raise_for_status()
        return user_data["username"], response.json()["id"]

    def login_user(self, username):
        login_data = {
            "username": username,
            "password": "password"
        }
        response = requests.post(f"{Config.API_URL}/login/", json=login_data)
        response.raise_for_status()
        return response.json()["access_token"]

    def create_post(self, token, user_id):
        post_data = {
            "title": fake.sentence(),
            "content": self.generate_text("Write a post about technology")
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{Config.API_URL}/posts/", json=post_data, headers=headers)
        response.raise_for_status()
        return response.json()["id"]

    def create_comment(self, token, post_id):
        comment_type_prompt = "Write a positive comment" if self.comment_type == "positive" else "Write a negative comment"
        comment_data = {
            "content": self.generate_text(comment_type_prompt)
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{Config.API_URL}/posts/{post_id}/comments/", json=comment_data, headers=headers)
        response.raise_for_status()

    def get_comments_analytics(self, date_from, date_to):
        response = requests.get(f"{Config.API_URL}/api/comments-daily-breakdown?date_from={date_from}&date_to={date_to}")
        response.raise_for_status()
        return response.json()

    def run(self):
        for _ in range(self.num_users):
            username, user_id = self.create_user()
            token = self.login_user(username)
            for _ in range(self.num_posts_per_user):
                post_id = self.create_post(token, user_id)
                for _ in range(self.num_comments_per_post):
                    self.create_comment(token, post_id)
        
        analytics = self.get_comments_analytics("2024-01-01", "2024-12-31")
        print("Comments Analytics:", analytics)

if __name__ == "__main__":
    num_users = int(input("Enter the number of users to create: "))
    num_posts_per_user = int(input("Enter the number of posts per user: "))
    num_comments_per_post = int(input("Enter the number of comments per post: "))
    comment_type = input("Enter comment type (positive/negative): ").strip().lower()

    if comment_type not in ["positive", "negative"]:
        print("Invalid comment type. Defaulting to 'positive'.")
        comment_type = "positive"

    bot = Bot(num_users=num_users, num_posts_per_user=num_posts_per_user,
              num_comments_per_post=num_comments_per_post, comment_type=comment_type)
    bot.run()
