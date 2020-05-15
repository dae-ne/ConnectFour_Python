# Cztery w rzędzie (Connect Four)

## Opis gry
"Cztery w rzędzie" jest dwuosobową grą planszową na planszy zbudowanej z siatki 7x6.
Wygrywa w niej gracz, który ułoży 4 monety w jednej linii (poziomo, pionowo lub po skosie).
Moneta może być umieszczona tylko w najniższym wolnym miejscu w kolumnie.

## Opis zadania
- Okno wyświetlające siatkę 7 kolumn x 6 wierszy, informację “Player 1” lub “Player 2”,
    przycisk do resetowania gry oraz przycisk służący do wyświetlenia pomocy:
    sposobu sterowania i reguł gry.
- Początkowo pola siatki są puste.
- Gracze na zmianę wrzucają monety do wybranych przez siebie kolumn.
- Pola w których jest moneta gracza 1 są czerwone, pola z monetami gracza 2
    są żółte.
- Po najechaniu kursorem myszy na kolumnę zostaje ona podświetlona i po kliknięciu
    przycisku myszy moneta zostaje dodana do najniższej wolnej pozycji
    w podświetlonej kolumnie.
- Wygrywa gracz który pierwszy ustawi cztery monety w linii (poziomo, pionowo
    lub po skosie).
- Gdy gra się kończy, wyświetlane jest okienko z napisem “Wygrał gracz 1” lub
    “Wygrał gracz 2”, zależnie kto wygrał grę. Możliwe jest zresetowanie planszy
    bez zamykania głównego okna.
- Reprezentacja reguł gry ma być realizowana poprzez hierarchię klas. Klasa
    bazowa definiuje między innymi funkcję wirtualną ktoWygral() nadpisywaną w
    klasach pochodnych. Realizowane powinny być przynajmniej dwa zestawy reguł,
    jako dwie klasy pochodne.

## Testy
1. Wykonanie po dwa ruchy przez każdego z graczy - monety spadają na dół pola
gry lub zatrzymują się na już wrzuconym żetonie.
2. Ułożenie pionowej linii monet przez jednego gracza - oczekiwana informacja o
jego wygranej.
3. Ułożenie poziomej linii monet przez drugiego gracza - oczekiwana informacja o
jego wygranej.
4. Ułożenie skośnej linii przez dowolnego gracza - oczekiwana informacja o
jego wygranej.
5. Zapełnienie pola gry tak, że żaden gracz nie ułożył linii - oczekiwana informacja
o remisie.
6. Ułożenie linii dłuższej niż 4 przez jednego z graczy - oczekiwana informacja o
jego wygranej.
[c][c][c][ ][c][c][c]
[ż][ż][ż][ ][ż][ż][ż] <- w następnym ruchu gracz żółty wrzuci monetę w
środkową kolumnę.
7. Próba wrzucenia monety do zapełnionej kolumny - oczekiwana informacja o błędzie.
