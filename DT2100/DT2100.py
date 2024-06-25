import serial

def extract_value(data):
   # Convert bytearray to string and strip special characters
   data_str = data.decode('utf-8').replace('\x02', '').replace('\r', '')
   # Find the period and get the substring that ends just before it
   period_index = data_str.find('.')
   number_str = data_str[:period_index].strip()
   # Extract the number part which should be after the last space
   last_space_index = number_str.rfind(' ')
   number = number_str[last_space_index + 1:]
   return number

def pack_value(data):
    return b'\x02' + data + b'\r'

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b"\r")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\r")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

class DT2100:
    def __init__(self, port, baud=38400) -> None:
        self.ser = serial.Serial(port, baud)
        self.rl = ReadLine(self.ser)

    def getSpeed(self):
        self.ser.write(pack_value(b'CSD'))
        return extract_value(self.rl.readline())

