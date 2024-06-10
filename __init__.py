from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict
from fastapi import FastAPI, Request, Response

