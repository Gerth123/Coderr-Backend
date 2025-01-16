# Coderr - Jobplattform Backend

Dieses Repository beinhaltet das Backend der Jobplattform **Coderr**. Die Plattform dient dazu, Unternehmen und Kunden zu vernetzen und bietet verschiedene Funktionen zur Verwaltung von Profilen und Angeboten. Das Backend wurde mit **Python**, **Django**, und **Django REST Framework (DRF)** entwickelt.

## Features

- **Sales Page**: Eine Seite, die potenzielle Nutzer über die Vorteile von Coderr informiert.
- **Login und Registrierung**: Sichere Authentifizierung und Benutzerverwaltung für Kunden und Unternehmen.
- **Angebotsliste**: Anzeige aller verfügbaren Angebote auf der Plattform.
- **Einzelne Angebotsseite**: Detaillierte Informationen zu einem spezifischen Angebot.
- **Eigenes Profil**:
  - **Kunde**: Benutzer können ihre persönlichen Daten und Einstellungen verwalten.
  - **Business**: Unternehmen können ihre Firmendaten und angebotenen Dienstleistungen verwalten.
- **Fremdansicht von Profilen**:
  - **Kunde**: Ansicht eines Kundenprofils durch andere Benutzer.
  - **Business**: Ansicht eines Unternehmensprofils durch andere Benutzer.
- **Rechtliches**:
  - **Datenschutzerklärung**: Transparente Informationen zur Datennutzung.
  - **Impressum**: Rechtliche Angaben zur Plattform.

## Technologie-Stack

- **Programmiersprache**: Python
- **Framework**: Django
- **REST-API**: Django REST Framework (DRF)
- **Datenbank**: Konfigurierbar, typischerweise SQLite, PostgreSQL oder MySQL

## API-Endpunkte

### Endpoints zu Angeboten:

```plaintext
GET    /offers/                 - Liste aller Angebote mit Filter- und Suchmöglichkeiten
POST   /offers/                 - Erstellen eines neuen Angebots inklusive zugehöriger Details
GET    /offers/{id}/            - Abrufen der Details eines spezifischen Angebots
PATCH  /offers/{id}/            - Aktualisieren eines spezifischen Angebots
DELETE /offers/{id}/            - Löschen eines spezifischen Angebots
GET    /offerdetails/{id}/      - Abrufen der Details eines spezifischen Angebotsdetails
```

### Endpoints zu Bestellungen:

```plaintext
GET    /orders/                         - Liste der Bestellungen des angemeldeten Benutzers
POST   /orders/                         - Erstellen einer neuen Bestellung basierend auf einem Angebot
GET    /orders/{id}/                    - Abrufen der Details einer spezifischen Bestellung
PATCH  /orders/{id}/                    - Aktualisieren des Status einer spezifischen Bestellung
DELETE /orders/{id}/                    - Löschen einer Bestellung (nur durch Admins)
GET    /order-count/{business_user_id}/ - Gibt die Anzahl der laufenden Bestellungen eines Geschäftsnutzers zurück
GET    /completed-order-count/{business_user_id}/ - Gibt die Anzahl der abgeschlossenen Bestellungen eines Geschäftsnutzers zurück
```

### Endpoints zu Basisinformationen:

```plaintext
GET /base-info/ - Abrufen der allgemeinen Basisinformationen der Plattform
```

### Endpoints für Benutzerprofile:

```plaintext
GET    /profile/<int:pk>/      - Abrufen der Details eines spezifischen Nutzers
PATCH  /profile/<int:pk>/      - Aktualisieren der Details eines spezifischen Nutzers
GET    /profiles/business/     - Liste aller Geschäftsnutzer
GET    /profiles/customer/     - Liste aller Kundenprofile
```

### Endpoints für Authentifizierung/Registrierung:

```plaintext
POST /login/         - User-Login
POST /registration/  - User-Registrierung
```

### Endpoints für Bewertungen:

```plaintext
GET    /reviews/           - Liste aller Bewertungen
POST   /reviews/           - Erstellen einer neuen Bewertung
GET    /reviews/{id}/      - Abrufen der Details einer spezifischen Bewertung
PATCH  /reviews/{id}/      - Aktualisieren einer spezifischen Bewertung
DELETE /reviews/{id}/      - Löschen einer spezifischen Bewertung
```

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Weitere Details findest du in der Lizenzdatei.

## Kontakt

Bei Fragen oder Anregungen wende dich gerne an [deine E-Mail-Adresse eintragen].

