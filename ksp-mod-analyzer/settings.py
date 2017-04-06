"""
    settings.py
    -----------
    Implements functions for reading and writing UI configuration using a QSettings object.
    
    Currently not in use.
"""


def read_settings(config, ui):
    """Reads configuration from the OS repository (Registry in Windows, ini-file in Linux).

    Uses default values if no settings are found.

    "type=<type>" defines the data type.
    """
    print("Reading settings...")


def save_settings(config, ui):
    """Saves the current UI configuration to the OS repository, called when exiting the main application"""
    print("Saving settings...")
