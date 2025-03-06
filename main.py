#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TheoryX Solver - AI-powered Theoretical Mechanics Problem Solver
Copyright (C) 2024 Rundao

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from frontend import solver_ui

if __name__ == "__main__":
    # 启动UI
    solver_ui.launch(
        server_name="0.0.0.0",
        server_port=7860
    )