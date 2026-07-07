# Open-Source CLM Stack

## Architecture Overview
**Approach:** Hybrid (DOCX templates → HTML editing → PDF output)

---

## Tech Stack

### Frontend
```yaml
Framework: React 18 + Next.js 14
Language: TypeScript 5.3+
UI Components: shadcn/ui (Radix UI + Tailwind CSS)
Rich Text Editor: Tiptap (MIT license)
Forms: React Hook Form + Zod
Diff Viewer: react-diff-viewer
PDF Viewer: react-pdf (PDF.js)
State Management: Zustand
HTTP Client: Axios + TanStack Query
```

### Backend
```yaml
Language: Python 3.11+
Framework: FastAPI
DOCX Processing: 
  - python-docx (read/write)
  - docxtpl (template engine - Jinja2 based)
  - python-docx2html (DOCX → HTML)
PDF Generation: LibreOffice (headless) + subprocess
Template Engine: Jinja2 (built-in with docxtpl)
Diff Engine: difflib (stdlib) + diff-match-patch
Task Queue: Celery
Message Broker: Redis
ORM: SQLAlchemy 2.0
Validation: Pydantic V2
Oracle Driver: python-oracledb
```

### Database
```yaml
Primary: Oracle Database 19c+
Cache: Redis 7+
Features: JSON support, temporal queries
```

### Storage
```yaml
Object Storage: MinIO (S3-compatible, self-hosted)
Alternative: AWS S3
```

### Infrastructure
```yaml
Containerization: Docker + Docker Compose
Reverse Proxy: Nginx
Monitoring: Prometheus + Grafana
Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
Error Tracking: Sentry
```

---

## Package Dependencies

### Backend (requirements.txt)
```txt
fastapi==0.104.0
uvicorn[standard]==0.24.0
python-docx==1.1.0
docxtpl==0.17.0
python-docx2html==0.1.0
jinja2==3.1.2
celery==5.3.4
redis==5.0.1
python-oracledb==1.4.2
sqlalchemy==2.0.23
pydantic==2.5.2
boto3==1.29.7
python-multipart==0.0.6
python-magic==0.4.27
diff-match-patch==20230430
pydantic-settings==2.1.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.0.4",
    "typescript": "^5.3.3",
    "@tiptap/react": "^2.1.13",
    "@tiptap/starter-kit": "^2.1.13",
    "@tiptap/extension-table": "^2.1.13",
    "react-hook-form": "^7.49.2",
    "zod": "^3.22.4",
    "@tanstack/react-query": "^5.17.9",
    "axios": "^1.6.2",
    "react-diff-viewer": "^3.1.1",
    "react-pdf": "^7.6.0",
    "zustand": "^4.4.7",
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6"
  }
}
```

---

## Document Workflow

### Template Format
**Default:** `.docx` (created in MS Word)

**Variable Syntax:**
```
{{ client_name }}
{{ contract_date }}

{% if payment_plan == "monthly" %}
Monthly: {{ monthly_amount }}
{% endif %}

{% for item in items %}
- {{ item.name }}: ${{ item.price }}
{% endfor %}
```

### Conversions Required
```
1. Template Load:   DOCX → HTML (python-docx2html) → Cache (Redis)
2. User Editing:    HTML (Tiptap editor)
3. Save:            HTML → DOCX (python-docx + docxtpl merge)
4. Preview:         HTML (browser render)
5. Final Output:    DOCX → PDF (LibreOffice headless)
6. Redlining:       HTML diff (diff-match-patch)
```

---

## Template Population

### Library: docxtpl
```python
from docxtpl import DocxTemplate

doc = DocxTemplate("template.docx")

context = {
    'client_name': 'Acme Corp',
    'contract_value': '$150,000',
    'start_date': '2026-07-05',
    'items': [
        {'name': 'Service A', 'price': 1000},
        {'name': 'Service B', 'price': 2000}
    ]
}

doc.render(context)
doc.save("output.docx")
```

---

## Performance Benchmarks

| Operation | Time (20-page doc) |
|-----------|-------------------|
| DOCX → HTML | 1-2s |
| Data Merge | 500ms |
| DOCX → PDF | 3-5s (LibreOffice) |
| HTML Diff | 100ms |
| **Total Pipeline** | **5-8s** |

---

## Cost Estimate

| Item | Annual Cost |
|------|-------------|
| Software Licenses | $0 |
| Infrastructure (AWS/Azure) | $12,000-24,000 |
| Development Time | +30% vs commercial |
| **Total** | **$12,000-24,000** |

---

## Limitations

- DOCX→HTML fidelity: 85% (complex layouts may break)
- LibreOffice PDF conversion: slower (3-5s), occasional formatting issues
- No enterprise SLA
- More development effort required
- Manual DOCX generation complexity

---

## Advantages

- ✅ Zero licensing costs
- ✅ Full control over codebase
- ✅ No vendor lock-in
- ✅ Active open-source communities
- ✅ Customizable to specific needs
