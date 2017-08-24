#!/usr/bin/python3
# -*- coding: utf-8 -*-

def biweight(d):
    W = 0.1
    return ( 1 - (d/W) ** 2 ) ** 2 if abs(d/W) < 1 else 0
