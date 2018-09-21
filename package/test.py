#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# print(os.path.dirname(__file__))
# print(os.path.abspath(__file__))
# print(os.path.basename(__file__))


current_dir = os.path.dirname(__file__)
parent_path = os.path.dirname(current_dir)
print(current_dir)
print(parent_path)
print(os.path.dirname(parent_path))
