from machine import SPI, Pin
from lora import SX1262 # or SX1261, depending on which you have

    

def get_modem():
    # The LoRa configuration will depend on your board and location, see
    # below under "Modem Configuration" for some possible examples.
    
#     lora_cfg = {
#         "freq_khz": 869000,
#         "sf": 7,
#         "bw": "125",  # kHz
#         "coding_rate": 5,
#         "preamble_len": 8,
#         "output_power": 14,  # dBm
#  #       "syncword":  0x1424
#  #       "pa_ramp_us": 80
#      }

# LORAWAN
#     lora_cfg = {
#         "freq_khz": 868100,
#         "sf": 7,
#         "bw": "125",  # kHz
#         "coding_rate": 5, # Works only with 4/8
#         "preamble_len": 8,
#         "output_power": 14,  # dBm
#         "syncword":  0x3444
#  #       "pa_ramp_us": 80
#      }

# Ebyte e32
    lora_cfg = {
        "freq_khz": 868000,
        "sf": 11,
        "bw": "500",  # kHz
        "coding_rate": 5, # 
        "preamble_len": 8,
        "output_power": 14,  # dBm
        "syncword":  0x1424,
        # "low_datarate_optimize": True
    }
    # To instantiate SPI correctly, see
    # https://docs.micropython.org/en/latest/library/machine.SPI.html
    spi = SPI(1, baudrate=8000000, sck=Pin(40), mosi=Pin(41), miso=Pin(38))
    cs = Pin(9)
    
    # or SX1261(), depending on which you have
    return SX1262(spi, cs,
                 busy=Pin(13),  # Required
                 dio1=Pin(45),   # Optional, recommended
                 reset=Pin(17),  # Optional, recommended
                 dio3_tcxo_millivolts=3300,
                 lora_cfg=lora_cfg)
