# Testing Strategy and Guidelines

## Overview

This document outlines the testing strategy and guidelines for the Calibrify project, ensuring code quality and reliability.

## Testing Levels

### 1. Unit Tests

```python
# tests/test_equipment.py
from django.test import TestCase
from apps.equipment.models import Equipment
from apps.calibration.models import Calibration

class EquipmentTests(TestCase):
    def setUp(self):
        self.equipment = Equipment.objects.create(
            name="Test Equipment",
            serial_number="TEST001",
            calibration_interval=365
        )

    def test_equipment_creation(self):
        """Test equipment can be created with valid data."""
        self.assertEqual(self.equipment.name, "Test Equipment")
        self.assertEqual(self.equipment.serial_number, "TEST001")
        self.assertEqual(self.equipment.calibration_interval, 365)

    def test_calibration_due_date(self):
        """Test calibration due date calculation."""
        Calibration.objects.create(
            equipment=self.equipment,
            date="2023-01-01",
            performed_by=self.user
        )
        self.assertEqual(
            self.equipment.next_calibration_date(),
            datetime.date(2024, 1, 1)
        )
```

### 2. Integration Tests

```python
# tests/integration/test_calibration_workflow.py
from rest_framework.test import APITestCase
from django.urls import reverse

class CalibrationWorkflowTests(APITestCase):
    def setUp(self):
        self.user = self.create_user()
        self.client.force_authenticate(user=self.user)
        self.equipment = self.create_equipment()

    def test_complete_calibration_workflow(self):
        """Test the complete calibration workflow."""
        # Schedule calibration
        schedule_data = {
            'equipment': self.equipment.id,
            'scheduled_date': '2023-12-01',
            'notes': 'Regular calibration'
        }
        response = self.client.post(
            reverse('calibration-schedule'),
            schedule_data
        )
        self.assertEqual(response.status_code, 201)
        calibration_id = response.data['id']

        # Perform calibration
        perform_data = {
            'measurements': [
                {'point': 0, 'reading': 0.001},
                {'point': 10, 'reading': 10.002}
            ],
            'status': 'passed',
            'certificate': self.get_test_file()
        }
        response = self.client.put(
            reverse('calibration-perform', args=[calibration_id]),
            perform_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'completed')
```

### 3. End-to-End Tests

```python
# tests/e2e/test_equipment_management.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import BaseE2ETest

class EquipmentManagementTests(BaseE2ETest):
    def test_add_equipment_workflow(self):
        """Test adding new equipment through the UI."""
        self.login()
        
        # Navigate to equipment page
        self.driver.find_element(By.ID, "nav-equipment").click()
        
        # Click add equipment button
        self.driver.find_element(By.ID, "add-equipment-btn").click()
        
        # Fill form
        self.driver.find_element(By.ID, "equipment-name").send_keys("New Equipment")
        self.driver.find_element(By.ID, "serial-number").send_keys("SN001")
        
        # Submit form
        self.driver.find_element(By.ID, "submit-btn").click()
        
        # Verify success
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        self.assertIn("Equipment added successfully", success_message.text)
```

## Test Categories

### 1. Functional Tests

```python
# tests/functional/test_equipment_api.py
class EquipmentAPITests(APITestCase):
    def test_equipment_crud(self):
        """Test CRUD operations for equipment."""
        # Create
        response = self.client.post('/api/equipment/', {
            'name': 'Test Equipment',
            'serial_number': 'TEST001'
        })
        self.assertEqual(response.status_code, 201)
        equipment_id = response.data['id']
        
        # Read
        response = self.client.get(f'/api/equipment/{equipment_id}/')
        self.assertEqual(response.status_code, 200)
        
        # Update
        response = self.client.put(f'/api/equipment/{equipment_id}/', {
            'name': 'Updated Equipment'
        })
        self.assertEqual(response.status_code, 200)
        
        # Delete
        response = self.client.delete(f'/api/equipment/{equipment_id}/')
        self.assertEqual(response.status_code, 204)
```

