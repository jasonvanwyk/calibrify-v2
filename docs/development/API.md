# API Documentation

## Overview

The Calibrify API is a RESTful service that provides access to equipment calibration and maintenance functionality. This document describes the available endpoints, authentication methods, and example usage.

## Base URL

```
Production: https://api.example.com/api/v1/
Development: http://localhost:8000/api/v1/
```

## Authentication

### JWT Authentication

```bash
# Get JWT token
POST /api/token/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "your-password"
}

# Response
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

# Use token in requests
GET /api/v1/equipment/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Endpoints

### Equipment

#### List Equipment

```bash
GET /api/v1/equipment/

# Query Parameters
?search=term           # Search equipment by name/serial
?category=id          # Filter by category
?status=active        # Filter by status
?page=1              # Pagination
?page_size=10        # Items per page

# Response
{
    "count": 100,
    "next": "http://api.example.com/api/v1/equipment/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Microscope XYZ",
            "serial_number": "MSC001",
            "category": {
                "id": 1,
                "name": "Microscopes"
            },
            "status": "active",
            "last_calibration": "2023-01-01T00:00:00Z",
            "next_calibration": "2024-01-01T00:00:00Z"
        }
    ]
}
```

#### Create Equipment

```bash
POST /api/v1/equipment/
Content-Type: application/json

{
    "name": "New Microscope",
    "serial_number": "MSC002",
    "category_id": 1,
    "location_id": 1,
    "calibration_interval": 365,
    "description": "High-precision microscope"
}

# Response
{
    "id": 2,
    "name": "New Microscope",
    "serial_number": "MSC002",
    "category": {
        "id": 1,
        "name": "Microscopes"
    },
    "status": "active",
    "created_at": "2023-12-01T12:00:00Z"
}
```

### Calibrations

#### List Calibrations

```bash
GET /api/v1/calibrations/
GET /api/v1/equipment/{equipment_id}/calibrations/

# Response
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "equipment": {
                "id": 1,
                "name": "Microscope XYZ"
            },
            "date": "2023-01-01T00:00:00Z",
            "performed_by": {
                "id": 1,
                "name": "John Doe"
            },
            "status": "passed",
            "certificate_url": "https://..."
        }
    ]
}
```

#### Create Calibration

```bash
POST /api/v1/calibrations/
Content-Type: multipart/form-data

{
    "equipment_id": 1,
    "date": "2023-12-01T12:00:00Z",
    "status": "passed",
    "notes": "Regular calibration",
    "certificate": <file>
}

# Response
{
    "id": 2,
    "equipment": {
        "id": 1,
        "name": "Microscope XYZ"
    },
    "date": "2023-12-01T12:00:00Z",
    "status": "passed",
    "certificate_url": "https://..."
}
```

### Maintenance

#### Schedule Maintenance

```bash
POST /api/v1/maintenance/
Content-Type: application/json

{
    "equipment_id": 1,
    "scheduled_date": "2024-01-15T10:00:00Z",
    "type": "preventive",
    "description": "Annual maintenance"
}

# Response
{
    "id": 1,
    "equipment": {
        "id": 1,
        "name": "Microscope XYZ"
    },
    "scheduled_date": "2024-01-15T10:00:00Z",
    "status": "scheduled"
}
```

### Reports

#### Generate Audit Report

```bash
POST /api/v1/reports/audit/
Content-Type: application/json

{
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "equipment_ids": [1, 2, 3],
    "format": "pdf"
}

# Response
{
    "report_url": "https://...",
    "generated_at": "2023-12-01T12:00:00Z",
    "expires_at": "2023-12-08T12:00:00Z"
}
```

## Webhooks

### Register Webhook

```bash
POST /api/v1/webhooks/
Content-Type: application/json

{
    "url": "https://your-server.com/webhook",
    "events": ["calibration.created", "maintenance.scheduled"],
    "secret": "your-webhook-secret"
}

# Response
{
    "id": "webhook_id",
    "url": "https://your-server.com/webhook",
    "events": ["calibration.created", "maintenance.scheduled"],
    "created_at": "2023-12-01T12:00:00Z"
}
```

## Error Responses

```json
{
    "error": {
        "code": "validation_error",
        "message": "Invalid input data",
        "details": {
            "field": ["Error message"]
        }
    }
}
```

## Rate Limiting

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1701432000
```

## Pagination

All list endpoints support pagination:

```bash
GET /api/v1/equipment/?page=2&page_size=10

# Response
{
    "count": 100,
    "next": "http://api.example.com/api/v1/equipment/?page=3&page_size=10",
    "previous": "http://api.example.com/api/v1/equipment/?page=1&page_size=10",
    "results": []
}
```

## Filtering

Most endpoints support filtering:

```bash
GET /api/v1/equipment/?category=1&status=active&search=microscope
GET /api/v1/calibrations/?start_date=2023-01-01&end_date=2023-12-31
```

## API Versioning

The API uses URL versioning:

- Current version: `v1`
- Beta features: `v1-beta`
- Legacy support: Specified in headers

## SDK Examples

### Python

```python
import requests

class CalibrifyClient:
    def __init__(self, api_key, base_url="https://api.example.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        
    def get_equipment(self, equipment_id):
        response = requests.get(
            f"{self.base_url}/equipment/{equipment_id}/",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
        
    def create_calibration(self, equipment_id, data):
        response = requests.post(
            f"{self.base_url}/calibrations/",
            json={"equipment_id": equipment_id, **data},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
```

### JavaScript

```javascript
class CalibrifyAPI {
    constructor(apiKey, baseUrl = 'https://api.example.com/v1') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
    }
    
    async getEquipment(id) {
        const response = await fetch(`${this.baseUrl}/equipment/${id}/`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            }
        });
        return await response.json();
    }
    
    async createCalibration(equipmentId, data) {
        const response = await fetch(`${this.baseUrl}/calibrations/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                equipment_id: equipmentId,
                ...data
            })
        });
        return await response.json();
    }
}
```

## Best Practices

1. **Authentication**
   - Always use HTTPS
   - Rotate API keys regularly
   - Use short-lived JWT tokens

2. **Rate Limiting**
   - Implement exponential backoff
   - Cache responses when possible
   - Monitor rate limit headers

3. **Error Handling**
   - Handle HTTP 429 (Too Many Requests)
   - Implement retry logic
   - Log API errors appropriately

4. **Data Validation**
   - Validate input before sending
   - Handle validation errors gracefully
   - Check response status codes

## Support

For API support:
- Email: api-support@example.com
- Documentation: https://docs.example.com
- Status page: https://status.example.com 