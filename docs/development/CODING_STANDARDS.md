# Coding Standards

This document outlines the coding standards and best practices for the Calibrify project.

## General Guidelines

1. **Code Readability**
   - Write self-documenting code
   - Use meaningful variable and function names
   - Keep functions focused and small
   - Follow language-specific conventions

2. **Documentation**
   - Add docstrings to all functions and classes
   - Include type hints
   - Document complex algorithms
   - Keep comments up to date

3. **File Organization**
   - One class per file (when practical)
   - Group related functionality
   - Use meaningful file names
   - Keep files under 300 lines

## Python Standards

### 1. Style Guide

Follow PEP 8 with these specifics:

```python
# Imports
from __future__ import annotations  # At the top
import os
import sys
from typing import List, Optional

# Standard library imports first
import json
import datetime

# Third-party imports
import django
import requests

# Local imports
from .models import Equipment
from .utils import format_date

class EquipmentManager:
    """
    Manages equipment operations.
    
    Attributes:
        name (str): Equipment name
        status (str): Current status
    """
    
    def get_calibration_status(self, equipment_id: int) -> dict:
        """
        Get equipment calibration status.
        
        Args:
            equipment_id: The equipment ID
            
        Returns:
            dict: Calibration status information
            
        Raises:
            Equipment.DoesNotExist: If equipment not found
        """
        pass
```

### 2. Type Hints

- Use type hints for all function arguments and returns
- Use Optional[] for nullable values
- Use Union[] for multiple types
- Use TypeVar for generics

### 3. Error Handling

```python
try:
    result = potentially_failing_function()
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    raise CustomException("Meaningful message") from e
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    raise
```

## JavaScript Standards

### 1. Style Guide

```javascript
// Use ES6+ features
const getEquipment = async (id) => {
  try {
    const response = await fetch(`/api/equipment/${id}`);
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch equipment:', error);
    throw error;
  }
};

// Use meaningful names
const updateCalibrationStatus = (equipment) => {
  if (!equipment.lastCalibration) {
    return 'Never calibrated';
  }
  
  const daysSinceCalibration = calculateDaysSince(equipment.lastCalibration);
  return daysSinceCalibration > equipment.calibrationInterval
    ? 'Overdue'
    : 'Up to date';
};
```

### 2. DOM Manipulation

```javascript
// Prefer querySelector over getElementById
const element = document.querySelector('.equipment-list');

// Use dataset for data attributes
element.dataset.status = 'active';

// Use template literals for HTML
const createListItem = (equipment) => `
  <li class="equipment-item" data-id="${equipment.id}">
    <h3>${equipment.name}</h3>
    <p>${equipment.description}</p>
  </li>
`;
```

## HTML/CSS Standards

### 1. HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calibrify - Equipment Management</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="site-header">
        <nav class="main-nav">
            <!-- Navigation content -->
        </nav>
    </header>
    
    <main class="content">
        <section class="equipment-list">
            <!-- Content here -->
        </section>
    </main>
    
    <footer class="site-footer">
        <!-- Footer content -->
    </footer>
</body>
</html>
```

### 2. CSS Organization

```css
/* Use BEM naming convention */
.block {}
.block__element {}
.block--modifier {}

/* Example */
.equipment-card {}
.equipment-card__title {}
.equipment-card--active {}

/* Use CSS custom properties */
:root {
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --spacing-unit: 8px;
}

/* Organize by component */
.equipment-card {
  padding: calc(var(--spacing-unit) * 2);
  border: 1px solid var(--color-border);
}
```

## Database Standards

### 1. Model Design

```python
class Equipment(models.Model):
    """
    Equipment model representing calibratable items.
    """
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['serial_number']),
        ]
```

### 2. Query Optimization

```python
# Use select_related for foreign keys
Equipment.objects.select_related('category').all()

# Use prefetch_related for many-to-many
Equipment.objects.prefetch_related('calibrations').all()

# Use bulk operations
Equipment.objects.bulk_create(equipment_list)
```

## Testing Standards

### 1. Unit Tests

```python
class EquipmentTests(TestCase):
    def setUp(self):
        self.equipment = Equipment.objects.create(
            name="Test Equipment",
            serial_number="TEST001"
        )

    def test_equipment_creation(self):
        """Test equipment can be created."""
        self.assertEqual(self.equipment.name, "Test Equipment")
        self.assertEqual(self.equipment.serial_number, "TEST001")
```

### 2. Integration Tests

```python
class CalibrationAPITests(APITestCase):
    def test_calibration_creation(self):
        """Test calibration can be created via API."""
        url = reverse('calibration-create')
        data = {
            'equipment': self.equipment.id,
            'date': '2023-01-01',
            'notes': 'Test calibration'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Security Standards

1. **Input Validation**
   - Validate all user input
   - Use Django's form validation
   - Sanitize data before storage

2. **Authentication**
   - Use Django's authentication system
   - Implement proper password policies
   - Use secure session management

3. **Authorization**
   - Implement proper permission checks
   - Use Django's permission system
   - Check object-level permissions

## Version Control

1. **Branch Naming**
   ```
   feature/add-calibration-reminder
   fix/incorrect-date-format
   refactor/equipment-model
   ```

2. **Commit Messages**
   ```
   feat: add equipment calibration reminder
   fix: correct date format in calibration view
   docs: update API documentation
   ```

## Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] No unnecessary dependencies added
- [ ] Error handling is appropriate
- [ ] Logging is adequate 