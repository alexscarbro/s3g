"""
A set of functions to easily create ojects internalized in
makerbot_driver
"""

from __future__ import absolute_import
import threading

import makerbot_driver


def create_parser(machine_name, legacy=False):
    parser = makerbot_driver.Gcode.GcodeParser()
    if legacy:
        parser.state = makerbot_driver.Gcode.LegacyGcodeStates()
    else:
        parser.state = makerbot_driver.Gcode.GcodeStates()
    parser.state.profile = makerbot_driver.Profile(machine_name)
    return parser


def create_print_to_file_parser(filename, machine_name, legacy=False):
    parser = create_parser(machine_name, legacy)
    parser.s3g = makerbot_driver.s3g()
    condition = threading.Condition()
    parser.s3g.writer = makerbot_driver.Writer.FileWriter(open(filename, 'wb'), condition)
    return parser


def create_print_to_stream_parser(port, machine_name, legacy=False):
    parser = create_parser(machine_name, legacy)
    parser.s3g = makerbot_driver.s3g.from_filename(port)
    return parser


def create_eeprom_reader(port, firmware_verison=6.0, software_variant='00', working_directory=None):
    s3g = makerbot_driver.s3g.from_filename(port)
    reader = makerbot_driver.EEPROM.EepromReader.factory(
        s3g, firmware_verison, software_variant, working_directory)
    return reader


def create_eeprom_writer(port, firmware_version=6.0, software_variant='00', working_directory=None):
    s3g = makerbot_driver.s3g.from_filename(port)
    writer = makerbot_driver.EEPROM.EepromWriter.factory(
        s3g, firmware_version, software_variant, working_directory)
    return writer
