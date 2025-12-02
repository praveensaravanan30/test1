import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,Timer


async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(1000):
        dut.clock.value = 0
        await Timer(5, unit="ns")
        dut.clock.value = 1
        await Timer(5, unit="ns")

@cocotb.test()
async def test_encryption_1(dut):
    """Test encryption with plaintext 0x1000"""

    await cocotb.start(generate_clock(dut))
    print("RC5 encryption");
    await Timer(5, unit="ns")  
    dut.reset.value = 0;
    dut.enc_start.value = 1;
    dut.p.value = 0x1000;
    await Timer(15, unit="ns")
    dut.reset.value = 1;
    await Timer(150, unit="ns")  
    dut._log.info("reset = %d, enc_start = %d, p = %x, c = %x, enc_done = %d",dut.reset.value,dut.enc_start.value,dut.p.value,dut.c.value,dut.enc_done.value)
    assert dut.c.value == 0x9530, "Ciphertext is not correct"   
   
@cocotb.test()
async def test_encryption_2(dut):
    """Test encryption with plaintext 0xFFFF"""

    await cocotb.start(generate_clock(dut))
    print("RC5 encryption");
    await Timer(5, unit="ns")  
    dut.reset.value = 0;
    dut.enc_start.value = 1;
    dut.p.value = 0xFFFF;
    await Timer(15, unit="ns")
    dut.reset.value = 1;
    await Timer(150, unit="ns")  
    dut._log.info("reset = %d, enc_start = %d, p = %x, c = %x, enc_done = %d",dut.reset.value,dut.enc_start.value,dut.p.value,dut.c.value,dut.enc_done.value)
    assert dut.c.value == 0x58CB, "Ciphertext is not correct"   
    
@cocotb.test()
async def test_encryption_3(dut):
    """Test encryption with plaintext 0x00FF"""

    await cocotb.start(generate_clock(dut))
    print("RC5 encryption");
    await Timer(5, unit="ns")  
    dut.reset.value = 0;
    dut.enc_start.value = 1;
    dut.p.value = 0x00FF;
    await Timer(15, unit="ns")
    dut.reset.value = 1;
    await Timer(150, unit="ns")  
    dut._log.info("reset = %d, enc_start = %d, p = %x, c = %x, enc_done = %d",dut.reset.value,dut.enc_start.value,dut.p.value,dut.c.value,dut.enc_done.value)
    assert dut.c.value == 0xAFE8, "Ciphertext is not correct"   
    
@cocotb.test()
async def test_encryption_4(dut):
    """Test encryption with plaintext 0xFF00"""

    await cocotb.start(generate_clock(dut))
    print("RC5 encryption");
    await Timer(5, unit="ns")  
    dut.reset.value = 0;
    dut.enc_start.value = 1;
    dut.p.value = 0xFF00;
    await Timer(15, unit="ns")
    dut.reset.value = 1;
    await Timer(150, unit="ns")  
    dut._log.info("reset = %d, enc_start = %d, p = %x, c = %x, enc_done = %d",dut.reset.value,dut.enc_start.value,dut.p.value,dut.c.value,dut.enc_done.value)
    assert dut.c.value == 0x86CF, "Ciphertext is not correct"   

# ✅ CRITICAL: Pytest wrapper function
def test_rc5_enc_16bit_hidden_runner():
    import os
    from pathlib import Path
    from cocotb_tools.runner import get_runner
    
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    
    sources = [
        proj_path / "sources/CA_8bit.sv",
        proj_path / "sources/rc5_enc_16bit.sv",
    ]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="rc5_enc_16bit",
        always=True,
    )
    
    runner.test(
        hdl_toplevel="rc5_enc_16bit",
        test_module="test_rc5_enc_16bit_hidden"
    )

