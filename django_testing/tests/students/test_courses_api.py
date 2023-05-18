import pytest
from rest_framework.test import APIClient

from students.models import Student, Course
from model_bakery import baker



@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def cours_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_api_client(client, cours_factory):
    cours = cours_factory(_quantity=1, name='python1')
    response = client.get(f'/api/v1/courses/{cours[0].id}/')
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == cours[0].id

@pytest.mark.django_db
def test_cours_get_2(client, cours_factory):
    cours = cours_factory(_quantity=5)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0

@pytest.mark.django_db
def test_cours_get_id(client, cours_factory):
    cours = cours_factory(_quantity=1)
    response = client.get("/api/v1/courses/", {'id': cours[0].id})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == cours[0].id


@pytest.mark.django_db
def test_cours_get_name(client, cours_factory):
    cours = cours_factory(_quantity=1)
    response = client.get("/api/v1/courses/", {'name': cours[0].name})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == cours[0].name


@pytest.mark.django_db
def test_cours_post(client):
    response = client.post("/api/v1/courses/", data={'name': 'tort'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_cours_patch(client, cours_factory):
    cours = cours_factory(_quantity=1, name='ne_python')
    new_name = 'python'
    response = client.patch(f'/api/v1/courses/{cours[0].id}/', data={'name': new_name})
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == new_name

@pytest.mark.django_db
def test_cours_delete(client, cours_factory):
    cours = cours_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{cours[0].id}/')
    assert response.status_code == 204
