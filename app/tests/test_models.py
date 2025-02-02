from django.test import TestCase
from app.models import MyModel

class MyModelTestCase(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.instance = MyModel.objects.create(name="Test Name", age=25)

    def test_instance_creation(self):
        """Test if the instance is created correctly."""
        self.assertEqual(self.instance.name, "Test Name")
        self.assertEqual(self.instance.age, 25)

    def test_instance_str(self):
        """Test the __str__ method of the model."""
        self.assertEqual(str(self.instance), "Test Name")
