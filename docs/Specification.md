# RC5 Encryption with Cellular Automata Key Generation - Specification

## Overview

Implement a 16-bit RC5 encryption module that uses an 8-bit Cellular Automata (CA) module for key generation. The module should perform two rounds of RC5 encryption with proper state machine control.

## Module Interface

### rc5_enc_16bit

```systemverilog
module rc5_enc_16bit (
    input clock,           // Positive edge-triggered clock
    input reset,           // Asynchronous active low reset
    input enc_start,       // When HIGH, encryption begins
    input [15:0] p,       // Plaintext input
    output reg [15:0] c,   // Ciphertext output
    output reg enc_done    // When HIGH, indicates stable ciphertext output
);
```

## Requirements

1. **Key Generation**: Use the provided `CA_8bit` module to generate S-box values
   - Initialize CA with seed value `8'hFF`
   - Generate 6 S-box values (s[0] through s[5]) using the CA module
   - S-box generation should complete before encryption begins

2. **Encryption Algorithm**: Implement two rounds of RC5 encryption
   - **Initial Addition**: Add s[0] to upper 8 bits and s[1] to lower 8 bits
   - **Round 1**: 
     - Upper 8 bits: Rotate left by (lower 8 bits % 8), XOR with lower 8 bits, add s[2]
     - Lower 8 bits: Rotate left by (upper 8 bits % 8), XOR with upper 8 bits, add s[3]
   - **Round 2**:
     - Upper 8 bits: Rotate left by (lower 8 bits % 8), XOR with lower 8 bits, add s[4]
     - Lower 8 bits: Rotate left by (upper 8 bits % 8), XOR with upper 8 bits, add s[5]

3. **State Machine**: Implement a finite state machine to control:
   - S-box generation state
   - Initial addition state
   - Round 1 states (MSB and LSB computation)
   - Round 2 states (MSB and LSB computation)
   - Completion state

4. **Timing**:
   - `enc_done` should be asserted HIGH when encryption is complete
   - All operations should be synchronous to the positive edge of clock
   - Reset should initialize all state to known values

## CA_8bit Module

The `CA_8bit` module is provided and implements an 8-bit Cellular Automata with rule combination R90-R90-R150-R90-R150-R90-R150-R90.

### Interface
```systemverilog
module CA_8bit(
    input wire clock,
    input wire reset,
    input wire [7:0] CA_seed,
    output reg [7:0] CA_out
);
```

## Test Cases

The implementation will be tested with the following plaintext inputs:
- `0x1000` → Expected ciphertext: `0x9530`
- `0xFFFF` → Expected ciphertext: `0x58CB`
- `0x00FF` → Expected ciphertext: `0xAFE8`
- `0xFF00` → Expected ciphertext: `0x86CF`

## Implementation Notes

- Use modular arithmetic for 8-bit operations (modulo 256)
- Implement a rotate_left function for 8-bit left rotation
- Ensure proper state transitions and timing
- Handle reset condition correctly

