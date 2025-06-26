import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
from src.logica.Eporra import Eporra
from src.modelo.declarative_base import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    logica = Eporra()

    app = App_EPorra(sys.argv, logica)
    sys.exit(app.exec_())