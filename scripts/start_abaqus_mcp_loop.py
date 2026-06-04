# -*- coding: utf-8 -*-
"""Start the Abaqus MCP plugin loop inside Abaqus/CAE noGUI."""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_HOME = os.environ.get("ABAQUS_MCP_HOME", PROJECT_ROOT)
os.environ["ABAQUS_MCP_HOME"] = MCP_HOME

SRC_DIR = os.path.join(MCP_HOME, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import abaqus_mcp_plugin

abaqus_mcp_plugin.mcp_loop()
