import argparse
import logging
logger = logging.getLogger(__name__)

import sipyco.common_args as sca
from sipyco.pc_rpc import simple_server_loop
from itcm_artiq.devices.matthias_shutterbox.driver import MatthiasShutterBox

def get_argparser():
    parser = argparse.ArgumentParser(
        description = "ARTIQ controller for Matthias black box shutter box")
    parser.add_argument("-d", 
                        "--device",
                        default="COM10",
                        help = "device's hardware address")
    sca.simple_network_args(parser, 3782)
    sca.verbosity_args(parser)

    return parser

def main():
    args = get_argparser().parse_args()
    sca.init_logger_from_args(args)

    logger.info("Trying to establish connection "
                 "to shutter box at {}...".format(args.device))

    dev = MatthiasShutterBox(args.device)
    logger.info("Established connection.")

    try:
        logger.info("Starting server at port {}...".format(args.port))
        simple_server_loop({"MatthiasShutterBox":dev}, args.bind, args.port)
    finally:
        dev.close()

if __name__ == "__main__":
    main()