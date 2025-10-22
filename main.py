import flet as ft
from alert import AlertManager
from automobile import Automobile
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label='Marca',
                               width=280)
    input_modello = ft.TextField(label='Modello',
                                 width=280)
    input_anno = ft.TextField(label='Anno',
                              width=280)

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24)
    txtOut = ft.TextField(width=50,
                          disabled=True,
                          value='0',
                          border_color="green",
                          text_align=ft.TextAlign.CENTER)

    input_aggiunta = ft.ElevatedButton('Aggiungi automobile')


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    #hendlers per il counter
    def decrementa_posti(e):
        valore = int(txtOut.value or 0)
        txtOut.value = str(max(0, valore - 1))  # evita negativi
        txtOut.update()

    def incrementa_posti(e):
        valore = int(txtOut.value)
        txtOut.value = str(valore + 1)
        txtOut.update()

    #hendler per l'inserimento auto
    def aggiungi_automobili(e):
        marca = (input_marca.value or '').strip()     #'or' e strip() per evitare spazi o campi vuoti
        modello = (input_modello.value or '').strip()
        anno_str = (input_anno.value or '').strip()
        posti_str = (txtOut.value or '0').strip()
        #controllo sull'inserimento
        if not marca or not modello or not anno_str:
            alert.show_alert("❌ Compila marca, modello e anno.")
            return

        try:
            anno = int(anno_str)
            posti = max(1, int(posti_str)) #con il numero '1' si dice 'almeno un posto
            if anno <= 0 or posti <= 0:
                raise ValueError
        except ValueError:
            alert.show_alert("❌ Inserire valori numerici validi per anno e posti.")
            return
        # Creo l'oggetto Automobile (adattato ai parametri del costruttore)
        autonoleggio.aggiungi_automobile(marca, modello, anno, posti)

        # Reset parametri
        input_marca.value = ''
        input_modello.value = ''
        input_anno.value = ''
        txtOut.value = '0'
        page.update()

        #aggiorno la lista
        aggiorna_lista_auto()

    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btnMinus.on_click = decrementa_posti
    btnAdd.on_click = incrementa_posti
    input_aggiunta.on_click=aggiungi_automobili
    # TODO


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing=20,
               controls=[input_marca, input_modello, input_anno, btnMinus, txtOut, btnAdd ],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[input_aggiunta],
               alignment=ft.MainAxisAlignment.CENTER),
        # TODO

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
