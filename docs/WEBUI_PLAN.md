# 🌐 Web UI - Piano di Sviluppo

## 📋 Panoramica

La **Fase 5** aggiungerà un'interfaccia web moderna e user-friendly al Research Assistant CLI, permettendo agli utenti di:
- Interagire con il sistema tramite browser
- Visualizzare risultati con link cliccabili
- Navigare facilmente tra le fonti
- Salvare e condividere ricerche

## 🎯 Obiettivi

### Funzionalità Core
- ✅ **Interfaccia Web**: Dashboard moderna e responsive
- ✅ **Ricerca Interattiva**: Form di ricerca con autocompletamento
- ✅ **Risultati Visuali**: Display elegante con citazioni e link
- ✅ **Navigazione Fonti**: Link cliccabili alle fonti originali
- ✅ **Storia Ricerche**: Cronologia delle ricerche effettuate
- ✅ **Export Risultati**: Download in PDF/HTML/JSON

### Funzionalità Avanzate
- 🔄 **Ricerca in Tempo Reale**: Aggiornamenti live durante la ricerca
- 🔄 **Filtri Avanzati**: Filtra per motore, data, dominio
- 🔄 **Condivisione**: Link diretti ai risultati
- 🔄 **Temi**: Modalità chiara/scura
- 🔄 **Mobile**: Design responsive per dispositivi mobili

## 🏗️ Architettura

### Stack Tecnologico

```
Frontend:
├── React/Vue.js          # Framework UI
├── Tailwind CSS          # Styling
├── Axios                 # HTTP client
└── React Router          # Routing

Backend:
├── FastAPI               # API REST
├── Uvicorn               # ASGI server
├── SQLite/PostgreSQL     # Database
└── WebSocket             # Real-time updates
```

### Struttura Progetto

```
ai-search-app/
├── src/
│   ├── main.py           # CLI entry point
│   ├── config.py         # Configurazione
│   ├── api/              # API REST
│   │   ├── __init__.py
│   │   ├── routes.py     # Endpoint API
│   │   ├── models.py     # Data models
│   │   └── database.py   # DB operations
│   └── webui/            # Frontend
│       ├── static/       # Assets
│       ├── templates/    # HTML templates
│       └── components/   # React components
├── webui/                # Frontend standalone
│   ├── src/
│   ├── public/
│   └── package.json
└── docs/
    └── webui.md          # Documentazione Web UI
```

## 🎨 Design UI/UX

### Layout Principale

```
┌─────────────────────────────────────────────────────────┐
│ 🏠 Research Assistant Web UI                          │
├─────────────────────────────────────────────────────────┤
│ 🔍 [Ricerca...] [Avanzate] [Cerca]                   │
├─────────────────────────────────────────────────────────┤
│ 📊 Statistiche: 8 fonti • 85% confidenza • 12.3s    │
├─────────────────────────────────────────────────────────┤
│ 💬 Risposta con citazioni [1][2][3]                  │
│                                                       │
│ Nuclear fusion research has seen significant...       │
│                                                       │
├─────────────────────────────────────────────────────────┤
│ 📚 Fonti:                                              │
│ [1] 🔗 Breakthrough in Nuclear Fusion (nature.com)   │
│ [2] 🔗 NIF Milestone Report (science.org)            │
│ [3] 🔗 Recent Developments (arxiv.org)                │
├─────────────────────────────────────────────────────────┤
│ 💾 [Salva] [Condividi] [Export PDF] [Storia]        │
└─────────────────────────────────────────────────────────┘
```

### Componenti UI

#### 1. **Header**
- Logo e titolo
- Toggle tema (chiaro/scuro)
- Menu utente
- Notifiche

#### 2. **Search Bar**
- Input di ricerca con autocompletamento
- Pulsante ricerca avanzata
- Indicatori di stato (ricerca in corso)

#### 3. **Results Panel**
- Risposta principale con citazioni evidenziate
- Statistiche di ricerca
- Barra di progresso

#### 4. **Sources Panel**
- Lista fonti con preview
- Link cliccabili
- Filtri per dominio/motore
- Ordinamento per rilevanza

#### 5. **Actions Bar**
- Salva ricerca
- Condividi risultati
- Export in vari formati
- Storia ricerche

## 🔧 Implementazione

### Fase 1: Setup Base
```bash
# 1. Installazione dipendenze
pip install fastapi uvicorn sqlalchemy

# 2. Setup frontend
npm create vite@latest webui -- --template react
cd webui
npm install axios tailwindcss
```

