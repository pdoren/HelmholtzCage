import serial
import time
import math

class HMC5883L:

    TIME_GET_DATA = 100

    HMC5883L_RANGE_0_88GA = 0.073
    HMC5883L_RANGE_1_3GA = 0.92
    HMC5883L_RANGE_1_9GA = 1.22
    HMC5883L_RANGE_2_5GA = 1.52
    HMC5883L_RANGE_4GA = 2.27
    HMC5883L_RANGE_4_7GA = 2.56
    HMC5883L_RANGE_5_6GA = 3.03
    HMC5883L_RANGE_8_1GA = 4.35

    CMD_MAG = b'\x55'
    CMD_ERR = b'\x21'

    def __init__(self, port, mgPerDigit=HMC5883L_RANGE_1_3GA):
        # Configuración
        self.ser = serial.Serial(
            port=port,
            baudrate=38400,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS
        )
        self.mgPerDigit = mgPerDigit
        self.ser.isOpen()

    def getERR(self):
        strMag = self._sendCMD(self.CMD_ERR, self.TIME_GET_DATA)
        return strMag

    def getMAG(self):
        d = self._sendCMD(self.CMD_MAG, self.TIME_GET_DATA)
        try:
            return [float(i) * self.mgPerDigit for i in d.split(';')]
        except ValueError:
            return None

    def computeHeading(self, mag):
        heading = math.atan2(mag[1], mag[0])
        if heading < 0:
            heading += 2.0 * math.pi
        return heading * 180.0/math.pi; # 0 indica el norte

    def getInfo(self):
        mag = self.getMAG()
        if mag is not None:
            heading = self.computeHeading(mag)
            return "MAG: (%0.2fmG, %0.2fmG, %0.2fmG) HEADING: %.2fDEG \n" % (mag[0], mag[1], mag[2], heading)
        else:
            return '';

    def _sendCMD(self, cmd, t = 1000.0):

        self.ser.write(cmd)

        out = ''
        # esperar 1 seg para recibir la respuesta
        # de la fuente de poder
        time.sleep(t / 1000.0)
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode()

        return out
