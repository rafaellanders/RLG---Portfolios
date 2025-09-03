import os
import sys
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QTextEdit, QMessageBox
)

import tratapdf
import tratacsv


class PdfProcessor(QObject):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal()

    def __init__(self, pdf_paths, csv_path):
        super().__init__()
        self.pdf_paths = pdf_paths
        self.csv_path = csv_path

    def run(self):
        total = len(self.pdf_paths)
        for i, path in enumerate(self.pdf_paths, start=1):
            try:
                dados = tratapdf.abrepdf(path)
                try:
                    tratacsv.abrecsv(dados, self.csv_path)
                except TypeError:
                    tratacsv.abrecsv(dados)
                msg = f"OK: {os.path.basename(path)} feito."
            except Exception as e:
                msg = f"ERRO: {os.path.basename(path)} -> {e!s}"

            percent = int(i * 100 / total)
            self.progress.emit(percent, msg)

        self.finished.emit()


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processador de PDFs → CSV")
        self.setMinimumSize(700, 450)

        # botões
        self.btn_csv = QPushButton("Selecionar CSV destino…")
        self.btn_csv.clicked.connect(self.selecionar_csv)

        self.btn_pdfs = QPushButton("Selecionar PDFs…")
        self.btn_pdfs.clicked.connect(self.selecionar_pdfs)

        self.btn_faca = QPushButton("FAÇA")
        self.btn_faca.clicked.connect(self.processar)
        self.btn_faca.setEnabled(False)  # só habilitado depois de escolher CSV + PDFs

        # labels
        self.lbl_status = QLabel("Pronto.")
        self.lbl_csv = QLabel("CSV destino: (nenhum selecionado)")
        self.lbl_pdfs = QLabel("PDFs selecionados: 0")

        # progress bar e log
        self.bar = QProgressBar()
        self.bar.setValue(0)
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # layout
        top = QHBoxLayout()
        top.addWidget(self.btn_csv)
        top.addWidget(self.btn_pdfs)
        top.addWidget(self.btn_faca)
        top.addWidget(self.lbl_status)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.lbl_csv)
        layout.addWidget(self.lbl_pdfs)
        layout.addWidget(self.bar)
        layout.addWidget(self.log)

        cont = QWidget()
        cont.setLayout(layout)
        self.setCentralWidget(cont)

        # variáveis
        self.csv_path = None
        self.pdf_paths = []

        self._thread = None
        self._worker = None

    def selecionar_csv(self):
        caminho, _ = QFileDialog.getSaveFileName(
            self, "Selecionar CSV destino", "", "CSV Files (*.csv);;All Files (*)"
        )
        if caminho:
            if not caminho.lower().endswith(".csv"):
                caminho += ".csv"
            self.csv_path = caminho
            self.lbl_csv.setText(f"CSV destino: {self.csv_path}")
            self.log.append(f"CSV destino selecionado: {self.csv_path}")
            self.atualizar_botao_faca()

    def selecionar_pdfs(self):
        arquivos, _ = QFileDialog.getOpenFileNames(
            self, "Selecione um ou mais PDFs", "", "Arquivos PDF (*.pdf)"
        )
        if arquivos:
            self.pdf_paths = arquivos
            self.lbl_pdfs.setText(f"PDFs selecionados: {len(self.pdf_paths)}")
            self.log.append(f"{len(self.pdf_paths)} PDFs selecionados.")
            self.atualizar_botao_faca()

    def atualizar_botao_faca(self):
        # habilita o botão FAÇA somente se CSV e PDFs foram selecionados
        self.btn_faca.setEnabled(bool(self.csv_path and self.pdf_paths))

    def processar(self):
        if not self.csv_path or not self.pdf_paths:
            QMessageBox.warning(self, "Aviso", "Selecione CSV e PDFs antes de clicar em FAÇA.")
            return

        self.btn_csv.setEnabled(False)
        self.btn_pdfs.setEnabled(False)
        self.btn_faca.setEnabled(False)
        self.lbl_status.setText("Processando…")
        self.bar.setValue(0)
        self.log.append("Iniciando processamento de PDFs…")

        self._thread = QThread(self)
        self._worker = PdfProcessor(self.pdf_paths, self.csv_path)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._atualizar_progresso)
        self._worker.finished.connect(self._finalizar)

        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def _atualizar_progresso(self, percent, msg):
        self.bar.setValue(percent)
        self.log.append(msg)

    def _finalizar(self):
        self.lbl_status.setText("Concluído.")
        self.btn_csv.setEnabled(True)
        self.btn_pdfs.setEnabled(True)
        self.atualizar_botao_faca()
        self.log.append("Processamento finalizado.\n")
        self._worker = None
        self._thread = None


def iniciar_interface():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    app.exec()


if __name__ == "__main__":
    iniciar_interface()
