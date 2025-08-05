# standalone_research.py
import logging
import json
import os
import re
import time
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import random
from urllib.parse import urlparse
import hashlib
import sys

from dotenv import load_dotenv
load_dotenv()

# Import configuration
from config import config

def setup_cli_logging(verbose=False):
    # Use configuration for log level
    if verbose:
        level = logging.DEBUG
    else:
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        level = level_map.get(config.app.log_level, logging.INFO)

    class ColoredFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green  
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[35m', # Magenta
            'RESET': '\033[0m'
        }

        def format(self, record):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
            return super().format(record)

    logging.basicConfig(
        level=level,
        format='%(levelname)s | %(message)s',
        handlers=[logging.StreamHandler()]
    )

    for handler in logging.root.handlers:
        handler.setFormatter(ColoredFormatter('%(levelname)s | %(message)s'))

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    title: str
    snippet: str
    url: str
    source_engine: str
    timestamp: str
    content_length: int = 0
    domain: str = ""

    def __post_init__(self):
        self.content_length = len(self.snippet)
        try:
            parsed = urlparse(self.url)
            self.domain = parsed.netloc
        except:
            self.domain = "unknown"

@dataclass
class SearchStats:
    engines_tried: List[str]
    engines_successful: List[str]
    total_results_found: int
    unique_results: int
    domains_found: List[str]
    search_duration: float
    queries_used: List[str]

@dataclass
class ResearchAnswer:
    query: str
    answer: str
    sources: List[SearchResult]
    citations: List[int]
    confidence: float
    execution_time: float
    search_stats: SearchStats
    raw_sources_data: List[Dict]

