#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Part of academic course project at CMU in the course API Design and 
# Implementation - 17780 by Josh Bloch and Charlie Garrod.
# 
# Authors:
# - Vikramraj Sitpal
# - Chirag Sachdeva

from enum import Enum

class QuoteType(Enum):
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    CURRENCY = "CURRENCY"
    EQUITY = "EQUITY"
    ETF = "ETF"
    INDEX = "INDEX"
    MUTUALFUND = "MUTUALFUND"
    MISC = "MISC"

class Interval(Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    DAY_5 = "5d"
    WEEK_1 = "1wk"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"

class Duration(Enum):
    DAY_1 = "1d"
    DAY_5 = "5d"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"
    MONTH_6 = "6mo"
    YEAR_1 = "1y"
    YEAR_2 = "2y"
    YEAR_5 = "5y"
    YEAR_10 = "10y"
    YEAR_TO_DATE = "ytd"
    MAX = "max"

class Multiplier(Enum):
    ONCE = 1
    TWICE = 2
    THRICE = 3
    QUADRICE = 4
    HALF = 0.5
    QUARTER = 0.25