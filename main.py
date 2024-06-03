import logging
from logging_config import logging_config  # Ensure the logging config is loaded
import time

# Create logger for main module
main_logger = logging.getLogger(__name__)

main_logger.debug("Debug message")
is_running = True

# manager =
# load manager by using setting file (create fake monitors, connect them to queue,
# then create senders [grpc, rabit, kafka, websocket, udp, tcp, http, etc])
# controllers =
# load controllers by using setting file (grpc, fastapi, rabit, or nothing)
while is_running:
    # Sleep for 1 second
    time.sleep(1)
    main_logger.info("Main loop running")