class SimpleAIClient:
    def __init__(self, model=None):
        self.base_url = config.llm.ollama_base_url
        self.model = model or config.llm.ollama_model

    def generate(self, prompt: str, temperature: float = 0.3, num_predict: int = 1000) -> str:
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": num_predict
            }
            logger.debug(f"   🤖 Requesting Ollama generation with {self.model}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        full_response += data["response"]
                    if data.get("done", False):
                        break
            logger.debug(f"   ✅ Ollama generation completed: {len(full_response)} chars")
            return full_response.strip()
        except requests.exceptions.ConnectionError:
            logger.error("   ❌ Could not connect to Ollama. Is it running?")
            raise Exception("Ollama service not available - please start Ollama first")
        except Exception as e:
            logger.error(f"   ❌ Ollama generation failed: {str(e)}")
            raise Exception(f"Ollama generation failed: {str(e)}")

class EnhancedPerplexityResearcher:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        self.search_engines = [
            {'name': 'searx_multi', 'method': self._search_searx_enhanced, 'priority': 4},
            {'name': 'yahoo_enhanced', 'method': self._search_yahoo_enhanced, 'priority': 3},
            {'name': 'brave_enhanced', 'method': self._search_brave_enhanced, 'priority': 1},
            {'name': 'startpage', 'method': self._search_startpage, 'priority': 5},
            {'name': 'yandex', 'method': self._search_yandex, 'priority': 6},
            {'name': 'duckduckgo_fallback', 'method': self._search_duckduckgo_safe, 'priority': 7}
        ]

    # ===== METODI DI SEARCH ENGINE ======
    def _search_searx_enhanced(self, query: str) -> List[SearchResult]:
        instances = config.get_searx_instances()
        time_range = None
        match = re.search(r'\b(1d|1w|1m|1y)\b', query)
        if match:
            keyword = match.group(1)
            time_map = {'1d': 'day', '1w': 'week', '1m': 'month', '1y': 'year'}
            time_range = time_map.get(keyword)
            query = re.sub(r'\b' + re.escape(keyword) + r'\b', '', query).strip()
        for i, instance in enumerate(instances):
            try:
                url = f"{instance}/search"
                params = {
                    'q': query,
                    'format': 'json',
                    'language': 'en',
                    'engines': 'google,bing,yahoo',
                    'categories': 'general'
                }
                if time_range:
                    params['time_range'] = time_range
                logger.debug(f"         🌐 Instance {i+1}: {instance}")
                response = self.session.get(url, params=params, timeout=12)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        raw_results = data.get('results', [])
                        logger.debug(f"         📥 Raw results: {len(raw_results)}")
                        results = []
                        for item in raw_results[:6]:
                            title = item.get('title', '').strip()
                            content = item.get('content', '').strip()
                            url_item = item.get('url', '').strip()
                            if title and content and url_item and len(title) > 5:
                                result = SearchResult(
                                    title=title,
                                    snippet=content[:400],
                                    url=url_item,
                                    source_engine=f"searx_{instance.split('//')[1].split('.')[0]}",
                                    timestamp=datetime.now().isoformat()
                                )
                                results.append(result)
                        if results:
                            return results
                    except Exception as e:
                        logger.debug(f"         ❌ SearX {instance}: JSON decode error - {e}")
                        continue
            except Exception as e:
                logger.debug(f"         ❌ SearX {instance}: Exception - {e}")
                continue
        logger.debug(f"      ❌ SearX: All instances failed")
        return []

    def _search_yahoo_enhanced(self, query: str) -> List[SearchResult]:
        try:
            url = "https://search.yahoo.com/search"
            params = {
                'p': query,
                'ei': 'UTF-8',
                'fr': 'yfp-t',
                'b': 1
            }
            logger.debug(f"      🌐 Yahoo: Searching for '{query}'")
            response = self.session.get(url, params=params, timeout=12)
            if response.status_code == 200:
                logger.debug(f"      📥 Yahoo: Got response ({len(response.text)} chars)")
                results = self._parse_yahoo_results_enhanced(response.text, query)
                if results:
                    return results
        except Exception as e:
            logger.debug(f"      ❌ Yahoo: Exception - {e}")
        return []

    def _search_brave_enhanced(self, query: str) -> List[SearchResult]:
        api_key = config.get_brave_api_key()
        if not api_key:
            logger.debug("❌ BRAVE_API_KEY not set in environment variables.")
            return []
        time_map = {'1d': 'pd', '1w': 'pw', '1m': 'pm', '1y': 'py'}
        freshness = None
        match = re.search(r'\b(1d|1w|1m|1y)\b', query)
        if match:
            freshness = time_map.get(match.group(1))
            query = re.sub(r'\b' + re.escape(match.group(1)) + r'\b', '', query).strip()
        endpoint = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key
        }
        params = {
            "q": query,
            "count": 10,
            "country": "US",
            "search_lang": "en",
            "ui_lang": "en-US",
            "safesearch": "moderate"
        }
        if freshness:
            params["freshness"] = freshness
        try:
            response = self.session.get(endpoint, headers=headers, params=params, timeout=12)
            if response.status_code != 200:
                logger.debug(f"❌ Brave API: HTTP {response.status_code}")
                return []
            data = response.json()
            web = data.get("web", {})
            items = []
            if isinstance(web, dict) and isinstance(web.get("results"), list):
                items = web.get("results")
            elif isinstance(data.get("results"), list):
                items = data.get("results")
            results = []
            for item in items[:6]:
                title = item.get("title", "").strip()
                content = item.get("description", item.get("snippet", "")).strip()
                url_item = item.get("url", "").strip()
                if title and url_item:
                    results.append(SearchResult(
                        title=title,
                        snippet=content[:400],
                        url=url_item,
                        source_engine="brave_api",
                        timestamp=datetime.now().isoformat()
                    ))
            return results
        except Exception as e:
            logger.debug(f"❌ Exception from Brave API: {e}")
            return []

    def _search_startpage(self, query: str) -> List[SearchResult]:
        try:
            url = "https://www.startpage.com/sp/search"
            params = {
                'query': query,
                'cat': 'web',
                'pl': 'opensearch',
                'language': 'english'
            }
            logger.debug(f"      🌐 Startpage: Searching for '{query}'")
            response = self.session.get(url, params=params, timeout=12)
            if response.status_code == 200:
                logger.debug(f"      📥 Startpage: Got response ({len(response.text)} chars)")
                results = self._parse_startpage_results(response.text, query)
                if results:
                    return results
        except Exception as e:
            logger.debug(f"      ❌ Startpage: Exception - {e}")
        return []

    def _search_yandex(self, query: str) -> List[SearchResult]:
        try:
            url = "https://yandex.com/search/"
            params = {
                'text': query,
                'lr': 21,
                'lang': 'en'
            }
            logger.debug(f"      🌐 Yandex: Searching for '{query}'")
            response = self.session.get(url, params=params, timeout=12)
            if response.status_code == 200:
                logger.debug(f"      📥 Yandex: Got response ({len(response.text)} chars)")
                results = self._parse_yandex_results(response.text, query)
                if results:
                    return results
        except Exception as e:
            logger.debug(f"      ❌ Yandex: Exception - {e}")
        return []

    def _search_duckduckgo_safe(self, query: str) -> List[SearchResult]:
        try:
            from duckduckgo_search import DDGS
            logger.debug(f"      🌐 DuckDuckGo: Searching for '{query}'")
            time.sleep(random.uniform(2, 4))
            with DDGS() as ddgs:
                results = []
                search_results = ddgs.text(query, max_results=4)
                for result in search_results:
                    if result and isinstance(result, dict):
                        search_result = SearchResult(
                            title=result.get('title', '').strip(),
                            snippet=result.get('body', '').strip()[:400],
                            url=result.get('href', ''),
                            source_engine='duckduckgo',
                            timestamp=datetime.now().isoformat()
                        )
                        results.append(search_result)
                if results:
                    return results
        except ImportError:
            logger.debug(f"      ❌ DuckDuckGo: Library not available")
        except Exception as e:
            logger.debug(f"      ❌ DuckDuckGo: Exception - {e}")
        return []

    # =========== PARSER HTML ================
    def _parse_yahoo_results_enhanced(self, html: str, query: str) -> List[SearchResult]:
        results = []
        patterns = [
            r'<div class="dd algo[^"]*"[^>]*>.*?<h3[^>]*><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></h3>.*?<p[^>]*class="fst"[^>]*>(.*?)</p>',
            r'<div[^>]*class="[^"]*algo[^"]*".*?<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?<span[^>]*class="[^"]*fst[^"]*"[^>]*>(.*?)</span>',
            r'<div class="algo.*?<h3[^>]*><a[^>]*href="([^"]*)"[^>]*>(.*?)</a></h3>.*?<div[^>]*>(.*?)</div>'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            for match in matches[:6]:
                if len(match) >= 3:
                    url, title, snippet = match[0], match[1], match[2]
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                    import html as html_module
                    title = html_module.unescape(title)
                    snippet = html_module.unescape(snippet)
                    if title and snippet and len(title) > 5 and len(snippet) > 10:
                        result = SearchResult(
                            title=title,
                            snippet=snippet[:400],
                            url=url,
                            source_engine='yahoo',
                            timestamp=datetime.now().isoformat()
                        )
                        results.append(result)
            if results:
                break
        return results[:5]

    def _parse_startpage_results(self, html: str, query: str) -> List[SearchResult]:
        results = []
        try:
            pattern = r'<div class="w-gl__result__main">.*?<h3.*?><a.*?href="([^"]*)".*?>(.*?)</a></h3>.*?<p class="w-gl__description">(.*?)</p>'
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            for match in matches[:5]:
                url, title, snippet = match
                import html as html_module
                title = html_module.unescape(re.sub(r'<[^>]+>', '', title)).strip()
                snippet = html_module.unescape(re.sub(r'<[^>]+>', '', snippet)).strip()
                if title and snippet:
                    results.append(SearchResult(
                        title=title,
                        snippet=snippet,
                        url=url,
                        source_engine='startpage',
                        timestamp=datetime.now().isoformat()
                    ))
        except Exception as e:
            logger.debug(f"Startpage parsing failed: {e}")
        return results

    def _parse_yandex_results(self, html: str, query: str) -> List[SearchResult]:
        results = []
        try:
            pattern = r'<div class="serp-item.*?data-cid="([^"]*)".*?href="([^"]*)".*?<h2.*?>(.*?)</h2>.*?<div class="text-container.*?>(.*?)</div>'
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            for match in matches[:5]:
                cid, url, title, snippet = match
                import html as html_module
                title = html_module.unescape(re.sub(r'<[^>]+>', '', title)).strip()
                snippet = html_module.unescape(re.sub(r'<[^>]+>', '', snippet)).strip()
                if title and snippet and not url.startswith('javascript'):
                    results.append(SearchResult(
                        title=title,
                        snippet=snippet,
                        url=url if url.startswith('http') else f"https:{url}",
                        source_engine='yandex',
                        timestamp=datetime.now().isoformat()
                    ))
        except Exception as e:
            logger.debug(f"Yandex parsing failed: {e}")
        return results

    # ============ RESTO (metodi di orchestrazione)  ===========

    # (RIMUOVO PER BREVITA' qui i metodi research, deduplicate, generate_answer, ecc. che sono già corretti dal tuo codice)

    # Inserisci qui il resto dei tuoi metodi come erano prima (main loop, summary, ecc).
    # ...
    def research(self, query: str) -> ResearchAnswer:
        """Main research method with comprehensive logging"""
        start_time = time.time()
        logger.info(f"🔍 STARTING RESEARCH: '{query}'")
        logger.info(f"   📅 Timestamp: {datetime.now().isoformat()}")

        search_queries = self._generate_search_queries(query)
        logger.info(f"   📝 Generated {len(search_queries)} search queries: {search_queries}")

        search_results, search_stats = self._enhanced_web_search(search_queries)
        self._log_search_results(search_results, search_stats)
        answer_data = self._generate_answer_with_citations(query, search_results)
        execution_time = time.time() - start_time

        research_answer = ResearchAnswer(
            query=query,
            answer=answer_data['text'],
            sources=search_results,
            citations=answer_data['citations'],
            confidence=self._calculate_enhanced_confidence(search_results, search_stats),
            execution_time=execution_time,
            search_stats=search_stats,
            raw_sources_data=[asdict(result) for result in search_results]
        )

        logger.info(f"✅ RESEARCH COMPLETED in {execution_time:.2f}s")
        logger.info(f"   📊 Final confidence: {research_answer.confidence:.2%}")
        logger.info(f"   📚 Sources used: {len(search_results)}")
        logger.info(f"   🔗 Citations: {answer_data['citations']}")
        return research_answer

    def _generate_search_queries(self, query: str) -> List[str]:
        """Generate multiple search queries for comprehensive coverage"""
        base_query = query.strip()
        queries = [base_query]
        current_year = datetime.now().year
        queries.append(f"{base_query} {current_year}")
        unique_queries = []
        for q in queries:
            if q not in unique_queries and len(q.strip()) > 0:
                unique_queries.append(q.strip())
        return unique_queries[:4]

    def _enhanced_web_search(self, queries: List[str], max_results: int = 8) -> tuple[list, SearchStats]:
        search_start = time.time()
        all_results = []
        engines_tried = []
        engines_successful = []

        logger.info(f"🌐 STARTING WEB SEARCH")
        logger.info(f"   🎯 Queries: {len(queries)}")
        logger.info(f"   🔧 Engines available: {[e['name'] for e in self.search_engines]}")

        for query in queries:
            logger.info(f"\n   🔍 Searching for: '{query}'")
            for engine in self.search_engines:
                engine_name = engine['name']
                engines_tried.append(engine_name)
                logger.info(f"      🚀 Trying {engine_name}...")
                try:
                    results = engine['method'](query)
                    if results:
                        engines_successful.append(engine_name)
                        all_results.extend(results)
                        logger.info(f"      ✅ {engine_name}: Found {len(results)} results")
                        for i, result in enumerate(results):
                            logger.info(f"         [{i+1}] {result.title[:60]}...")
                            logger.info(f"             🔗 {result.url}")
                            logger.info(f"             📄 Snippet: {result.snippet[:100]}...")
                        break  # Stop trying other engines for this query
                    else:
                        logger.warning(f"      ⚠️ {engine_name}: No results found")
                except Exception as e:
                    logger.error(f"      ❌ {engine_name}: Error - {str(e)}")
                    continue

        unique_results = self._deduplicate_results_enhanced(all_results)
        domains = list(set([result.domain for result in unique_results if result.domain]))
        search_duration = time.time() - search_start

        search_stats = SearchStats(
            engines_tried=list(set(engines_tried)),
            engines_successful=list(set(engines_successful)),
            total_results_found=len(all_results),
            unique_results=len(unique_results),
            domains_found=domains,
            search_duration=search_duration,
            queries_used=queries
        )
        return unique_results[:max_results], search_stats

    def _log_search_results(self, results: List[SearchResult], stats: SearchStats):
        logger.info(f"\n📊 SEARCH STATISTICS:")
        logger.info(f"   ⏱️ Search duration: {stats.search_duration:.2f}s")
        logger.info(f"   🔧 Engines tried: {stats.engines_tried}")
        logger.info(f"   ✅ Engines successful: {stats.engines_successful}")
        logger.info(f"   📥 Total results found: {stats.total_results_found}")
        logger.info(f"   🔄 Unique results after dedup: {stats.unique_results}")
        logger.info(f"   🌐 Domains found: {stats.domains_found}")

        logger.info(f"\n📚 FINAL SEARCH RESULTS:")
        for i, result in enumerate(results, 1):
            logger.info(f"   [{i}] Title: {result.title}")
            logger.info(f"       🔗 URL: {result.url}")
            logger.info(f"       🏢 Domain: {result.domain}")
            logger.info(f"       🔧 Engine: {result.source_engine}")
            logger.info(f"       📏 Content length: {result.content_length} chars")
            logger.info(f"       📄 Snippet: {result.snippet[:150]}...")
            logger.info(f"       ⏰ Found at: {result.timestamp}")
            logger.info("")

    def _deduplicate_results_enhanced(self, results: List[SearchResult]) -> List[SearchResult]:
        logger.debug(f"   🔄 Deduplication: Starting with {len(results)} results")
        seen_urls = set()
        seen_content_hashes = set()
        seen_title_hashes = set()
        unique_results = []
        for result in results:
            if result.url in seen_urls:
                logger.debug(f"   ❌ Duplicate URL: {result.url}")
                continue
            content_text = f"{result.title} {result.snippet}".lower()
            content_hash = hashlib.md5(content_text.encode()).hexdigest()[:16]
            if content_hash in seen_content_hashes:
                logger.debug(f"   ❌ Duplicate content: {result.title[:40]}...")
                continue
            title_hash = hashlib.md5(result.title.lower().encode()).hexdigest()[:8]
            if title_hash in seen_title_hashes:
                logger.debug(f"   ❌ Similar title: {result.title[:40]}...")
                continue
            seen_urls.add(result.url)
            seen_content_hashes.add(content_hash)
            seen_title_hashes.add(title_hash)
            unique_results.append(result)
            logger.debug(f"   ✅ Unique result: {result.title[:40]}...")
        logger.debug(f"   🔄 Deduplication: {len(unique_results)}/{len(results)} unique results")
        return unique_results

    def _generate_answer_with_citations(self, query: str, sources: List[SearchResult]) -> Dict[str, Any]:
        logger.info(f"🧠 GENERATING ANSWER WITH CITATIONS")
        logger.info(f"   📚 Sources available: {len(sources)}")
        if not sources:
            logger.warning(f"   ⚠️ No sources available, generating fallback answer")
            return {
                'text': self._generate_fallback_answer(query),
                'citations': []
            }
        sources_text = ""
        for i, source in enumerate(sources, 1):
            source_info = f"\n[{i}] {source.title}\n{source.snippet}\nURL: {source.url}\nSource: {source.source_engine}\n"
            sources_text += source_info
            logger.debug(f"   📖 Source {i}: {source.title[:50]}... ({source.source_engine})")
        logger.info(f"   📝 Prepared {len(sources)} sources for AI analysis")
        
        # Load prompt template from file
        try:
            with open('prompts/research_assistant.txt', 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            prompt = prompt_template.format(query=query, sources_text=sources_text)
            logger.debug(f"   📝 Loaded prompt template from file")
        except FileNotFoundError:
            logger.warning(f"   ⚠️ Prompt file not found, using fallback")
            prompt = f"""You are a research assistant like Perplexity AI. Answer the question using the provided sources with citations.

QUESTION: {query}

SOURCES:
{sources_text}

INSTRUCTIONS:
1. Write a comprehensive, well-structured answer (2-3 paragraphs)
2. Use information from the sources naturally throughout your response
3. Add citations [1], [2], [3] etc. immediately after statements that reference specific sources
4. Be factual, objective, and accurate
5. If sources conflict, mention the different perspectives
6. If sources don't have complete information, acknowledge limitations
7. Focus on the most recent and reliable information

Write a clear, informative answer with proper citations:"""
        try:
            logger.info(f"   🤖 Requesting AI analysis...")
            response = self.ai_client.generate(
                prompt,
                temperature=0.3,
                num_predict=1000
            )
            logger.info(f"   ✅ AI response generated ({len(response)} chars)")
            citations = self._extract_citations_enhanced(response)
            logger.info(f"   🔗 Citations found: {citations}")
            valid_citations = [c for c in citations if 1 <= c <= len(sources)]
            if len(valid_citations) != len(citations):
                logger.warning(f"   ⚠️ Invalid citations removed: {set(citations) - set(valid_citations)}")
            return {
                'text': response.strip(),
                'citations': valid_citations
            }
        except Exception as e:
            logger.error(f"   ❌ Answer generation failed: {e}")
            return {
                'text': self._generate_fallback_answer(query),
                'citations': []
            }

    def _extract_citations_enhanced(self, text: str) -> List[int]:
        citations = []
        matches = re.findall(r'\[(\d+)\]', text)
        logger.debug(f"   🔍 Citation extraction: Found {len(matches)} citation markers")
        for match in matches:
            try:
                citation_num = int(match)
                if citation_num not in citations:
                    citations.append(citation_num)
                    logger.debug(f"   ✅ Valid citation: [{citation_num}]")
            except ValueError:
                logger.debug(f"   ❌ Invalid citation: [{match}]")
                continue
        return sorted(citations)

    def _generate_fallback_answer(self, query: str) -> str:
        logger.info(f"   🔄 Generating fallback answer for: {query}")
        
        # Load fallback prompt from file
        try:
            with open('prompts/fallback_answer.txt', 'r', encoding='utf-8') as f:
                fallback_template = f.read()
            return fallback_template.format(query=query)
        except FileNotFoundError:
            logger.warning(f"   ⚠️ Fallback prompt file not found, using hardcoded fallback")
            return f"""I don't have access to current web sources to provide a comprehensive answer about "{query}". 

To get accurate and up-to-date information on this topic, I recommend:
- Consulting authoritative sources and official websites
- Checking recent news reports from reputable outlets  
- Looking for expert analysis and academic sources
- Verifying information across multiple reliable sources

For rapidly changing topics, real-time information from trusted news sources and official statements would provide the most current details."""

    def _calculate_enhanced_confidence(self, sources: List[SearchResult], stats: SearchStats) -> float:
        if not sources:
            confidence = 0.3
            logger.info(f"   📊 Confidence (no sources): {confidence:.2%}")
            return confidence
        base_confidence = 0.6
        source_bonus = min(len(sources) * 0.08, 0.25)
        engine_diversity = len(set(source.source_engine for source in sources))
        diversity_bonus = min(engine_diversity * 0.05, 0.15)
        domain_diversity = len(set(source.domain for source in sources if source.domain))
        domain_bonus = min(domain_diversity * 0.03, 0.1)
        if stats.engines_successful:
            success_rate = len(stats.engines_successful) / len(stats.engines_tried)
            success_bonus = success_rate * 0.1
        else:
            success_bonus = 0
        avg_content_length = sum(len(source.snippet) for source in sources) / len(sources)
        quality_bonus = min(avg_content_length / 1000, 0.1)
        total_confidence = base_confidence + source_bonus + diversity_bonus + domain_bonus + success_bonus + quality_bonus
        final_confidence = min(total_confidence, 0.95)
        logger.info(f"   📊 Confidence calculation:")
        logger.info(f"      🔢 Base: {base_confidence:.2%}")
        logger.info(f"      📚 Sources ({len(sources)}): +{source_bonus:.2%}")
        logger.info(f"      🔧 Engine diversity ({engine_diversity}): +{diversity_bonus:.2%}")
        logger.info(f"      🌐 Domain diversity ({domain_diversity}): +{domain_bonus:.2%}")
        logger.info(f"      ✅ Search success: +{success_bonus:.2%}")
        logger.info(f"      📄 Content quality: +{quality_bonus:.2%}")
        logger.info(f"      🎯 FINAL: {final_confidence:.2%}")
        return final_confidence


def show_welcome():
    print("""
🔍 Research Assistant CLI
========================
This tool performs AI-powered web research using multiple search engines.
Before starting:
1. Make sure Ollama is installed and running (http://localhost:11434)
2. Optional: Set BRAVE_API_KEY environment variable for Brave Search
3. Required models: llama3:8b or mistral:latest or llama2:latest
Examples:
    python standalone_research.py "Latest developments in quantum computing"
    python standalone_research.py -v "Climate change effects 2024"
""")

def print_research_summary(research: ResearchAnswer):
    print("\n" + "="*80)
    print("🔍 RESEARCH SUMMARY")
    print("="*80)
    print(f"\n📋 QUERY: {research.query}")
    print(f"⏱️  EXECUTION TIME: {research.execution_time:.2f} seconds")
    print(f"🎯 CONFIDENCE: {research.confidence:.2%}")
    print(f"\n📊 SEARCH STATISTICS:")
    print(f"   🔧 Engines tried: {', '.join(research.search_stats.engines_tried)}")
    print(f"   ✅ Engines successful: {', '.join(research.search_stats.engines_successful)}")
    print(f"   📥 Total results found: {research.search_stats.total_results_found}")
    print(f"   🔄 Unique results: {research.search_stats.unique_results}")
    print(f"   🌐 Domains: {', '.join(research.search_stats.domains_found[:3])}{'...' if len(research.search_stats.domains_found) > 3 else ''}")
    print(f"   ⏱️  Search duration: {research.search_stats.search_duration:.2f}s")
    print(f"\n📚 SOURCES FOUND ({len(research.sources)}):")
    for i, source in enumerate(research.sources, 1):
        print(f"   [{i}] {source.title}")
        print(f"       🔗 {source.url}")
        print(f"       🏢 {source.domain} ({source.source_engine})")
        print(f"       📄 {source.snippet[:100]}...")
        print()
    print("💬 ANSWER:")
    print("-" * 80)
    print(research.answer)
    print("-" * 80)
    if research.citations:
        print(f"\n🔗 CITATIONS USED: {research.citations}")
    print("\n" + "="*80)

def get_research_options(use_defaults=True):
    """Get research options from user or use defaults"""
    options = {
        'verbose': False,
        'engines': "searx,brave,yahoo,startpage",
        'output': None
    }
    
    if not use_defaults:
        print("\n📋 Configure research options:")
        verbose = input("Enable verbose mode? (y/N): ").lower().startswith('y')
        engines = input("Search engines (default: searx,brave,yahoo,startpage): ").strip()
        output = input("Save results to file (optional, e.g. results.json): ").strip()
        
        options['verbose'] = verbose
        if engines:
            options['engines'] = engines
        if output:
            options['output'] = output
            
    return options

def main():
    # Validate configuration and show warnings
    warnings = config.validate()
    if warnings:
        print("\n⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    show_welcome()
    
    while True:
        # Ask for research mode
        print("\n🔧 Choose research mode:")
        print("1. Quick search (default options)")
        print("2. Custom search (configure options)")
        print("3. Exit")
        
        mode = input("➤ ").strip()
        
        if mode == "3":
            print("\n👋 Thank you for using Research Assistant!")
            break
            
        use_defaults = mode != "2"
        
        # Get research options
        options = get_research_options(use_defaults)
        
        while True:
            # Get query from user
            query = input("\n🔍 Enter your research query (or 'back' for options, 'exit' to quit):\n➤ ").strip()
            
            if query.lower() == 'exit':
                print("\n👋 Thank you for using Research Assistant!")
                return
                
            if query.lower() == 'back':
                break
                
            if not query:
                print("❌ Please enter a valid query")
                continue
            
            setup_cli_logging(options['verbose'])
            
            print("\n🚀 Starting Research Process")
            print("="*50)
            print(f"📝 Query: {query}")
            print(f"🔍 Engines: {options['engines']}")
            if options['output']:
                print(f"💾 Output: {options['output']}")
            print("="*50)
            
            try:
                # Check Ollama service
                try:
                    requests.get("http://localhost:11434/api/tags")
                    print("✅ Ollama service detected")
                except:
                    print("❌ Error: Ollama service not found")
                    print("Please install and start Ollama first: https://ollama.ai")
                    continue
                
                # Perform research
                ai_client = SimpleAIClient()
                researcher = EnhancedPerplexityResearcher(ai_client)
                
                if options['engines'] != "searx,brave,yahoo,startpage":
                    requested_engines = [e.strip() for e in options['engines'].split(",")]
                    researcher.search_engines = [
                        engine for engine in researcher.search_engines 
                        if any(req in engine['name'] for req in requested_engines)
                    ]
                    logger.info(f"🔧 Using engines: {[e['name'] for e in researcher.search_engines]}")
                
                print("\n🔍 Starting research...")
                result = researcher.research(query)
                print_research_summary(result)
                
                # Save results if requested
                if options['output']:
                    output_data = {
                        'query': result.query,
                        'answer': result.answer,
                        'sources': result.raw_sources_data,
                        'citations': result.citations,
                        'confidence': result.confidence,
                        'execution_time': result.execution_time,
                        'search_stats': asdict(result.search_stats),
                        'timestamp': datetime.now().isoformat()
                    }
                    with open(options['output'], 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, indent=2, ensure_ascii=False)
                    print(f"\n💾 Results saved to: {options['output']}")
                
                print(f"\n✅ Research completed successfully!")
                
                # Ask to continue
                cont = input("\nPress Enter for new search (or 'back' for options): ").strip().lower()
                if cont == 'back':
                    break
                
            except KeyboardInterrupt:
                print(f"\n⚠️ Research interrupted by user")
                break
            except Exception as e:
                logger.error(f"❌ Research failed: {e}")
                continue

if __name__ == "__main__":
    main()
