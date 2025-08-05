# 🛠️ Guida per Sviluppatori - Research Assistant CLI

## 📋 Panoramica Tecnica

### Architettura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Search Engine  │    │   AI Client     │
│                 │    │     Manager      │    │                 │
│ - User Input    │───▶│ - Multi-engine  │───▶│ - Ollama        │
│ - Results       │    │ - Deduplication │    │ - oobabooga     │
│ - Configuration │    │ - Statistics     │    │ - Fallback      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Configuration │    │   Data Models   │    │   Output        │
│                 │    │                 │    │                 │
│ - Environment   │    │ - SearchResult  │    │ - JSON Export   │
│ - Validation    │    │ - ResearchAnswer│    │ - Console       │
│ - Security      │    │ - SearchStats   │    │ - Logging       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componenti Principali

#### 1. **Configuration Manager** (`src/config.py`)
- Gestione centralizzata delle variabili d'ambiente
- Validazione automatica dei parametri
- Supporto per diversi ambienti (dev, prod)

#### 2. **Search Engine Manager** (`src/main.py`)
- Orchestrazione dei motori di ricerca
- Deduplicazione intelligente dei risultati
- Gestione degli errori e fallback

#### 3. **AI Client** (`src/main.py`)
- Interfaccia unificata per LLM locali
- Supporto per Ollama e oobabooga
- Gestione dei prompt e generazione risposte

## 🔧 Setup Sviluppo

### Ambiente di Sviluppo

```bash
# 1. Clona e setup
git clone https://github.com/yourusername/ai-search-app.git
cd ai-search-app

# 2. Ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# 3. Dipendenze sviluppo
pip install -r requirements.txt
pip install -r requirements-dev.txt  # se disponibile

# 4. Pre-commit hooks (opzionale)
pre-commit install
```

### Struttura del Codice

```
src/
├── main.py              # Entry point e logica principale
├── config.py            # Gestione configurazione
└── __init__.py          # Package initialization

# File di configurazione
├── env.example          # Template variabili d'ambiente
├── requirements.txt     # Dipendenze Python
├── .gitignore          # File da ignorare
└── setup.py            # Setup package (futuro)
```

## 📊 Data Models

### SearchResult
```python
@dataclass
class SearchResult:
    title: str              # Titolo del risultato
    snippet: str            # Snippet/descrizione
    url: str               # URL del risultato
    source_engine: str     # Motore di ricerca
    timestamp: str         # Timestamp ISO
    content_length: int    # Lunghezza contenuto
    domain: str           # Dominio estratto
```

### ResearchAnswer
```python
@dataclass
class ResearchAnswer:
    query: str             # Query originale
    answer: str            # Risposta generata
    sources: List[SearchResult]  # Fonti utilizzate
    citations: List[int]   # Citazioni nella risposta
    confidence: float      # Livello di confidenza
    execution_time: float  # Tempo di esecuzione
    search_stats: SearchStats  # Statistiche ricerca
    raw_sources_data: List[Dict]  # Dati grezzi
```

### SearchStats
```python
@dataclass
class SearchStats:
    engines_tried: List[str]      # Motori provati
    engines_successful: List[str] # Motori con successo
    total_results_found: int      # Risultati totali
    unique_results: int           # Risultati unici
    domains_found: List[str]      # Domini trovati
    search_duration: float        # Durata ricerca
    queries_used: List[str]       # Query utilizzate
```

## 🔍 Motori di Ricerca

### Implementazione

Ogni motore di ricerca implementa:
1. **Metodo di ricerca** (es: `_search_brave_enhanced`)
2. **Parser risultati** (es: `_parse_yahoo_results_enhanced`)
3. **Gestione errori** e fallback

### Aggiungere un Nuovo Motore

