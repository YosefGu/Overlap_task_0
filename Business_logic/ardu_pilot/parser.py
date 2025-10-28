import struct
from pprint import pprint
import pandas as pd
from collections import defaultdict
import mmap
import time

START_MSG_MARKER = b'\xA3\x95'
START_FMT_MARKER = b'\xA3\x95\x80'

AP_TO_STRUCT = {
    'a': '32h',    # int16_t[16]
    'b': 'b',      # int8_t
    'B': 'B',      # uint8_t
    'h': 'h',      # int16_t
    'H': 'H',      # uint16_t
    'i': 'i',      # int32_t
    'I': 'I',      # uint32_t
    'f': 'f',      # float
    'd': 'd',      # double
    'n': '4s',     # char[4]
    'N': '16s',    # char[16]
    'Z': '64s',    # char[64]
    'c': 'h',   # int16_t[100]
    'C': 'H',   # uint16_t[100]
    'e': 'i',   # int32_t[100]
    'E': 'I',   # uint32_t[100]
    'L': 'i',      # int32_t (lat/lon)
    'M': 'B',      # uint8_t (flight mode)
    'q': 'q',      # int64_t
    'Q': 'Q',      # uint64_t
}

char_to_multiple = ['c', 'C', 'e', 'E']

   



class Parser:

    def __init__(self, path : str):
        self.path = path
        self.fmts = {}
        self.messages = defaultdict(list)
        
    def read_file(self):
        # counter = 0
        start_time = time.time()
        with open(self.path, "rb") as file, mmap.mmap(
            file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            self.create_fmts_dict(mm)
            start_pos = 0
            while True:
                # counter += 1
                start_pos = mm.find(START_MSG_MARKER, start_pos)                    
                if start_pos == -1:
                    break                

                msg_type = mm[start_pos + 2] 
                fmt = self.fmts.get(msg_type)

                if not fmt:
                    start_pos += 1
                    continue

                if msg_type != 128:
                    payload = mm[start_pos + 3: start_pos  + fmt["length"]]                
                    values = struct.unpack(fmt["format"], payload)
                    decodes_values = []
                    for val in values:
                        if isinstance(val, bytes):
                            decodes_values.append(val.decode('ascii', errors='ignore').rstrip('\x00'))
                        else:
                            decodes_values.append(val)
                    scale_values = self.scale_data(values, fmt["row_format"])
                    self.messages[msg_type].append(scale_values)
                    start_pos += fmt["length"]
                else:
                    start_pos += 89
        end_time = time.time()
        print(f"time:{end_time - start_time:.3f}")
        # print("messages count:",counter)
        # print("fack msg count:",fack_msg)

    def scale_data(self, values, format_):
        updated_values = list(values)
        for index, chr in enumerate(format_):
            if chr in char_to_multiple:
                updated_values[index] *= 100
        return updated_values
    
    def create_fmts_dict(self, mm):
        start_pos = 0  
        count_fake_fmt = 0
        while True:
            start_pos = mm.find(START_FMT_MARKER, start_pos)
            if start_pos == -1:
                break

            try:
                payload = mm[start_pos + 3 : start_pos + 89]
                fmt_format = "<BB4s16s64s"
                type_, length, name, format_, columns = struct.unpack_from(fmt_format, payload)

                decode_name = name.decode('ascii', errors='ignore').rstrip('\x00')
                format_str_raw = format_.decode('ascii', errors='ignore').rstrip('\x00')
                columns_str = columns.decode('ascii', errors='ignore').rstrip('\x00')
                if decode_name.isalnum():
                    format_str = self.ap_fmt_to_struct(format_str_raw)
                    self.fmts[type_] = {
                        "length" : length,
                        "name" : decode_name,
                        "format" : format_str,
                        "row_format" : format_str_raw,
                        "columns" : columns_str.split(',') 
                    }
                    start_pos += 89
                else:
                    count_fake_fmt += 1
                    start_pos += 1
            except Exception as e:
                count_fake_fmt += 1
                start_pos += 1
        print("count fmt:", len(self.fmts))
        print("count fack fmt:", count_fake_fmt)    
    
    def ap_fmt_to_struct(self, fmt_str):
        """
        Get ArduPilot format and convert it to a struct format.
        """
        struct_fmt = '<'  # Little-endian
        for c in fmt_str:
            if c not in AP_TO_STRUCT:
                raise ValueError(f"Unknown format char: {c}")
            struct_fmt += AP_TO_STRUCT[c]
        return struct_fmt   
        
p = Parser(r"C:\Users\yos77\Documents\ness\overlap\log_file_test_01.bin")
p.read_file()