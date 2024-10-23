import cv2
import numpy as np

def draw_bezier_curve(image, p0, p1, p2, curvature_factor=1.0, color=(0, 0, 255), thickness=2):
    """
    Zeichnet eine quadratische Bézier-Kurve auf ein Bild.
    
    Parameter:
    - image: Das Bild, auf dem die Kurve gezeichnet wird
    - p0, p1, p2: Die Punkte (Startpunkt, Kontrollpunkt, Endpunkt) als Tupel (x, y)
    - curvature_factor: Krümmungsfaktor, der den Einfluss des Kontrollpunkts steuert
    - color: Farbe der Kurve (BGR)
    - thickness: Linienstärke der Kurve
    """
    
    # Skaliere den Kontrollpunkt mit dem Krümmungsfaktor
    p1 = np.array(p0) + curvature_factor * (np.array(p1) - np.array(p0))
    
    # Quadratische Bézier-Funktion: P(t) = (1 - t)^2 * P0 + 2 * (1 - t) * t * P1 + t^2 * P2
    def bezier_curve(p0, p1, p2, t):
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

    # Berechne die Punkte der Bézier-Kurve
    curve_points = []
    for t in np.linspace(0, 1, 100):  # 100 Punkte auf der Kurve
        point = bezier_curve(np.array(p0), np.array(p1), np.array(p2), t)
        curve_points.append(point.astype(int))

    # Zeichne die Kurve, indem du die Punkte verbindest
    for i in range(len(curve_points) - 1):
        cv2.line(image, tuple(curve_points[i]), tuple(curve_points[i + 1]), color, thickness)

    # Zeichne die Punkte A, B und C für die Visualisierung
    cv2.circle(image, tuple(p0), 5, (0, 255, 0), -1)  # Punkt A (Startpunkt)
    cv2.circle(image, tuple(p1.astype(int)), 5, (255, 0, 0), -1)  # Punkt C (Kontrollpunkt)
    cv2.circle(image, tuple(p2), 5, (0, 255, 0), -1)  # Punkt B (Endpunkt)
    
    return image


# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    # Erstelle ein weißes Bild
    image = np.ones((400, 400, 3), dtype=np.uint8) * 255

    # Definiere die Punkte A, B, C
    p0 = (50, 300)   # Startpunkt (A)
    p1 = (200, 100)  # Kontrollpunkt (C)
    p2 = (350, 300)  # Endpunkt (B)

    # Krümmungsfaktor (z.B. 1.0 für normale Krümmung, >1 für stärkere Krümmung)
    curvature_factor = 1.9

    # Zeichne die Bézier-Kurve auf das Bild
    result_image = draw_bezier_curve(image, p0, p1, p2, curvature_factor)

    # Zeige das Bild an
    cv2.imshow('Bezier Curve with Curvature Factor', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()