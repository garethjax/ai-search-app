# 🔒 Sicurezza - Research Assistant CLI

## Variabili d'Ambiente

### Configurazione Sicura

Il progetto utilizza variabili d'ambiente per gestire le informazioni sensibili. **Non committare mai** il file `.env` nel repository.

### File di Configurazione

- `.env` - **NON COMMITTARE** - Contiene le tue chiavi API personali
- `env.example` - Template per le variabili d'ambiente
- `.gitignore` - Protegge i file sensibili

### Variabili Richieste

#### API Keys
```bash
# Brave Search API (opzionale ma raccomandato)
BRAVE_API_KEY=your_brave_api_key_here
```

#### Configurazione LLM
```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# oobabooga/text-generation-webui (alternativa)
OOBABOOGA_BASE_URL=http://localhost:7860
OOBABOOGA_MODEL=your_model_name_here
```

#### Impostazioni Applicazione
```bash
# Logging
LOG_LEVEL=INFO

# Motori di ricerca
DEFAULT_ENGINES=searx,brave,yahoo,startpage

# Limiti
MAX_RESULTS=8
REQUEST_TIMEOUT=12
```

## Setup Sicuro

### 1. Copia il Template
```bash
cp env.example .env
```

### 2. Configura le Variabili
Modifica il file `.env` con le tue chiavi API:
```bash
# Esempio
BRAVE_API_KEY=sk-1234567890abcdef
```

### 3. Verifica la Configurazione
```bash
python -c "from src.config import config; config.validate()"
```

## Best Practices

### ✅ Cosa Fare
- Usa sempre variabili d'ambiente per le API keys
- Mantieni il file `.env` locale e non condividerlo
- Usa chiavi API diverse per ambienti diversi
- Verifica regolarmente la validità delle chiavi

### ❌ Cosa NON Fare
- Non committare mai il file `.env`
- Non hardcodare le API keys nel codice
- Non condividere le chiavi API pubblicamente
- Non usare chiavi di produzione in ambiente di sviluppo

## Troubleshooting

### Errore: "BRAVE_API_KEY not set"
**Soluzione**: Aggiungi la tua API key al file `.env`:
```bash
BRAVE_API_KEY=your_actual_api_key
```

### Errore: "Invalid configuration"
**Soluzione**: Verifica che tutte le variabili nel `.env` siano valide:
```bash
python -c "from src.config import config; print(config.validate())"
```

## Validazione Automatica

Il sistema valida automaticamente la configurazione all'avvio e mostra warning per:
- API keys mancanti
- Valori non validi
- Configurazioni incomplete

## Supporto

Per problemi di sicurezza o configurazione, apri una issue su GitHub. 