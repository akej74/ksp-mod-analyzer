"""
    settings.py
    -----------
    Implements functions for reading and writing UI configuration using a QSettings object.
"""


def read_settings(config, ui):
    """Read configuration from the OS repository (Registry in Windows, ini-file in Linux).

    Uses default values if no settings are found.

    "type=<type>" defines the data type.
    """
    print("Reading settings...")


def save_settings(config, ui):
    """Save current UI configuration to the OS repository, called when exiting the main application"""
    print("Saving settings...")
