"""Module for Eastron SDM120M board registers definition."""
# =============================================================================
# Eastron SDM120-M - Modbus Input Registers
# =============================================================================
#
# AREA_A
# Range: 0x0000 - 0x001F
# Count: 32 registers
#
#   0x0000  Voltage                         V
#   0x0006  Current                         A
#   0x000C  Active Power                    W
#   0x0012  Apparent Power                  VA
#   0x0018  Reactive Power                  VAr
#   0x001E  Power Factor                    -
#
#
# AREA_B
# Range: 0x0156 - 0x0157
# Count: 2 registers
#
#   0x0156  Total Active Energy             kWh
#
#
# NOT INCLUDED IN CURRENT AREAS
#
#   0x0046  Frequency                       Hz
#   0x0048  Import Active Energy            kWh
#   0x004A  Export Active Energy            kWh
#   0x004C  Import Reactive Energy          kVArh
#   0x004E  Export Reactive Energy          kVArh
#   0x0050  Apparent Energy                 kVAh
#   0x0052  Ampere-hours                    Ah
#   0x0054  Total System Power Demand       W
#   0x0056  Max Total System Power Demand   W
#   0x0058  Import System Power Demand      W
#   0x005A  Max Import Power Demand         W
#   0x005C  Export System Power Demand      W
#   0x005E  Max Export Power Demand         W
#
#   0x0102  Current Demand                  A
#   0x0108  Maximum Current Demand          A
#
#   0x0158  Total Reactive Energy           kVArh
#
#   0x4EA2  CO2                             kg
#
# =============================================================================
#
# Register type : Input Register (Modbus FC04)
# Data type     : FLOAT32
# Register size : 2 consecutive 16-bit registers per value
# =============================================================================
from __future__ import annotations

from homeassistant.const import (
    ATTR_VOLTAGE,
    Platform,
    UnitOfEnergy,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
)
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_INPUT,
    DataType,
)

from ...helpers.boards import register_board
from ...helpers.ha import ensure_number_in_platforms
from ...const import CONF_NUMBERS
from ..boards import BoardDefinition, Metadata, Register, RegisterArea, RegisterFunction, RegisterFunctionRead
from ..enums import Board, RegisterAreaName, SensorFunction

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   EASTRON SDM120M
####### ####### ####### ####### #######

@register_board(Board.EASTRON_SDM120M)
def _sdm120m_regs():
    return BoardDefinition(
        metadata = Metadata(name="Modbus Energy Meter", manufacturer="eastron", model="sdm120m"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=32,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.FLOAT32,
            ),
            RegisterAreaName.AREA_B: RegisterArea(
                address=0x0156,
                count=2,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.FLOAT32,
            )
        },
        registers = {
            Platform.SENSOR: Register(
                functions={
                    SensorFunction.VOLTAGE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x00,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class=ATTR_VOLTAGE,
                        unit_of_measurement=UnitOfElectricPotential.VOLT
                    ),
                    SensorFunction.CURRENT: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x06,

                        function_read=RegisterFunctionRead(
                            precision=2,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="current",
                        unit_of_measurement=UnitOfElectricCurrent.AMPERE
                    ),
                    SensorFunction.ACTIVE_POWER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0C,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="power",
                        unit_of_measurement=UnitOfPower.WATT
                    ),
                    SensorFunction.APPARENT_POWER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x12,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="apparent_power",
                        unit_of_measurement="VA",
                    ),
                    SensorFunction.REACTIVE_POWER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x18,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="reactive_power",
                        unit_of_measurement="var",
                    ),
                    SensorFunction.POWER_FACTOR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x1E,

                        function_read=RegisterFunctionRead(
                            precision=3,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="power_factor",
                        unit_of_measurement=None,
                    ),
                    SensorFunction.TOTAL_ACTIVE_ENERGY: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x00,

                        function_read=RegisterFunctionRead(
                            precision=2,
                            scale=1,
                        ),

                        state_class="total",
                        device_class="energy",
                        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR
                    ),
                }
            )
        }
    )
