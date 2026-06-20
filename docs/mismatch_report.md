# Mismatch Report

## Overview

This document tracks known mismatches between this implementation and the reference paper or other implementations.

## Known Mismatches

### 1. Synthetic Data vs Real Market Data

**Severity**: Low (Design Decision)

**Description**: The pipeline uses synthetic data for self-contained demonstration.

**Impact**: Results do not represent real market conditions.

**Resolution**: Users should provide real market data through custom pipeline integration.

### 2. Numerical Optimization Tolerance

**Severity**: Low

**Description**: Numerical solvers use default tolerances from SciPy.

**Impact**: May produce slightly different results across platforms.

**Resolution**: Configure solver tolerances if high precision is required.

### 3. CFVaR3 Mock Kappa3

**Severity**: Low (Demo Only)

**Description**: The demo pipeline uses a mock third-order cumulant function.

**Impact**: CFVaR3 results in demo are illustrative only.

**Resolution**: Provide real kappa3 function for production use.

## Potential Future Mismatches

### 1. Parallel Processing

**Status**: Not Implemented

**Description**: Large portfolio optimization could benefit from parallelization.

**Impact**: Performance for large-scale problems.

### 2. GPU Acceleration

**Status**: Not Implemented

**Description**: Matrix operations could be accelerated on GPU.

**Impact**: Computation time for very large portfolios.

## Reporting New Mismatches

If you discover a mismatch, please open an issue with:
- Description of the mismatch
- Steps to reproduce
- Expected vs actual behavior
- Impact assessment
