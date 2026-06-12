import argparse
import logging

import sipyco.common_args as sca
from sipyco.pc_rpc import simple_server_loop

from itcm_artiq.devices.ni_PCIe6738.driver import NI_PCIe6738Counter

logger = logging.getLogger(__name__)

def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for National Instruments 32 channel DAC")
    parser.add_argument ("-d",
                         "--device",
                         default="DC_DAC",
                         help="Device name set on NI MAX")
    sca.simple_network_args(parser, 3780)
    sca.verbosity_args(parser)

    return parser


def main():
    args= get_argparser().parse_args()
    sca.init_logger_from_args(args)

    logger.debug("Trying to establish connection to PCIe6738 card")
    counter = NI_PCIe6738Counter(args.device)
    logger.debug("Connection estabished.")

    try:
        logger.info("Starting server at port {}...".format(args.port))
        simple_server_loop({"pmt_counter": counter}, sca.bind_address_from_args(args), args.port)
    finally:
        counter.close()

if __name__ == "__main__":
    main()