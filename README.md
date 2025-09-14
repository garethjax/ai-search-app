# 🔍 Research Assistant CLI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-🔒-orange.svg)](SECURITY.md)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/ai-search-app)

> Uno strumento CLI avanzato per ricerche web automatizzate con AI, che combina multiple fonti e genera risposte documentate con citazioni.

## ✨ Caratteristiche

- 🔍 **Ricerca Multi-Engine**: Google, Yahoo, Brave Search, Startpage, Yandex, DuckDuckGo
- 🤖 **AI Integration**: Supporto per Ollama e oobabooga/text-generation-webui
- 📚 **Citazioni Automatiche**: Risposte documentate con riferimenti alle fonti
- 🛡️ **Sicurezza Robusta**: Gestione sicura delle API keys tramite variabili d'ambiente
- ⚡ **Performance Ottimizzate**: Deduplicazione intelligente e caching
- 📊 **Statistiche Dettagliate**: Metriche complete su motori e risultati
- 💾 **Salvataggio Risultati**: Export in JSON per analisi successive
- 🌐 **Web UI** (Fase 5): Interfaccia web moderna con link cliccabili

## 🚀 Installazione Rapida

### Prerequisiti

- **Python 3.8+**
- **Ollama** (per AI locale) - [Scarica qui](https://ollama.ai)
- **Connessione Internet**

### Setup

1. **Clona il repository**
   ```bash
   git clone https://github.com/yourusername/ai-search-app.git
   cd ai-search-app
   ```

2. **Crea ambiente virtuale**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installa dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura le variabili d'ambiente**
   ```bash
   cp env.example .env
   # Modifica .env con le tue API keys
   ```

5. **Avvia Ollama**
   ```bash
   ollama run llama3.1:8b
   ```

## ⚙️ Configurazione

### Variabili d'Ambiente

Copia `env.example` in `.env` e configura:

```bash
# API Keys (opzionale ma raccomandato)
BRAVE_API_KEY=your_brave_api_key_here

# Configurazione LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Impostazioni Applicazione
LOG_LEVEL=INFO
DEFAULT_ENGINES=searx,brave,yahoo,startpage
MAX_RESULTS=8
REQUEST_TIMEOUT=12
```

### Brave Search API (Opzionale)

Per risultati migliori, ottieni una API key gratuita:
1. Vai su [Brave Search Settings](https://search.brave.com/settings)
2. Crea una nuova API key
3. Aggiungila al file `.env`

## 📖 Utilizzo

### Modalità Interattiva

```bash
python src/main.py
```

Seguire le istruzioni a schermo per:
- Scegliere modalità di ricerca (veloce/personalizzata)
- Inserire la query di ricerca
- Visualizzare risultati con citazioni

### Modalità Diretta

```bash
# Ricerca veloce
python src/main.py "Ultime novità sulla fusione nucleare"

# Modalità verbose
python src/main.py -v "Cambiamenti climatici 2024"
```

### Esempi di Query

```bash
# Ricerca generale
"Intelligenza artificiale nelle scuole italiane"

# Ricerca temporale
"Notizie coronavirus 1w"  # ultima settimana
"Elezioni USA 1m"         # ultimo mese

# Ricerca specifica
"Prezzi Bitcoin 2024"
"Nuove tecnologie quantum computing"
```

## 🔧 Motori di Ricerca

| Motore | Status | Caratteristiche |
|--------|--------|-----------------|
| **SearX** | ✅ Attivo | Multi-engine, privacy-focused |
| **Brave Search** | ✅ Attivo | API ufficiale, risultati accurati |
| **Yahoo** | ✅ Attivo | Ricerca web tradizionale |
| **Startpage** | ✅ Attivo | Privacy-friendly |
| **Yandex** | ✅ Attivo | Motore russo, buona copertura |
| **DuckDuckGo** | ✅ Attivo | Privacy-first, fallback |

## 🤖 Supporto AI

### Ollama (Predefinito)

```bash
# Modelli supportati
ollama run llama3.1:8b
ollama run mistral:latest
ollama run llama2:latest
```

### oobabooga/text-generation-webui

Configura nel file `.env`:
```bash
OOBABOOGA_BASE_URL=http://localhost:7860
OOBABOOGA_MODEL=your_model_name
```

## 📊 Output e Risultati

### Formato Risposta

```
🔍 RESEARCH SUMMARY
==========================================
📋 QUERY: Ultime novità sulla fusione nucleare
⏱️  EXECUTION TIME: 12.34 seconds
🎯 CONFIDENCE: 85%

📊 SEARCH STATISTICS:
   🔧 Engines tried: searx, brave, yahoo
   ✅ Engines successful: searx, brave
   📥 Total results found: 24
   🔄 Unique results: 8
   🌐 Domains: nature.com, science.org, ...

📚 SOURCES FOUND (8):
   [1] Breakthrough in Nuclear Fusion Technology
       🔗 https://nature.com/article/...
       🏢 nature.com (brave_api)
       📄 Recent developments in nuclear fusion...

💬 ANSWER:
------------------------------------------
Nuclear fusion research has seen significant breakthroughs in recent years [1], 
particularly in achieving net energy gain. The National Ignition Facility (NIF) 
reported a major milestone in 2022 [2], marking a crucial step toward...

🔗 CITATIONS USED: [1, 2, 3]
==========================================
```

### Salvataggio Risultati

```bash
# Salva in JSON
python src/main.py --output results.json "query"
```

Formato JSON:
```json
{
  "query": "Ultime novità sulla fusione nucleare",
  "answer": "Nuclear fusion research has seen...",
  "sources": [...],
  "citations": [1, 2, 3],
  "confidence": 0.85,
  "execution_time": 12.34,
  "search_stats": {...},
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🛠️ Sviluppo

### Struttura del Progetto

```
ai-search-app/
├── src/
│   ├── main.py          # Entry point principale
│   └── config.py        # Gestione configurazione
├── docs/                # 📚 Documentazione completa
│   ├── README.md        # Indice documentazione
│   ├── SECURITY.md      # Sicurezza e configurazione
│   ├── DEVELOPMENT.md   # Guida sviluppatori
│   ├── CONTRIBUTING.md  # Come contribuire
│   └── WEBUI_PLAN.md    # Piano Web UI
├── prompts/             # 📝 Prompt di sistema
│   ├── README.md        # Documentazione prompt
│   ├── research_assistant.txt  # Prompt principale
│   └── fallback_answer.txt     # Prompt di fallback
├── env.example          # Template variabili d'ambiente
├── requirements.txt     # Dipendenze Python
├── .gitignore          # File da ignorare
└── README.md           # Questo file
```

### 📚 Documentazione

Per informazioni dettagliate su sviluppo, contributi e piani futuri, consulta la [documentazione completa](docs/README.md).

### Contribuire

Per informazioni dettagliate su come contribuire, consulta la [guida completa](docs/CONTRIBUTING.md).

**Workflow rapido:**
1. **Fork** il repository
2. **Crea** un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

### Testing

```bash
# Test configurazione
python -c "from src.config import config; print(config.validate())"

# Test connessione Ollama
curl http://localhost:11434/api/tags
```

## 🔒 Sicurezza

- ✅ API keys gestite tramite variabili d'ambiente
- ✅ Validazione automatica della configurazione
- ✅ Protezione contro valori non validi
- ✅ Documentazione completa in [docs/SECURITY.md](docs/SECURITY.md)

## 🐛 Troubleshooting

### Problemi Comuni

| Problema | Soluzione |
|----------|-----------|
| **"Ollama service not found"** | Avvia Ollama: `ollama serve` |
| **"BRAVE_API_KEY not set"** | Aggiungi API key al file `.env` |
| **"No results found"** | Prova query più specifiche o diversi motori |
| **"Connection timeout"** | Verifica connessione internet e timeout |

### Logging

```bash
# Abilita debug mode
LOG_LEVEL=DEBUG python src/main.py

# Modalità verbose
python src/main.py -v "query"
```

## 📈 Roadmap

- [ ] **Fase 3**: Supporto per più software LLM locali
- [x] **Fase 4**: Separazione dei prompt di sistema ✅
- [ ] **Fase 5**: Web UI - Interfaccia grafica con link cliccabili
- [ ] **API REST**: Endpoint per integrazioni
- [ ] **Plugin System**: Estensioni personalizzate

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi [LICENSE](LICENSE) per dettagli.

## 🤝 Supporto

- 📧 **Issues**: [GitHub Issues](https://github.com/yourusername/ai-search-app/issues)
- 💬 **Discussioni**: [GitHub Discussions](https://github.com/yourusername/ai-search-app/discussions)
- 📖 **Documentazione**: [docs/](docs/) - Guida completa per sviluppatori e utenti

## 🙏 Ringraziamenti

- [Ollama](https://ollama.ai) per l'infrastruttura AI locale
- [Brave Search](https://search.brave.com) per l'API di ricerca
- [SearX](https://searx.github.io/searx/) per la privacy-first search
- Tutti i contributori e tester della community

## ✍️ Crediti

![Search Foundry](https://github.com/Search-Foundry/seo-tool-skeleton/raw/master/screenshots/SearchFoundryLogo.svg)


- A cura di [Martino Mosna](https://www.martinomosna.com), parte del collettivo [Search Foundry](https://www.searchfoundry.pro)


---
© 2025 Martino Mosna - Founding member of Search Foundry

Made with ❤️ and 🤖

Questo progetto è rilasciato a scopo didattico e sperimentale.

Se ti è stato utile, lascia una ⭐️ su GitHub!
