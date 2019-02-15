import logging
import os
import sys

logger = logging.getLogger(__name__)

print(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO, format='%(asctime)-1s [%(name)s] %(levelname)s %(message)s')
