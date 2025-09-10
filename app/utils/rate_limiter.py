import time
from collections import defaultdict
from typing import Dict, List, Tuple

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize a rate limiter
        
        Args:
            max_requests: Maximum number of requests allowed in the time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_history: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if a request from the client is allowed
        
        Args:
            client_id: Identifier for the client (e.g., IP address)
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove requests outside the time window
        self.request_history[client_id] = [
            timestamp for timestamp in self.request_history[client_id]
            if current_time - timestamp <= self.time_window
        ]
        
        # Check if the client has exceeded the rate limit
        if len(self.request_history[client_id]) >= self.max_requests:
            return False
        
        # Add the current request to the history
        self.request_history[client_id].append(current_time)
        return True
    
    def get_remaining_requests(self, client_id: str) -> Tuple[int, int]:
        """
        Get the number of remaining requests for a client
        
        Args:
            client_id: Identifier for the client
            
        Returns:
            Tuple[int, int]: (remaining requests, seconds until reset)
        """
        current_time = time.time()
        
        # Remove requests outside the time window
        self.request_history[client_id] = [
            timestamp for timestamp in self.request_history[client_id]
            if current_time - timestamp <= self.time_window
        ]
        
        # Calculate remaining requests
        remaining = max(0, self.max_requests - len(self.request_history[client_id]))
        
        # Calculate seconds until reset
        if self.request_history[client_id]:
            oldest_request = min(self.request_history[client_id])
            reset_time = oldest_request + self.time_window - current_time
        else:
            reset_time = 0
        
        return remaining, int(reset_time)