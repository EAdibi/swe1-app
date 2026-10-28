import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    """Create a question published `days` offset from now (negative = past)."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        q = create_question("Recent?", days=0)
        self.assertIs(q.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        q = create_question("Old?", days=-2)
        self.assertIs(q.was_published_recently(), False)

    def test_str_methods(self):
        q = create_question("What's new?", days=0)
        c = Choice.objects.create(question=q, choice_text="Not much")
        self.assertEqual(str(q), "What's new?")
        self.assertEqual(str(c), "Not much")


class IndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_lists_question(self):
        q = create_question("Listed question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q])


class DetailAndResultsViewTests(TestCase):
    def test_detail_shows_question(self):
        q = create_question("Detail question", days=-1)
        response = self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertContains(response, q.question_text)

    def test_results_page_loads(self):
        q = create_question("Results question", days=-1)
        response = self.client.get(reverse("polls:results", args=(q.id,)))
        self.assertEqual(response.status_code, 200)


class VoteViewTests(TestCase):
    def setUp(self):
        self.question = create_question("Vote?", days=-1)
        self.choice = Choice.objects.create(question=self.question, choice_text="Yes")

    def test_vote_increments_and_redirects(self):
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.post(url, {"choice": self.choice.id})
        self.assertRedirects(
            response, reverse("polls:results", args=(self.question.id,))
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_without_choice_shows_error(self):
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.post(url, {})
        self.assertContains(response, "You didn&#x27;t select a choice.")
