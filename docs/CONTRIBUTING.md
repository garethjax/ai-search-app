# 🤝 Contribuire - Research Assistant CLI

Grazie per il tuo interesse a contribuire al progetto! Questo documento ti guiderà attraverso il processo di contribuzione.

## 📋 Come Contribuire

### 🐛 Segnalare Bug

1. **Cerca** se il bug è già stato segnalato nelle [Issues](https://github.com/yourusername/ai-search-app/issues)
2. **Crea** una nuova issue con:
   - **Titolo** descrittivo
   - **Descrizione** dettagliata del problema
   - **Steps to reproduce** (passi per riprodurre)
   - **Expected vs Actual** (comportamento atteso vs reale)
   - **Environment** (sistema operativo, versione Python, etc.)

### 💡 Proporre Feature

1. **Discuti** l'idea nelle [Discussions](https://github.com/yourusername/ai-search-app/discussions)
2. **Crea** una issue con tag `enhancement`
3. **Descrivi** il caso d'uso e i benefici
4. **Aspetta** feedback dalla community

### 🔧 Sviluppare

#### Setup Sviluppo

```bash
# 1. Fork del repository
# Vai su GitHub e clicca "Fork"

# 2. Clona il tuo fork
git clone https://github.com/YOUR_USERNAME/ai-search-app.git
cd ai-search-app

# 3. Aggiungi upstream
git remote add upstream https://github.com/original-owner/ai-search-app.git

# 4. Crea branch per la feature
git checkout -b feature/amazing-feature

# 5. Setup ambiente
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### Workflow di Sviluppo

```bash
# 1. Aggiorna main
git checkout main
git pull upstream main

# 2. Crea branch feature
git checkout -b feature/your-feature-name

# 3. Sviluppa e testa
# ... fai le modifiche ...

# 4. Commit con messaggio chiaro
git add .
git commit -m "feat: add support for new search engine"

# 5. Push al tuo fork
git push origin feature/your-feature-name

# 6. Crea Pull Request
# Vai su GitHub e clicca "New Pull Request"
```

### 📝 Convenzioni

#### Commit Messages

Usa il formato [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat(search): add support for new search engine
fix(config): resolve API key validation issue
docs(readme): update installation instructions
test(api): add unit tests for Brave search
refactor(core): simplify configuration management
```

**Tipi**:
- `feat`: Nuova feature
- `fix`: Bug fix
- `docs`: Documentazione
- `style`: Formattazione (spazi, etc.)
- `refactor`: Refactoring codice
- `test`: Test
- `chore`: Task di manutenzione

#### Code Style

- **Python**: Segui [PEP 8](https://pep8.org/)
- **Naming**: `snake_case` per funzioni/variabili, `PascalCase` per classi
- **Docstrings**: Usa docstrings per funzioni e classi
- **Type Hints**: Aggiungi type hints dove possibile

```python
def search_web(query: str, max_results: int = 10) -> List[SearchResult]:
    """
    Search the web using multiple search engines.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of search results
        
    Raises:
        SearchError: If no search engines are available
    """
    pass
```

#### Testing

```bash
# Esegui tutti i test
python -m pytest tests/

# Test con coverage
python -m pytest --cov=src tests/

# Test specifici
python -m pytest tests/test_search.py::test_brave_search
```

### 🚀 Pull Request

#### Checklist PR

- [ ] **Codice** funziona e passa i test
- [ ] **Documentazione** aggiornata
- [ ] **Test** aggiunti per nuove funzionalità
- [ ] **Commit messages** seguono le convenzioni
- [ ] **Code review** completata
- [ ] **CI/CD** passa tutti i check

#### Template PR

```markdown
## 📝 Descrizione

Breve descrizione delle modifiche.

## 🔧 Tipo di Modifica

- [ ] Bug fix
- [ ] Nuova feature
- [ ] Breaking change
- [ ] Documentazione
- [ ] Test

## 🧪 Test

- [ ] Test unitari passano
- [ ] Test di integrazione passano
- [ ] Test manuali completati

## 📚 Documentazione

- [ ] README aggiornato
- [ ] Commenti codice aggiunti
- [ ] API documentation aggiornata

## 🔍 Checklist

- [ ] Codice segue le convenzioni del progetto
- [ ] Self-review completata
- [ ] Commenti aggiunti per codice complesso
- [ ] Test aggiunti per nuove funzionalità
- [ ] Documentazione aggiornata

## 📸 Screenshots (se applicabile)

Aggiungi screenshot per cambiamenti UI.

## 🔗 Issue Relate

Closes #123
```

## 🏗️ Architettura del Progetto

### Struttura File

```
ai-search-app/
├── src/                    # Codice sorgente
│   ├── main.py            # Entry point
│   ├── config.py          # Configurazione
│   └── __init__.py        # Package init
├── tests/                 # Test unitari
│   ├── test_config.py
│   ├── test_search.py
│   └── conftest.py
├── docs/                  # Documentazione
│   ├── api.md
│   └── deployment.md
├── examples/              # Esempi di utilizzo
├── requirements.txt       # Dipendenze
├── setup.py              # Setup package
└── README.md             # Documentazione principale
```

### Componenti Principali

1. **Configuration Manager** (`src/config.py`)
   - Gestione variabili d'ambiente
   - Validazione configurazione
   - Supporto multi-ambiente

2. **Search Engine Manager** (`src/main.py`)
   - Orchestrazione motori di ricerca
   - Deduplicazione risultati
   - Gestione errori

3. **AI Client** (`src/main.py`)
   - Interfaccia LLM locali
   - Gestione prompt
   - Generazione risposte

## 🧪 Testing

### Test Unitari

```python
# tests/test_search.py
import pytest
from src.main import EnhancedPerplexityResearcher

def test_brave_search():
    """Test Brave search functionality"""
    researcher = EnhancedPerplexityResearcher(None)
    results = researcher._search_brave_enhanced("test query")
    assert isinstance(results, list)
    assert len(results) >= 0
```

### Test di Integrazione

```python
# tests/test_integration.py
def test_full_research_workflow():
    """Test complete research workflow"""
    # Setup
    researcher = EnhancedPerplexityResearcher(mock_ai_client)
    
    # Execute
    result = researcher.research("test query")
    
    # Assert
    assert result.query == "test query"
    assert len(result.sources) > 0
    assert result.confidence > 0
```

### Test Performance

```python
# tests/test_performance.py
def test_search_performance():
    """Test search performance benchmarks"""
    start_time = time.time()
    result = researcher.research("performance test")
    execution_time = time.time() - start_time
    
    assert execution_time < 30  # Max 30 seconds
    assert len(result.sources) >= 3  # Min 3 sources
```

## 📚 Documentazione

### Aggiornare Documentazione

1. **README.md**: Documentazione principale
2. **DEVELOPMENT.md**: Guida sviluppatori
3. **SECURITY.md**: Best practices sicurezza
4. **API.md**: Documentazione API (futuro)

### Esempi di Codice

```python
# Esempio di utilizzo
from src.main import EnhancedPerplexityResearcher
from src.config import config

# Setup
researcher = EnhancedPerplexityResearcher(ai_client)

# Execute research
result = researcher.research("quantum computing 2024")

# Access results
print(f"Confidence: {result.confidence:.2%}")
print(f"Sources: {len(result.sources)}")
print(f"Answer: {result.answer}")
```

## 🔒 Sicurezza

### Reporting Vulnerabilità

Per vulnerabilità di sicurezza:
1. **NON** aprire issue pubblica
2. **Email** a: security@yourdomain.com
3. **Descrivi** la vulnerabilità in dettaglio
4. **Aspetta** risposta entro 48 ore

### Best Practices

- ✅ Validazione input utente
- ✅ Sanitizzazione dati
- ✅ Gestione sicura API keys
- ✅ Logging sicuro
- ❌ Mai hardcodare secrets
- ❌ Mai esporre dati sensibili

## 🎯 Roadmap

### Priorità Alta
- [ ] Supporto oobabooga/text-generation-webui
- [ ] Separazione prompt di sistema
- [ ] Miglioramento performance

### Priorità Media
- [ ] Web UI con link cliccabili
- [ ] API REST
- [ ] Plugin system

### Priorità Bassa
- [ ] Mobile app
- [ ] Desktop app
- [ ] Cloud deployment

## 🏆 Recognition

### Contributors

I contributori sono riconosciuti in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- README.md
- Release notes

### Badges

- **First PR**: Per il primo contributo
- **Bug Hunter**: Per bug fixes critici
- **Feature Creator**: Per nuove funzionalità
- **Documentation Hero**: Per miglioramenti docs

## 📞 Supporto

### Canali di Comunicazione

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-search-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-search-app/discussions)
- **Email**: dev@yourdomain.com
- **Discord**: [Server Discord](https://discord.gg/your-server)

### Mentorship

Per nuovi contributori:
1. **Issues** con tag `good first issue`
2. **Documentazione** dettagliata
3. **Code review** costruttiva
4. **Mentorship** program

---

**🎉 Grazie per contribuire al progetto! Ogni contributo, grande o piccolo, è apprezzato!** 