```python
def _search_new_engine(self, query: str) -> List[SearchResult]:
    """Implementazione nuovo motore di ricerca"""
    try:
        # 1. Preparazione request
        url = "https://api.newengine.com/search"
        params = {"q": query, "format": "json"}
        
        # 2. Esecuzione request
        response = self.session.get(url, params=params, timeout=12)
        
        # 3. Parsing risultati
        if response.status_code == 200:
            data = response.json()
            results = []
            for item in data.get("results", [])[:6]:
                result = SearchResult(
                    title=item.get("title", "").strip(),
                    snippet=item.get("description", "")[:400],
                    url=item.get("url", ""),
                    source_engine="new_engine",
                    timestamp=datetime.now().isoformat()
                )
                results.append(result)
            return results
            
    except Exception as e:
        logger.debug(f"❌ New Engine: Exception - {e}")
        return []

# Aggiungere alla lista dei motori
self.search_engines.append({
    'name': 'new_engine',
    'method': self._search_new_engine,
    'priority': 8
})
```

## 🤖 AI Integration

### Ollama Client

```python
class SimpleAIClient:
    def __init__(self, model=None):
        self.base_url = config.llm.ollama_base_url
        self.model = model or config.llm.ollama_model

    def generate(self, prompt: str, temperature: float = 0.3, num_predict: int = 1000) -> str:
        # Implementazione generazione testo
        pass
```

### oobabooga Integration

```python
class OobaboogaClient:
    def __init__(self):
        self.base_url = config.llm.oobabooga_base_url
        self.model = config.llm.oobabooga_model

    def generate(self, prompt: str) -> str:
        # Implementazione per oobabooga
        pass
```

## 🧪 Testing

### Test Unitari

```bash
# Esegui tutti i test
python -m pytest tests/

# Test specifici
python -m pytest tests/test_config.py
python -m pytest tests/test_search.py

# Con coverage
python -m pytest --cov=src tests/
```

### Test di Integrazione

```bash
# Test configurazione
python -c "from src.config import config; assert config.validate() == []"

# Test connessione Ollama
curl -f http://localhost:11434/api/tags

# Test ricerca
python src/main.py "test query" --output test_results.json
```

### Test Manuali

```bash
# Test motori di ricerca
python -c "
from src.main import EnhancedPerplexityResearcher
researcher = EnhancedPerplexityResearcher(None)
results = researcher._search_brave_enhanced('test')
print(f'Found {len(results)} results')
"

# Test AI client
python -c "
from src.main import SimpleAIClient
client = SimpleAIClient()
response = client.generate('Test prompt')
print(f'Response: {response[:100]}...')
"
```

## 🔧 Debugging

### Logging

```python
import logging

# Configurazione logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(message)s'
)

# Log specifici
logger.debug(f"Searching with engine: {engine_name}")
logger.info(f"Found {len(results)} results")
logger.warning(f"Engine {engine} failed: {error}")
logger.error(f"Critical error: {error}")
```

### Debug Mode

```bash
# Abilita debug completo
LOG_LEVEL=DEBUG python src/main.py

# Debug specifico componente
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.config import config
print(config.validate())
"
```

## 📈 Performance

### Ottimizzazioni

1. **Deduplicazione**: Rimozione risultati duplicati
2. **Caching**: Cache risultati per query simili
3. **Parallelizzazione**: Ricerche concorrenti
4. **Timeout**: Gestione timeout intelligente

### Metriche

```python
# Metriche performance
execution_time = time.time() - start_time
results_per_second = len(results) / execution_time
success_rate = len(successful_engines) / len(total_engines)
```

## 🔒 Sicurezza

### Best Practices

1. **API Keys**: Mai hardcodate nel codice
2. **Validazione**: Controllo input utente
3. **Sanitizzazione**: Pulizia dati ricevuti
4. **Rate Limiting**: Limitazione richieste

### Vulnerabilità Note

- **SSRF**: Validazione URL prima delle richieste
- **Injection**: Sanitizzazione query di ricerca
- **Information Disclosure**: Logging sicuro

## 🚀 Deployment

### Docker (Futuro)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY env.example .env

CMD ["python", "src/main.py"]
```

### CI/CD (Futuro)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python -m pytest tests/
```

## 📚 Risorse

### Documentazione

- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Requests Library](https://requests.readthedocs.io/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Strumenti Utili

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

### Community

- [GitHub Issues](https://github.com/yourusername/ai-search-app/issues)
- [GitHub Discussions](https://github.com/yourusername/ai-search-app/discussions)
- [Contributing Guidelines](CONTRIBUTING.md)

---

**💡 Suggerimento**: Mantieni sempre aggiornate le dipendenze e segui le best practices di sicurezza! 