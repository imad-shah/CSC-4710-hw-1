from gui import WorldCupApp
from repository import WorldCupRepository, get_connection, init_db
from controller import WorldCupController


def main() -> None:
    con = get_connection()
    init_db(con)
    controller = WorldCupController(WorldCupRepository(con))
    app = WorldCupApp(controller)
    app.mainloop()
    con.close()


if __name__ == "__main__":
    main()
