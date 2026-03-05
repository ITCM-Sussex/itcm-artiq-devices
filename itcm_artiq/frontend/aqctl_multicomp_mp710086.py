#!/usr/bin/env python3

import argparse
import logging

import sipyco.common_args as sca
from sipyco.pc_rpc import simple_server_loop
from devices.multicomp_mp710086.driver import MulticompMP710086

def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for Multicomp MP710086 PSU")
    parser.add_argument("-d",
                        "--device",
                        default="USB0::0x5345::0x1235::2037801::INSTR",
                        help="hardware address of device")
    sca.simple_network_args(parser, 4310)
    sca.verbosity_args(parser)

    return parser


def main():
    args = get_argparser().parse_args()
    sca.init_logger_from_args(args)
    logging.info("Trying to establish connection "
                 "to Multicomp MP710086 PSU at {}...".format(args.device))
    dev = MulticompMP710086(args.device)
    logging.info("Established connection.")

    try:
        logging.info("Starting server at port {}...".format(args.port))
        simple_server_loop({"MulticompMP710086": dev}, sca.bind_address_from_args(args),
                           args.port)
    finally:
        dev.close()


if __name__ == "__main__":
    main()