### 2. Performance Tests

```python
# tests/performance/test_api_performance.py
import locust

class CalibrifySiteUser(HttpUser):
    @task
    def view_equipment_list(self):
        self.client.get("/api/equipment/")
    
    @task
    def search_equipment(self):
        self.client.get("/api/equipment/?search=microscope")
    
    @task
    def view_calibrations(self):
        self.client.get("/api/calibrations/")
```

### 3. Security Tests

```python
# tests/security/test_authentication.py
class SecurityTests(TestCase):
    def test_password_complexity(self):
        """Test password complexity requirements."""
        weak_passwords = [
            'password123',
            'abc123',
            'qwerty'
        ]
        for password in weak_passwords:
            with self.assertRaises(ValidationError):
                validate_password(password)

    def test_jwt_expiration(self):
        """Test JWT token expiration."""
        token = create_access_token(self.user)
        self.assertTrue(verify_token(token))
        
        # Fast forward time
        with freeze_time(timezone.now() + timedelta(hours=2)):
            self.assertFalse(verify_token(token))
```

## Test Configuration

### 1. pytest Configuration

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = --nomigrations --cov=. --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### 2. Coverage Configuration

```ini
# .coveragerc
[run]
source = .
omit =
    */migrations/*
    */tests/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

## Test Data Management

### 1. Factories

```python
# tests/factories.py
import factory
from apps.equipment.models import Equipment
from apps.calibration.models import Calibration

class EquipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Equipment
    
    name = factory.Sequence(lambda n: f'Equipment {n}')
    serial_number = factory.Sequence(lambda n: f'SN{n:05d}')
    calibration_interval = 365

class CalibrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Calibration
    
    equipment = factory.SubFactory(EquipmentFactory)
    date = factory.Faker('date_this_year')
    performed_by = factory.SubFactory('tests.factories.UserFactory')
```

### 2. Fixtures

```python
# tests/fixtures.py
import pytest
from .factories import EquipmentFactory, CalibrationFactory

@pytest.fixture
def equipment():
    return EquipmentFactory()

@pytest.fixture
def calibration(equipment):
    return CalibrationFactory(equipment=equipment)

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
```

## CI/CD Integration

### 1. GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements/test.txt
          
      - name: Run tests
        run: |
          pytest --cov
          coverage xml
          
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Documentation

### 1. Test Case Template

```markdown
## Test Case: [ID] - [Brief Description]

### Objective
[What is being tested and why]

### Prerequisites
- Required setup
- Required data
- Required permissions

### Test Steps
1. Step one
2. Step two
3. Step three

### Expected Results
- Result one
- Result two

### Actual Results
- [To be filled during testing]

### Pass/Fail Criteria
- Criterion one
- Criterion two
```

### 2. Test Report Template

```markdown
# Test Report

## Summary
- Total Tests: X
- Passed: Y
- Failed: Z
- Coverage: XX%

## Failed Tests
1. [Test ID] - [Description]
   - Error: [Error message]
   - Stack trace: [Stack trace]

## Coverage Report
- Module A: XX%
- Module B: YY%
- Module C: ZZ%

## Recommendations
1. [Recommendation one]
2. [Recommendation two]
```

## Best Practices

### 1. Test Organization

- Group tests by feature/module
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Keep tests independent

### 2. Test Maintenance

- Regular test cleanup
- Update tests with code changes
- Remove obsolete tests
- Monitor test performance

### 3. Code Quality

- Use assertions effectively
- Handle test data cleanup
- Mock external services
- Use appropriate test isolation

## Troubleshooting

### 1. Common Issues

- Database connection errors
- Test isolation problems
- Slow tests
- Flaky tests

### 2. Solutions

- Use test databases
- Reset state between tests
- Optimize test performance
- Implement retry logic for flaky tests 