# -*- coding: utf-8 -*-

# ──────────────────────────────── Normalizers ─────────────────────────────── #

# Normalizers are defined here as functions that map a parameter-input domain to
# a function's domain, in effect "snapping" values to the closest acceptable
# value. For example, normalizing integer values to the closest odd integer
# value for window size parameters.

EVEN_NORMALIZER = lambda x: int(x)/2*2
ODD_NORMALIZER  = lambda x: int(x)/2*2+1

# ──────────────────────────────────────────────────────────────────────────── #