import serial
import time

class PS3305U:

    TIME_DEFAULT  = 100.0
    TIME_GET_DATA = 70.0 + TIME_DEFAULT
    TIME_GET_IDN  = 300.0 + TIME_DEFAULT

    def __init__(self, port='/dev/tty.usbserial-A9YL9R77'):
        # Configuración
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        self.ser.isOpen()

    def getID(self):
        return self._sendCMD('*IDN?', self.TIME_GET_IDN)

    def enableOUT(self):
        cmd = 'OUT1\r\n'
        self.ser.write(cmd.encode())

    def disableOUT(self):
        cmd = 'OUT0\r\n'
        self.ser.write(cmd.encode())

    def enableTRACK(self):
        cmd = 'TRACK1\r\n'
        self.ser.write(cmd.encode())

    def disableTRACK(self):
        cmd = 'TRACK0\r\n'
        self.ser.write(cmd.encode())

    def getERR(self):
        return self._sendCMD('ERR?', self.TIME_GET_DATA)

    def getSTATUS(self):
        return self._sendCMD('STATUS?')

    def _setDATA(self, c, n, d):
        cmd = str(c) + 'SET' + str(n) + ':' + str(d) + '\r\n'
        self.ser.write(cmd.encode())

    def _getOUT(self, c, n, m='OUT'):
        cmd = str(c) + str(m) + str(n) + '?'
        return self._sendCMD(cmd, self.TIME_GET_DATA).replace('V', '').replace('A', '')

    def setV1(self, v):
        if v >= 0 and v <= 30:
            self._setDATA('V', 1, v)

    def getV1(self):
        return float(self._getOUT('V', 1))

    def setV2(self, v):
        if v >= 0 and v <= 30:
            self._setDATA('V', 2, v)

    def getV2(self):
        return float(self._getOUT('V', 2))

    def setI1(self, i):
        if i >= 0 and i <= 5:
            self._setDATA('I', 1, i)

    def getI1(self):
        return float(self._getOUT('I', 1))

    def setI2(self, i):
        if i >= 0 and i <= 5:
            self._setDATA('I', 2, i)

    def getI2(self):
        return float(self._getOUT('I', 2))

    def getInfo(self):
        v1 = self.getV1()
        v2 = self.getV2()
        i1 = self.getI1()
        i2 = self.getI2()

        return "V1: %.2fV \t I1: %.2fA\nV2: %.2fV \t I2: %.2fA\n" % (v1, i1, v2, i2)

    def _sendCMD(self, cmd, t = 1000.0):

        cmd += '\r\n'
        self.ser.write(cmd.encode())

        out = ''
        # esperar 1 seg para recibir la respuesta
        # de la fuente de poder
        time.sleep(t / 1000.0)
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode("utf-8")

        return out
