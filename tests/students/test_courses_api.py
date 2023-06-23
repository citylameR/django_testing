import pytest
from model_bakery import baker

from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_cource(client, course_factory):
    # Arrange
    courses = course_factory()

    # Act
    response = client.get(f'/api/v1/courses/{courses.id}/')
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert courses.name == data['name']


@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=100)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert courses[i].name == course['name']


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=9)
    i = 5

    # Act
    response = client.get('/api/v1/courses/', {'id': courses[i].id, 'name': courses[i].name},)

    # Assert
    data = response.json
    assert response.status_code == 200
    assert courses[i].id == response.json()[0]['id']


@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    count = Course.objects.count()
    name = 'Вы устроитесь на работу'

    # Act
    response1 = client.post('/api/v1/courses/', data={'name': name})
    response2 = client.get(f'/api/v1/courses/?name={name}')

    # Assert
    assert response1.status_code == 201
    assert Course.objects.count() == count + 1
    assert response2.status_code == 200


@pytest.mark.django_db
def test_patch_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=100)

    # Act
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data = {'name': 'Вы устроитесь на работу'})

    # Assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=100)

    # Act
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')

    # Assert
    assert response.status_code == 204


