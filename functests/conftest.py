import logging
import os
import sys

logger = logging.getLogger(__name__)

print(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__)))

from functests.test_utils.data_fixtures import *  # noqa
from functests.test_utils.common_fixtures import *  # noqa

logging.basicConfig(level=logging.INFO, format='%(asctime)-1s [%(name)s] %(levelname)s %(message)s')
