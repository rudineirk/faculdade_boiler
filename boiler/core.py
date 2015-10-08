from boiler.conn import BoilerConn
import time


def main():
    conn = BoilerConn()
    try:
        print("air_temp      : %.5f" % conn.air_temp)
        print("water_in_temp : %.5f" % conn.water_in_temp)
        while True:
            time.sleep(0.5)
            print("water_column  : %.5f" % conn.water_column)
            water_flux = input()
            conn.water_flux = float(water_flux)
    except KeyboardInterrupt:
        conn.close()


if __name__ == '__main__':
    main()
