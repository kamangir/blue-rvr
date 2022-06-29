from . import *
from .utils import *
import abcli.logging
from abcli.logging import crash_report
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

logger.info("blue.drive(): started...")
show_help()

loop.run_in_executor(None, key_helper.get_key_continuous)
try:
    run_loop()
except Exception as e:
    logger.info("blue.drive() crashed: {}".format(e))
finally:
    logger.info("blue.drive(): ending...")
    key_helper.end_get_key_continuous()
    if camera_enabled:
        camera.close()

    try:
        looper.close()
    except:
        crash_report(f"{name}: close: failed.")

    logger.info("blue.drive(): ended - press any key...")

    exit(1)