### Fase 2: API REST
```python
# src/api/routes.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Research Assistant API")

class SearchRequest(BaseModel):
    query: str
    engines: list[str] = ["searx", "brave", "yahoo"]
    max_results: int = 8

@app.post("/api/search")
async def search_web(request: SearchRequest):
    # Implementazione ricerca
    pass

@app.get("/api/history")
async def get_search_history():
    # Recupera cronologia
    pass
```

### Fase 3: Frontend React
```jsx
// webui/src/components/SearchForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

const SearchForm = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/search', { query });
      setResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-form">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Inserisci la tua ricerca..."
        className="search-input"
      />
      <button 
        onClick={handleSearch}
        disabled={loading}
        className="search-button"
      >
        {loading ? '🔍 Ricerca...' : '🔍 Cerca'}
      </button>
    </div>
  );
};
```

### Fase 4: Database
```python
# src/api/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)
    answer = Column(Text)
    sources = Column(Text)  # JSON
    confidence = Column(Integer)
    execution_time = Column(Integer)
    created_at = Column(DateTime)
```

## 🎨 Design System

### Colori
```css
:root {
  --primary: #3b82f6;      /* Blue */
  --secondary: #10b981;    /* Green */
  --accent: #f59e0b;       /* Orange */
  --danger: #ef4444;        /* Red */
  --success: #22c55e;       /* Green */
  --warning: #f59e0b;       /* Orange */
  --info: #3b82f6;         /* Blue */
}
```

### Componenti
- **Button**: Pulsanti con varianti (primary, secondary, outline)
- **Card**: Contenitori per risultati e fonti
- **Badge**: Tag per motori di ricerca e stati
- **Modal**: Popup per dettagli e configurazioni
- **Tooltip**: Informazioni aggiuntive su hover

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile First */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### Layout Adattivo
- **Mobile**: Layout a colonna singola
- **Tablet**: Layout a due colonne
- **Desktop**: Layout a tre colonne con sidebar

## 🔄 Real-time Features

### WebSocket Integration
```python
# src/api/websocket.py
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```

### Live Updates
- Progress bar durante la ricerca
- Notifiche in tempo reale
- Aggiornamenti automatici dei risultati

## 🚀 Deployment

### Docker Setup
```dockerfile
# Dockerfile.webui
FROM node:18-alpine as frontend
WORKDIR /app
COPY webui/package*.json ./
RUN npm install
COPY webui/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY --from=frontend /app/dist ./static

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Web UI specific
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8000
WEBUI_DEBUG=false
WEBUI_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./research_assistant.db
```

## 📊 Analytics

### Metriche da Tracciare
- Numero di ricerche per giorno
- Tempo medio di ricerca
- Motori di ricerca più utilizzati
- Errori e fallimenti
- Performance API

### Dashboard Admin
- Statistiche in tempo reale
- Monitoraggio errori
- Gestione utenti
- Configurazione sistema

## 🔒 Sicurezza

### Autenticazione
- JWT tokens per API
- Session management
- Rate limiting
- CORS configuration

### Validazione
- Sanitizzazione input
- Protezione XSS
- CSRF protection
- SQL injection prevention

## 🧪 Testing

### Frontend Tests
```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Visual regression
npm run test:visual
```

### Backend Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_search_endpoint():
    response = client.post("/api/search", json={
        "query": "test query",
        "engines": ["searx"]
    })
    assert response.status_code == 200
    assert "results" in response.json()
```

## 📈 Roadmap Web UI

### Sprint 1 (2 settimane)
- [ ] Setup progetto base
- [ ] API REST endpoints
- [ ] Frontend React base
- [ ] Search form funzionante

### Sprint 2 (2 settimane)
- [ ] Results display
- [ ] Sources panel
- [ ] Basic styling
- [ ] Database integration

### Sprint 3 (2 settimane)
- [ ] History feature
- [ ] Export functionality
- [ ] Responsive design
- [ ] Error handling

### Sprint 4 (2 settimane)
- [ ] Real-time updates
- [ ] Advanced filters
- [ ] User preferences
- [ ] Performance optimization

### Sprint 5 (1 settimana)
- [ ] Testing & bug fixes
- [ ] Documentation
- [ ] Deployment setup
- [ ] Launch preparation

## 🎯 Success Metrics

### KPIs Tecnici
- Tempo di caricamento < 2 secondi
- Uptime > 99.9%
- Error rate < 1%
- API response time < 500ms

### KPIs Business
- Numero utenti attivi
- Tempo medio di sessione
- Tasso di conversione (ricerche completate)
- User satisfaction score

---

**🚀 La Web UI trasformerà il Research Assistant da tool CLI a piattaforma web completa e accessibile!** 