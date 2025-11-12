from django.test import TestCase
from django.urls import reverse
from apps.menu.models import MenuItem
from apps.menu.views import MenuTreeView


class MenuItemModelTests(TestCase):
    def setUp(self):
        self.root = MenuItem.objects.create(title="Главная", url="/")
        self.about = MenuItem.objects.create(title="О нас", url="/about/")
        self.team = MenuItem.objects.create(
            title="Команда", url="/about/team/", parent=self.about
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.root), "Главная")

    def test_parent_relationship(self):
        self.assertEqual(self.team.parent, self.about)
        self.assertIn(self.team, self.about.children.all())

    def test_children_related_name(self):
        children = self.about.children.all()
        self.assertEqual(children.count(), 1)
        self.assertEqual(children.first().title, "Команда")

    def test_no_parent_items_filter(self):
        top_level = MenuItem.objects.filter(parent__isnull=True)
        titles = [item.title for item in top_level]
        self.assertIn("Главная", titles)
        self.assertIn("О нас", titles)
        self.assertNotIn("Команда", titles)


class MenuTreeViewTests(TestCase):
    def setUp(self):
        self.root1 = MenuItem.objects.create(title="Главная", url="/")
        self.root2 = MenuItem.objects.create(title="О нас", url="/about/")
        self.child = MenuItem.objects.create(
            title="Команда", url="/about/team/", parent=self.root2
        )

    def test_view_class_used(self):
        self.assertTrue(issubclass(MenuTreeView, object))

    def test_view_context_contains_top_level_items(self):
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("menu_items", response.context)
        menu_items = response.context["menu_items"]
        self.assertEqual(menu_items.count(), 2)
        self.assertTrue(all(item.parent is None for item in menu_items))

    def test_view_prefetch_children(self):
        response = self.client.get(reverse("menu-list"))
        menu_items = list(response.context["menu_items"])
        about = next((m for m in menu_items if m.title == "О нас"), None)
        self.assertIsNotNone(about)
        self.assertTrue(about.children.filter(title="Команда").exists())
