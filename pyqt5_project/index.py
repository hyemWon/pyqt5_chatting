import sys
import login, join, main
from PyQt5.QtWidgets import QApplication, QStackedWidget



if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    login_obj = login.LoginForm(widget)
    widget.addWidget(login_obj)

    join_obj = join.JoinForm(widget)
    widget.addWidget(join_obj)

    main_obj = main.MainForm(widget)
    widget.addWidget(main_obj)

    widget.setWindowTitle("4IND")
    widget.setFixedWidth(1200)
    widget.setFixedHeight(800)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")