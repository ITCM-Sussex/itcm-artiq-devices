#!/usr/bin/env python3

import argparse
import logging
logger = logging.getLogger(__name__)

import sipyco.common_args as sca
from sipyco.pc_rpc import simple_server_loop
from devices.matthias_tdc.driver import MatthiasTDC

def get_argparser():
    parser = argparse.ArgumentParser(
        description = "ARTIQ controller for Matthias black box TDC")
    parser.add_argument("-d", "--device", help = "device's hardware address")
    sca.simple_network_args(parser, 4001)
    sca.verbosity_args(parser)

    return parser

def main():
    args = get_argparser().parse_args()
    sca.init_logger_from_args(args)

    dev = MatthiasTDC(args.device)

    try:
        simple_server_loop({"MatthiasTDC":dev}, args.bind, args.port)
    finally:
        dev.close()

if __name__ == "__main__":
    main()