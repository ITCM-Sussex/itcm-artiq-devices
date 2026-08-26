import argparse
import logging
logger = logging.getLogger(__name__)

import sipyco.common_args as sca
from sipyco.pc_rpc import simple_server_loop

from itcm_artiq.devices.andor_emccd.driver import AndorEMCCD

def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for Andor EMCCD")
    sca.simple_network_args(parser, 3781)
    sca.verbosity_args(parser)

    return parser

def main():
    args= get_argparser().parse_args()
    sca.init_logger_from_args(args)

    logger.debug("Trying to establish connection to Andor EMCCD")
    cam = AndorEMCCD()
    logger.debug("Connection estabished.")

    try:
        logger.info("Starting server at port {}...".format(args.port))
        simple_server_loop({"andor_emccd": cam}, sca.bind_address_from_args(args), args.port)
    finally:
        cam.close()

if __name__ == "__main__":
    main()