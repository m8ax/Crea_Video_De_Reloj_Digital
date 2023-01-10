# M8AX - Programa Para Crear Un Video De Un Reloj Digital, Con Todas Sus Horas, Minutos Y Segundos.
# La Variable segundoscalcular Es La Que Indica El Número De Relojes A Realizar Para Posteriormente Hacer El Video.
# Si segundoscalcular=86400 Se Hacen 86400 Relojes Para Hacer El Video... 24h
# Si segundoscalcular=43200 Se Hacen 43200 Relojes Para Hacer El Video... 12h - Por Defecto.
# Usa Una Imágen De Fondo fondorelojmviiiax.PnG, Incluida...

import cv2
import os
import errno
import numpy as np
import glob
import time
from shutil import rmtree

def agregar_cero(valor):
    return f"{valor:02d}"

def segahmss(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"

def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return horas, minutos, segundos

def barra_progreso_roja(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        (
            f"\r\033[38;2;{255};{0};{0}m|{barra}| - ETA - {segahmss(segrestante*-1)} -"
            f" {porcen:.2f}%      "
        ),
        end="\r\033[0m",
    )

os.system("cls")

try:
    rmtree("M8AX-HoraS")
except:
    nn = 0

try:
    os.mkdir("M8AX-HoraS")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

I = cv2.imread("fondorelojmviiiax.PnG")
font1 = cv2.FONT_HERSHEY_SIMPLEX
nn = 0
tiembarra = totaltiem = time.time()
segundoscalcular = int(
    input("¿ Cuántos Relojes Hacemos ?: 86400 = 24H = 86400 Relojes. ")
)
print("\nM8AX - ... Haciendo Imágenes Del Reloj Digital ...\n")

for k in range(0, segundoscalcular):
    hour, minute, second = segahms(k)
    if second == 0:
        ColorLetra = (
            np.random.randint(75, 256),
            np.random.randint(75, 256),
            np.random.randint(75, 256),
        )
    texto = (
        str(agregar_cero(hour))
        + ":"
        + str(agregar_cero(minute))
        + ":"
        + str(agregar_cero(second))
    )
    I1 = cv2.putText(I.copy(), texto, (350, 905), font1, 9, ColorLetra, 50)
    I2 = cv2.putText(I.copy(), ".           .", (72, 115), font1, 9, ColorLetra, 50)
    I3 = cv2.add(cv2.resize(I2, (1920, 1080)), cv2.resize(I1, (1920, 1080)))
    if k % 2 == 0:
        cv2.imwrite("./M8AX-HoraS/M8AX-Reloj-" + str(k) + ".PnG", I1)
    else:
        cv2.imwrite("./M8AX-HoraS/M8AX-Reloj-" + str(k) + ".PnG", I3)
    cv2.imshow("frame", I1)
    cv2.waitKey(1)
    barra_progreso_roja((k * 100) / segundoscalcular, 100, tiembarra)
barra_progreso_roja((segundoscalcular * 100) / segundoscalcular, 100, tiembarra)
cv2.destroyAllWindows()
print("\n\nM8AX - ... Imágenes Terminadas, Haciendo Video ...\n")
framesize = ((1920), (1080))
outv = cv2.VideoWriter(
    "M8AX-Reloj-12h" + "-Video.Mp4",
    cv2.VideoWriter_fourcc(*"h265"),
    1,
    framesize,
)

tiembarra = time.time()
print("")

for filename in sorted(glob.glob("./M8AX-HoraS/*.png"), key=os.path.getmtime):
    imgv = cv2.imread(filename)
    outv.write(imgv)
    nn = nn + 1
    barra_progreso_roja(
        (nn * 100) / (len(glob.glob("./M8AX-HoraS/*.png"))), 100, tiembarra
    )

barra_progreso_roja((nn * 100) / (len(glob.glob("./M8AX-HoraS/*.png"))), 100, tiembarra)
print("\n")
print(*sorted(glob.glob("./M8AX-HoraS/*.png"), key=os.path.getmtime), sep="\n")
outv.release()
calpors = round((segundoscalcular) / (time.time() - totaltiem), 3)
print(
    f"\n... Video Realizado Correctamente ...\n\n----- M8AX INFORMACIÓN -----\n\nRelojes Creados - {segundoscalcular}.\n\nTiempo De Proceso - {round(time.time()-totaltiem,3)} Segundos - {segahmss(time.time()-totaltiem)}.\n\nRelojes Por Segundo Procesados - {calpors} Rel/s.\n\nA Este Rítmo, En Un Minuto Se Realizan - {round(calpors*60,3)} Relojes.\n\nA Este Rítmo, En Una Hora Se Realizan - {round(calpors*3600,3)} Relojes."
)
print("\nSuscribete A Mi Canal De Youtube - https://youtube.com/m8ax")