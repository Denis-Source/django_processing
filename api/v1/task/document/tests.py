import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from api.tests import BaseAPITestCase
from task.document.constants import INPUT_FORMATS, OUTPUT_FORMATS
from task.models import Task, DocumentConversionTask


class RetrieveDocumentFormatsViewTestCase(BaseAPITestCase):
    url_name = "v1-convert-document-formats"

    def setUp(self) -> None:
        super().setUp()
        self.expected = {
            "input_formats": INPUT_FORMATS,
            "output_formats": OUTPUT_FORMATS
        }

    def test_unauthorized_success(self):
        """Should return a list of available format if user is not authorized"""

        response = self.client.get(
            self.get_url(),
        )
        self.assertEqual(self.expected, response.json())

    def test_authorized_success(self):
        """Should return a list of available formant if user is authorized"""
        response = self.client.get(
            self.get_url(),
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(self.expected, response.json())


class CreateDocumentConversionTaskTestCase(BaseAPITestCase):
    url_name = "v1-convert-document-create"

    def setUp(self) -> None:
        super().setUp()
        self.content = b"<!DOCTYPE html>" \
                       b"<html>" \
                       b"<body>" \
                       b"<h1>First Heading</h1>" \
                       b"<p>First paragraph.</p>" \
                       b"</body>" \
                       b"</html>"
        self.expected = "# First Heading\n\n" \
                        "First paragraph.\n"

        self.input_format = ".html"
        self.output_format = "md"

        self.temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=self.input_format)
        self.temp_input.write(self.content)
        self.temp_input.close()

    def test_create_success(self):
        """Should create a task if data and credentials are correct"""
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": self.output_format,
                    "input_file": f
                },
                headers={"Authorization": f"Token {self.get_user_token_value()}"}
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], Task.Statuses.CREATED)

    def test_create_unauthorized(self):
        """Should return unauthorized if credentials are not provided"""
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": self.output_format,
                    "input_file": f
                },
            )
        self.assertEqual(response.status_code, 401)

    def test_missing_file(self):
        """Should return a bad request if file is not provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test_task_1",
                "output_format": self.output_format,
            },
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(response.status_code, 400)

    def test_bad_data(self):
        """Should return a bad request if output format is wrong"""
        with open(self.temp_input.name) as f:
            response = self.client.post(
                self.get_url(),
                {
                    "name": "test_task_1",
                    "output_format": "png",  # wrong format
                    "input_file": f
                },
                headers={"Authorization": f"Token {self.get_user_token_value()}"}
            )
        self.assertEqual(response.status_code, 400)


class RetrieveDocumentConversionTaskTestCase(BaseAPITestCase):
    url_name = "v1-convert-document-retrieve"

    def setUp(self) -> None:
        super().setUp()

        self.data = {
            "name": "test_task",
            "output_format": "pdf",
            "input_file": SimpleUploadedFile(
                "testfile.txt",
                b"test content"
            )
        }

        self.user_task = DocumentConversionTask.objects.create(
            initiator=self.user,
            **self.data
        )
        self.other_task = DocumentConversionTask.objects.create(
            initiator=self.another_user,
            **self.data
        )

    def get_url(self, task_id):
        return reverse(self.url_name, kwargs={"id": task_id})

    def test_success(self):
        """Should return a task detail if credentials, task id and user initiator is correct"""
        response = self.client.get(
            self.get_url(self.user_task.id),
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_task.id, response.json()["id"])

    def test_wrong_id(self):
        """Should return 404 if provided task does not exist"""
        non_existent_task_id = 200
        response = self.client.get(
            self.get_url(non_existent_task_id),
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertFalse(DocumentConversionTask.objects.filter(id=non_existent_task_id).first())
        self.assertEqual(response.status_code, 404)

    def test_wrong_user(self):
        """Should return 404 if provided task exists, but it initiated by other user"""
        other_task_id = self.other_task.id
        response = self.client.get(
            self.get_url(other_task_id),
            headers={"Authorization": f"Token {self.get_user_token_value()}"}
        )
        self.assertTrue(DocumentConversionTask.objects.filter(id=other_task_id).exists())
        self.assertEqual(response.status_code, 404)

    def test_unauthorized(self):
        """Should return 401 if credentials are not provided"""
        response = self.client.get(
            self.get_url(self.user_task.id),
        )
        self.assertEqual(response.status_code, 401)
