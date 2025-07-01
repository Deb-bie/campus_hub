from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError # type: ignore
from app.config import config
from app.models.event_model import Event
from app.utils.exceptions import SearchServiceError
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ElasticsearchService:
    def __init__(self):
        self.client = Elasticsearch([{
            'host': config.ELASTICSEARCH_HOST,
            'port': config.ELASTICSEARCH_PORT,
            'scheme': config.ELASTICSEARCH_SCHEME
        }])
        self.index_name = config.ELASTICSEARCH_INDEX
        self._ensure_index_exists()
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        if not self.client.indices.exists(index=self.index_name):
            mapping = {
                'mappings': {
                    'properties': {
                        'name': {
                            'type': 'text',
                            'analyzer': 'standard',
                            'fields': {'keyword': {'type': 'keyword'}}
                        },
                        'description': {'type': 'text'},
                        'short_description': {'type': 'text'},
                        'organizer_id': {'type': 'keyword'},
                        'location': {'type': 'text'},
                        'start_time': {'type': 'date'},
                        'end_time': {'type': 'date'},
                        'category': {'type': 'keyword'},
                        'image_url': {'type': 'text'},
                        'capacity': {'type': 'double'},
                        'is_public': {'type': 'boolean'},
                        'is_virtual': {'type': 'boolean'},
                        'is_recurring': {'type': 'boolean'},
                        'is_free': {'type': 'boolean'},
                        'created_at': {'type': 'date'},
                        'updated_at': {'type': 'date'},
                        'virtual_meeting_link': {'type': 'text'},
                        'tags': {'type': 'keyword'},
                        'status': {'type': 'keyword'},
                        'fee': {'type': 'double'},
                    }
                }
            }
            
            try:
                self.client.indices.create(index=self.index_name, body=mapping)
                logger.info(f"Created index: {self.index_name}")
            except RequestError as e:
                logger.error(f"Failed to create index: {e}")
                raise SearchServiceError(f"Failed to create index: {e}")
    
    def save_event(self, event: Event) -> Event:
        """Save an event to Elasticsearch"""
        try:
            event_dict = event.to_dict()
            response = self.client.index(
                index=self.index_name,
                body=event_dict
            )
            
            event.id = response['_id']
            return event
        except Exception as e:
            logger.error(f"Failed to save product: {e}")
            raise SearchServiceError(f"Failed to save product: {e}")
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Get an event by ID"""
        try:
            response = self.client.get(index=self.index_name, id=event_id)
            event_data = response['_source']
            event_data['id'] = response['_id']
            return Event.from_dict(event_data)
        except NotFoundError:
            return None
        except Exception as e:
            logger.error(f"Failed to get product: {e}")
            raise SearchServiceError(f"Failed to get product: {e}")
    
    def search_events(self, query: str) -> List[Dict]:
        """Simple text search"""
        try:
            search_body = {
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': ['name^2', 'description'],
                        'fuzziness': 'AUTO'
                    }
                }
            }
            
            response = self.client.search(index=self.index_name, body=search_body)
            return self._format_search_results(response)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise SearchServiceError(f"Search failed: {e}")
    
    def advanced_search(self, **kwargs) -> Dict:
        """Advanced search with filters and pagination"""
        try:
            query = kwargs.get('query')
            category = kwargs.get('category')
            location = kwargs.get('location')
            is_public = kwargs.get('is_public')
            is_virtual = kwargs.get('is_virtual')
            is_recurring = kwargs.get('is_recurring')
            is_free = kwargs.get('is_free')
            tags = kwargs.get('tags')
            status = kwargs.get('status')
            fee = kwargs.get('fee')
            page = kwargs.get('page', 1)
            size = kwargs.get('size', config.DEFAULT_PAGE_SIZE)
            
            search_body = self._build_search_query(
                query, category, location, is_public, is_virtual, is_recurring, is_free, tags, status, fee, page, size
            )
            
            response = self.client.search(index=self.index_name, body=search_body)
            
            return {
                'events': self._format_search_results(response),
                'total': response['hits']['total']['value'],
                'page': page,
                'size': size,
                'total_pages': (response['hits']['total']['value'] + size - 1) // size
            }
        except Exception as e:
            logger.error(f"Advanced search failed: {e}")
            raise SearchServiceError(f"Advanced search failed: {e}")
    
    def _build_search_query(self, query, category, min_price, max_price, page, size):
        """Build Elasticsearch query"""
        search_body = {
            'query': {'bool': {'must': [], 'filter': []}},
            'from': (page - 1) * size,
            'size': size,
            'sort': [
                {'_score': {'order': 'desc'}},
                {'created_date': {'order': 'desc'}}
            ]
        }
        
        # Text search
        if query:
            search_body['query']['bool']['must'].append({
                'multi_match': {
                    'query': query,
                    'fields': ['name^2', 'description'],
                    'fuzziness': 'AUTO'
                }
            })
        
        # Category filter
        if category:
            search_body['query']['bool']['filter'].append({
                'term': {'category': category}
            })
        
        # If no query, match all
        if not search_body['query']['bool']['must']:
            search_body['query'] = {'match_all': {}}
        
        return search_body
    
    def _format_search_results(self, response):
        """Format search results"""
        return [
            {
                'id': hit['_id'],
                'score': hit['_score'],
                **hit['_source']
            }
            for hit in response['hits']['hits']
        ]
    
    def get_aggregations(self) -> Dict:
        """Get aggregations for faceted search"""
        try:
            search_body = {
                'size': 0,
                'aggs': {
                    'categories': {
                        'terms': {'field': 'category', 'size': 20}
                    }
                }
            }
            
            response = self.client.search(index=self.index_name, body=search_body)
            return response['aggregations']
        except Exception as e:
            logger.error(f"Aggregation failed: {e}")
            raise SearchServiceError(f"Aggregation failed: {e}")
    
    def health_check(self) -> bool:
        """Check Elasticsearch connection"""
        try:
            return self.client.ping()
        except Exception:
            return False


