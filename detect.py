import subprocess

def detect_license_plate(image_path):
    """Wykrywanie tablic rejestracyjnych za pomocą alpr.exe."""
    try:
        # Ścieżka do alpr.exe
        alpr_path = r"D:\openalpr-2.3.0-win-64bit\openalpr_64\alpr.exe"

        # Uruchomienie alpr.exe
        result = subprocess.run(
            [alpr_path, "-c", "eu", image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Sprawdzenie wyniku
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"Wynik alpr.exe: {output}")

            # Parsowanie wyniku
            lines = output.splitlines()
            for line in lines:
                if "confidence:" in line:
                    parts = line.split()
                    plate = parts[1]  # Pierwszy element po "-"
                    return plate  # Zwróć pierwszy wynik

        print(f"Błąd w alpr.exe: {result.stderr}")
        return None
    except Exception as e:
        print(f"Błąd: {str(e)}")
        return None
