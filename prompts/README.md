# 📝 Prompt di Sistema - Research Assistant CLI

Questa cartella contiene tutti i prompt di sistema utilizzati dal Research Assistant CLI. Separare i prompt dal codice li rende più manutenibili e permette modifiche senza toccare il codice.

## 📋 File Disponibili

### 🔍 **research_assistant.txt**
- **Scopo**: Prompt principale per generare risposte con citazioni
- **Utilizzo**: Quando ci sono fonti disponibili
- **Variabili**: `{query}`, `{sources_text}`
- **Output**: Risposta strutturata con citazioni [1], [2], [3]...

### 🔄 **fallback_answer.txt**
- **Scopo**: Risposta quando non ci sono fonti disponibili
- **Utilizzo**: Quando la ricerca non produce risultati
- **Variabili**: `{query}`
- **Output**: Messaggio informativo con raccomandazioni

## 🛠️ Come Modificare i Prompt

### 1. **Modifica Diretta**
```bash
# Modifica il prompt principale
nano prompts/research_assistant.txt

# Modifica il prompt di fallback
nano prompts/fallback_answer.txt
```

### 2. **Variabili Disponibili**

#### Per research_assistant.txt:
- `{query}` - La query di ricerca dell'utente
- `{sources_text}` - Testo formattato con tutte le fonti

#### Per fallback_answer.txt:
- `{query}` - La query di ricerca dell'utente

### 3. **Best Practices**

#### ✅ **Cosa Fare:**
- Mantieni le istruzioni chiare e concise
- Usa le variabili disponibili correttamente
- Testa le modifiche con query diverse
- Mantieni il formato delle citazioni [1], [2], [3]...

#### ❌ **Cosa Evitare:**
- Non rimuovere le variabili `{query}` e `{sources_text}`
- Non cambiare drasticamente la struttura delle citazioni
- Non rendere i prompt troppo lunghi o complessi
- Non aggiungere istruzioni che potrebbero confondere l'AI

## 🔧 Integrazione nel Codice

I prompt vengono caricati dinamicamente dal file `src/main.py`:

```python
# Carica il prompt principale
with open('prompts/research_assistant.txt', 'r', encoding='utf-8') as f:
    prompt_template = f.read()

# Sostituisce le variabili
prompt = prompt_template.format(
    query=query,
    sources_text=sources_text
)
```

## 📊 Struttura dei Prompt

### Prompt Principale
```
[Ruolo e contesto]
[Domanda]
[Fonti disponibili]
[Istruzioni dettagliate]
[Richiesta finale]
```

### Prompt di Fallback
```
[Messaggio di avviso]
[Raccomandazioni per l'utente]
[Fonti alternative suggerite]
```

## 🧪 Testing

Dopo aver modificato un prompt, testalo con:

```bash
# Test con query semplice
python src/main.py "test query"

# Test con query complessa
python src/main.py "ultime novità intelligenza artificiale 2024"
```

## 📈 Versioning

- **v1.0**: Prompt iniziali
- **v1.1**: Miglioramenti istruzioni citazioni
- **v1.2**: Aggiunta gestione conflitti fonti

## 🔄 Workflow di Modifica

1. **Modifica** il file di prompt desiderato
2. **Testa** con query diverse
3. **Verifica** che le citazioni funzionino
4. **Commit** le modifiche con messaggio descrittivo
5. **Documenta** eventuali cambiamenti significativi

---

**💡 Suggerimento**: Mantieni i prompt semplici e focalizzati. Un prompt troppo complesso può confondere l'AI e produrre risultati peggiori. 