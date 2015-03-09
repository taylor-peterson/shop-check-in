import Queue as queue

import fsm
import io_moderator
import id_logger
from website.server import LiveSite
import shop_user_database


def main():
    event_q = queue.Queue()
    message_q = queue.Queue()

    print "Connecting to Database..."

    shop_user_db = shop_user_database.ShopUserDatabaseTesting()

    print "Setting up ID Logger..."

    thread_id_logger = id_logger.IdLogger(event_q)
    thread_id_logger.daemon = True
    thread_id_logger.start()

    print "Setting up IO Moderator..."

    thread_io_moderator = io_moderator.IoModerator(event_q, message_q)
    thread_io_moderator.daemon = True
    thread_io_moderator.start()

    print "Setting up FSM..."

    board = fsm.BoardFsm(event_q, message_q, shop_user_db)

    server = LiveSite(board._shop)
    server.daemon = True
    server.start()

    board.run_fsm()

if __name__ == "__main__":
    main()
